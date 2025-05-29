import os
import cv2
import xml.etree.ElementTree as ET

def extract_frames(video_path, output_dir, prefix):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_name = f"{prefix}_{frame_id:06d}.jpg"
        cv2.imwrite(os.path.join(output_dir, frame_name), frame)
        frame_id += 1
    cap.release()

def convert_xml_to_yolo(xml_dir, output_dir, prefix):
    os.makedirs(output_dir, exist_ok=True)
    for xml_file in sorted(os.listdir(xml_dir)):
        if not xml_file.endswith(".xml"):
            continue
        tree = ET.parse(os.path.join(xml_dir, xml_file))
        root = tree.getroot()

        size = root.find("size")
        w = int(size.find("width").text)
        h = int(size.find("height").text)
        filename = root.find("filename").text

        yolo_lines = []
        for obj in root.findall("object"):
            bbox = obj.find("bndbox")
            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)

            x_center = ((xmin + xmax) / 2) / w
            y_center = ((ymin + ymax) / 2) / h
            width = (xmax - xmin) / w
            height = (ymax - ymin) / h

            yolo_lines.append(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        output_file = f"{prefix}_{filename}.txt"
        with open(os.path.join(output_dir, output_file), "w") as f:
            f.write("\n".join(yolo_lines))

def process_all(folder):
    video_dir = f"training/videos/{folder}"
    label_root = f"training/videos/labels/{folder}"
    out_image_dir = f"training/images/video_{folder}/images"
    out_label_dir = f"training/images/video_{folder}/labels"

    for video_file in os.listdir(video_dir):
        if not video_file.endswith(".mp4"):
            continue
        video_name = video_file.replace(".mp4", "")
        video_path = os.path.join(video_dir, video_file)
        label_dir = os.path.join(label_root, video_name)

        print(f"⏳ Processing: {video_file}")
        extract_frames(video_path, out_image_dir, video_name)
        convert_xml_to_yolo(label_dir, out_label_dir, video_name)
        print(f"✅ Done: {video_file}")


process_all("train")
process_all("val")
