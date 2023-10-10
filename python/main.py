from telegram_extractor import extract_data_from_telegram
from face_cropper_cv2 import get_faces
import asyncio
import os

###################################################
###########Detailes for Telegram ##################
api_id = ""
api_hash = ''
phone_number = '+'
channel_username = '@'
###################################################

asyncio.run(extract_data_from_telegram(channel_username,api_id,api_hash,phone_number))
for downloaded_file in os.listdir("./temp"):
    get_faces(file_name=downloaded_file)