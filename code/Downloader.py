# This module downloads foto in folder on server

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from tqdm import tqdm
from telethon.tl.types import InputMessagesFilterPhotos
import openpyxl
import os
from Functions import CalcImageHash
import shutil
from Variables import api_i, api_h
import time

api_id = api_i
api_hash = api_h

shop = openpyxl.open("../shops.xlsx", read_only=True)
sheet = shop['add']
list_downloads = []

dict_shop = {}
for namb in range(1, sheet.max_row + 1):
    key = (sheet['A' + str(namb)].value)
    dict_shop[key] = (sheet['B' + str(namb)].value)
list_keys_dict_shop = list(dict_shop.keys())

for title in list_keys_dict_shop:
    if title not in list_downloads:
        print(title)

        with TelegramClient('name', api_id, api_hash) as client:
            result = client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer='username',
                limit=500,
                hash=0,
            ))

# Download last 5000 photo frome chenal

            for chat in result.chats:
                #print(chat)

                if chat.id == title:
                    messages = client.get_messages(
                        chat,
                        limit=5000,
                        filter=InputMessagesFilterPhotos
                    )

                    for message in tqdm(messages):
                        message.download_media('../photo/' + dict_shop.get(title) + '/')
       