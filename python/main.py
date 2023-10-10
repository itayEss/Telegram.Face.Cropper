from telegram_extractor import extract_data_from_telegram
# from face_cropper_cv2 import get_faces
from face_cropper3_yolo import get_faces
import asyncio
import os

###################################################
###########Detailes for Telegram ##################
api_id = os.environ['TELEGRAM_APP_ID']
api_hash = os.environ['TELEGRAM_APP_HASH']
phone_number = os.environ['TELEGRAM_PHONE_NUMBER']
channel_username = os.environ['CHANNEL_TO_USE']
###################################################

asyncio.run(extract_data_from_telegram(channel_username,api_id,api_hash,phone_number))
for downloaded_file in os.listdir("./temp"):
    get_faces(file_name=downloaded_file)