from concurrent.futures import ThreadPoolExecutor
import os
import cv2
import glob
import time
import shutil
from datetime import datetime
from config import MODEL_PATH
from ultralytics import YOLO
from db import session
from services.getting_video_service import GettingVideo
from services.video_saver_service import VideoSaver
from services.camera_service import CameraService
from services.recorded_video_service import RecordedVideoService
from services.bird_detection_service import BirdDetectionService
from services.mode_service import ModeService
from services.permission_service import PermissionService
from services.deterrence_service import DeterrenceService
from models.deterrence_permission import DeterrencePermission
from models.enums.system_mode import SystemMode

camera_service = CameraService(session)
recorded_video_service = RecordedVideoService(session)
bird_detection_service = BirdDetectionService(session)
permission_service = PermissionService(session)
mode_service = ModeService(session)
deterrence_service = DeterrenceService(session)

model = YOLO(MODEL_PATH)

def save_video(cap, width, height, fps):
    saver = VideoSaver(width, height, fps)
    saver.create_temp_writer()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        saver.write_frame(frame)
    return saver.release()

def save_detected_video(camera_id):
    predict_dirs = sorted(glob.glob("runs/detect/predict*"), key=os.path.getmtime)
    if not predict_dirs:
        return None
    latest_dir = predict_dirs[-1]
    output_dir = f'static/videos/detected/camera_{camera_id}_{int(time.time())}'
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(latest_dir):
        if file.endswith(('.mp4', '.avi')):
            src = os.path.join(latest_dir, file)
            dst = os.path.join(output_dir, f"{int(time.time())}.mp4")
            shutil.move(src, dst)
            shutil.rmtree(latest_dir)
            return dst
    shutil.rmtree(latest_dir)
    return None

def process_camera(camera):
    if not hasattr(camera, "device_path"):
        return

    start_time = datetime.now()
    cap = GettingVideo().get_video(camera.device_path)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    temp_video_path = save_video(cap, width, height, fps)
    cap.release()

    saved_dir = f"static/videos/saved/camera_{camera.id}"
    os.makedirs(saved_dir, exist_ok=True)
    final_video_path = os.path.join(saved_dir, f"{int(time.time())}.mp4")
    shutil.move(temp_video_path, final_video_path)

    video = recorded_video_service.create(
        start_time=start_time,
        end_time=datetime.now(),
        file_path=final_video_path,
        camera_id=camera.id,
        note="auto"
    )

    results = model.predict(source=final_video_path, save=True, conf=0.25, device="cpu")
    total_boxes = sum(len(r.boxes) for r in results)
    if total_boxes == 0:
        print("❎ Птахів не виявлено")
        return

    box_counts = [len(r.boxes) for r in results if r.boxes]
    if box_counts:
        min_birds = min(box_counts)
        max_birds = max(box_counts)
    else:
        min_birds = max_birds = 0

    confidences = [float(b.conf[0]) for r in results if r.boxes for b in r.boxes]
    total_boxes = len(confidences)
    avg_conf = sum(confidences) / total_boxes if total_boxes > 0 else 0

    detection_video_path = save_detected_video(camera.id)
    if not detection_video_path:
        print("❌ Не вдалося зберегти відео з виявленням")
        return

    detection = bird_detection_service.create(
        timestamp=datetime.now(),
        video_id=video.id,
        confidence=avg_conf,
        bird_lowest_amount=min_birds,
        bird_highest_amount=max_birds,
        videopath=detection_video_path
    )

    if mode_service.get_mode() == SystemMode.manual.value:
        print(f"🟡 Ручний режим — очікування дозволу для detection_id={detection.id}")
        permission = permission_service.create_permission(detection.id, None, allow=None)
        while True:
            if permission_service.is_allowed(detection.id):
                permission = (
                    permission_service.session.query(DeterrencePermission)
                    .filter_by(detection_id=detection.id)
                    .first()
                )
                print("✅ Дозвіл надано — відлякування активується")
                deterrence_service.activate(camera.id, detection.id, permission.user_id)
                break
            elif permission_service.is_denied(detection.id):
                print("❌ Відлякування заборонено вручну")
                return
            time.sleep(2)
    else:
        deterrence_service.activate(camera.id, detection.id)

def main():
    while True:
        cameras = camera_service.get_all()
        with ThreadPoolExecutor(max_workers=len(cameras)) as executor:
            futures = [executor.submit(process_camera, camera) for camera in cameras]
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"⚠️ Помилка при обробці потоку: {e}")
        time.sleep(30000000)

if __name__ == "__main__":
    main()
