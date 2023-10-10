import cv2
import torch
from pathlib import Path
from ultralytics import YOLO



# Initialize
# model = torch.hub.load('ultralytics/yolov8n', 'yolov8n')  # You can change 'yolov5s' to 'yolov5m', 'yolov5l', or 'yolov5x' for larger models
model = YOLO(f'./model/yolov8n-face.pt', task="segment")

vid_path = './temp/mp4_2023-10-10_08-35-26.mp4'  # Replace with your video path
save_path = './saved_faces/'  # Folder to save detected faces
Path(save_path).mkdir(parents=True, exist_ok=True)

# Open video file
cap = cv2.VideoCapture(vid_path)

frame_num = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Inference
    results = model(frame, save=True, verbose=True)

    # #Extract bounding box coordinates
    # for *xyxy, conf, cls in results[0]:
    #     x1, y1, x2, y2 = map(int, xyxy)
    #     face = frame[y1:y2, x1:x2]
    #     cv2.imwrite(f'{save_path}/frame_{frame_num}_face.jpg', face)

    frame_num += 1

# Release the video capture object
cap.release()