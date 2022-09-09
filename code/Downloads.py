# This module downloads foto in folder on server
from Variables import api_i, api_h

api_id = api_i
api_hash = api_h

from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from tqdm import tqdm
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterVideo
import openpyxl


with TelegramClient('name', api_id, api_hash) as client:
    result = client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer="username",
        limit=500,
        hash=0,
    ))

    shop = openpyxl.open("../shops.xlsx", read_only=True)
    sheet = shop.active
    sh_lst = [] #shoplist
    for namb in range(1, sheet.max_row + 1):
        sh_lst.append(sheet['A' + str(namb)].value)
    #print(sh_lst)

    for title in sh_lst:
        for chat in result.chats:
            print(chat)

            if chat.title == title:
                messages = client.get_messages(chat, limit=5000, filter=InputMessagesFilterPhotos)

                for message in tqdm(messages):
                    message.download_media('../photo/' + title + '/')
