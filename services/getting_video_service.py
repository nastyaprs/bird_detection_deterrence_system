import cv2
import platform
import time

class GettingVideo:
    def get_video(self, source_path: str):
        if platform.system() == 'Windows':
            cap = cv2.VideoCapture(source_path)
            if not cap.isOpened():
                raise IOError(f"Не вдалося відкрити відео: {source_path}")
            return cap
        else:
            cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

            if not cap.isOpened():
                raise IOError("Не вдалося відкрити камеру")

            start_time = time.time()
            duration = 10

            frames = []
            while time.time() - start_time < duration:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)

            cap.release()
            return frames
