import cv2
import os

def handle_frame(frame, prefix, face_id=0):
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    # Initialize face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    for (x, y, w, h) in faces:
        face_image = frame[y:y+h, x:x+w]
        face_file_path = os.path.join("./faces/", f"face_{prefix}_{face_id}.jpg")
        imgCrop = cv2.resize(face_image, (180,227))
        cv2.imwrite(face_file_path, imgCrop)
        face_id += 1
        
    return face_id

def save_faces_from_video(video_path ,prefix):
    cap = cv2.VideoCapture(video_path)
    face_id = 0

    while True:
        end_of_video, frame = cap.read()
        if not end_of_video:
            break
        face_id = handle_frame(frame, prefix, face_id)

    cap.release()

#def get_faces(dir_path='./temp/', file_name="mp4_2023-10-10_08-35-26.mp4"):
def get_faces(dir_path='./temp/', file_name="photo_2023-10-10_05-36-10.png"):
    type= str.split(file_name, ".")[-1:][0]
    full_path =  dir_path + file_name
    prefix = str.replace(file_name, ".", "_")

    if type == "png":
        frame =cv2.imread(full_path)
        handle_frame(frame=frame, prefix=prefix)
    elif type == "mp4":
        save_faces_from_video(full_path, prefix=prefix )
