from datetime import (
	datetime, 
	timedelta
)
from telethon import (
    TelegramClient,
    errors, 
    events,
	types
)
import os.path

async def  download(message, date, type, postfix):
    file_name = "{}_{}.{}".format(type,date, postfix)
    file_path = "./{}/{}".format("temp",file_name)
    if not os.path.isfile(file_path):
        await message.download_media( file_path)
        print(message.sender.username, message.media)


async def extract_data_from_telegram(channel_username,api_id,api_hash,phone_number):
    async with TelegramClient("testsession", api_id, api_hash) as client:
        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            try:
                client.sign_in(phone_number, input('Enter the code: '))
            except errors.SessionPasswordNeededError:
                client.sign_in(password=input('Password: '))

        async for message in client.iter_messages(channel_username):
            print(message.sender.username, message.text, message.date)
            if message.media is not None:
                date = message.date.strftime("%Y-%m-%d_%H-%M-%S")
                if message.photo != None:
                    type = "photo"
                    postfix = "png"
                    await download(message=message, type=type, date= date, postfix=postfix)
                elif str.split(message.media.document.mime_type, "/")[1] == "mp4":
                    mime_type = str.split(message.media.document.mime_type, "/")
                    type = mime_type[1]
                    postfix = mime_type[1]
                    await download(message=message, type=type, date= date, postfix=postfix)
                else:
                    print("File type: {} is not supported".format(message.media.document.mime_type))


