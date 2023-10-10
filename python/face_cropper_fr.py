import face_recognition

image = face_recognition.load_image_file("./temp/photo_2023-10-10_05-36-10.png")
face_locations = face_recognition.face_locations(image)