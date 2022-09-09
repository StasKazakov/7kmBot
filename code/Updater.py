# This modul update shops filеs.

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
sheet = shop.active
list_updates = []

dict_shop = {}
for namb in range(1, sheet.max_row + 1):
    key = (sheet['A' + str(namb)].value)
    dict_shop[key] = (sheet['B' + str(namb)].value)
list_keys_dict_shop = list(dict_shop.keys())

count = 0
while True:
    try:
        for title in list_keys_dict_shop:
            if title not in list_updates:
                print(title)

                with TelegramClient('name', api_id, api_hash) as client:
                    result = client(GetDialogsRequest(
                        offset_date=None,
                        offset_id=0,
                        offset_peer='username',
                        limit=500,
                        hash=0,
                    ))

                    # Download last 100 photo frome chenal

                    for chat in result.chats:
                        # print(chat)

                        if chat.id == title:
                            messages = client.get_messages(
                                chat,
                                limit=100,
                                filter=InputMessagesFilterPhotos
                            )

                            for message in tqdm(messages):
                                message.download_media('../photo/' + dict_shop.get(title) + '/')
                                path_shop = '../shops/'
                                path_img = '../photo/' + dict_shop.get(title) + '/'
                                shop_file = open(path_shop + dict_shop.get(title) + '.txt', 'a', encoding='utf-8')
                                list_img = os.listdir(path_img)
                                current_file = 0

                                while current_file < len(list_img):
                                    hash = CalcImageHash(path_img + list_img[current_file])
                                    with open(path_shop + dict_shop.get(title) + '.txt', 'r', encoding='utf-8') as f:
                                        hash_list = f.read().splitlines()
                                        if hash not in hash_list:
                                            shop_file.write(hash + '\n')
                                    current_file += 1
                                shop_file.close()
                    #shutil.rmtree(path_shop + dict_shop.get(title) + '/')
                    list_updates.append(title)
                    print(f'{dict_shop.get(title)} is update!')
                    time.sleep(5)
                    count += 1

    except:
        print('Ошибка')
        list_updates.append(title)

# Delete all folders with foto

# with open("../catalog.txt", encoding='utf-8') as f:
#     clist = f.read().splitlines()

# current_folder = 0
# while current_folder < len(clist):
#     dir_path = '../photo/'
#     shutil.rmtree(dir_path + clist[current_folder] + '/')
#     current_folder += 1


list_updates = []
time.sleep(72000)

