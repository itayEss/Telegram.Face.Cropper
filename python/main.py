
from telegram_extractor import extract_data_from_telegram
from face_cropper_cv2 import get_faces
import asyncio
import os

###################################################
###########Detailes for Telegram ##################
api_id = "24817662"
api_hash = 'f887bd8bd39fa28a379b63375653146c'
phone_number = '+972528022557'
channel_username = '@isrsuperbot'
###################################################

asyncio.run(extract_data_from_telegram(channel_username,api_id,api_hash,phone_number))
for downloaded_file in os.listdir("./temp"):
    get_faces(file_name=downloaded_file)