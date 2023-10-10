import cv2
import os
import numpy as np
from pathlib import Path
from ultralytics import YOLO

from skimage.metrics import structural_similarity as ssim

def calculate_similarity(image1, image2):
    # Convert the images to grayscale
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Compute SSIM between two images
    return ssim(image1_gray, image2_gray)

def handle_video(full_path,prefix, similarity_threshold, model):
    frame_num = 0
    prev_faces = []
    cap = cv2.VideoCapture(full_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_num, prev_faces = handle_frame(frame=frame, prefix=prefix,
                                similarity_threshold=similarity_threshold, 
                                frame_num=frame_num, model=model, prev_faces=prev_faces)

    cap.release()

def handle_frame(frame, prefix, similarity_threshold, model, frame_num=0, prev_faces=[]):
    results = model(frame, save=True, verbose=True)
    boxes = results[0].boxes.data.cpu().numpy()

    current_faces = []

    for i, (x1, y1, x2, y2, conf, cls_id) in enumerate(boxes):
        if(conf.T > 0.75):
            cropped_box = frame[int(y1):int(y2), int(x1):int(x2)]
            current_faces.append(cropped_box)
            should_save = True

            for prev_face in prev_faces:
                prev_face_resized = cv2.resize(prev_face, (cropped_box.shape[1], cropped_box.shape[0]))
                similarity = calculate_similarity(prev_face_resized, cropped_box)
                if similarity < similarity_threshold:
                    should_save = False
                    break

            if should_save:
                face_file_path = os.path.join("./faces/", f"face_{prefix}_{frame_num}.jpg")
                imgCrop = cv2.resize(cropped_box, (180,227))
                cv2.imwrite(face_file_path, imgCrop)
            
            frame_num += 1

    prev_faces = current_faces  # Update previous frame faces
    return frame_num, prev_faces

#def main(dir_path='./temp/', file_name="photo_2023-10-10_05-36-10.png"):
def get_faces(dir_path='./temp/', file_name="mp4_2023-10-10_08-35-26.mp4"):
    model = YOLO(f'./model/yolov8n-face.pt', task="detect")
    similarity_threshold = 0.95  # Set a high threshold. Closer to 1 means stricter similarity.

    type= str.split(file_name, ".")[-1:][0]
    full_path =  dir_path + file_name
    prefix = str.replace(file_name, ".", "_")

    if type == "png":
        frame =cv2.imread(full_path)
        handle_frame(frame=frame, prefix=prefix, model=model, similarity_threshold=similarity_threshold)
    elif type == "mp4":
        handle_video(full_path, prefix=prefix, model=model, similarity_threshold=similarity_threshold)

    
# get_faces()
