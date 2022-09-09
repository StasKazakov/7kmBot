import telebot
import cv2
import os
import io
from Functions import CalcImageHash
from telebot import types
from Variables import bot_token, mess, mess2, instruction, contacts

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, mess, parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    website_key = types.KeyboardButton('Сайт')
    shops_key = types.KeyboardButton('Виробники')
    info_key = types.KeyboardButton('Інструкція')
    contact_key = types.KeyboardButton('Контакти')
    markup.add(website_key, shops_key, info_key, contact_key)
    bot.send_message(message.chat.id, mess2, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Сайт':
        bot.send_message(message.chat.id, "http://7kmbot.tilda.ws")
    elif message.text == 'Виробники':
        with open("../catalog.txt", encoding='utf-8') as f:
            shop_list = f.read().splitlines()
        shop_list.sort()
        list_mess = "\n".join(shop_list)
        bot.send_message(message.chat.id, f'<b>Доступні виробники:</b>\n{list_mess}', parse_mode='html')
    elif message.text == 'Інструкція':
        bot.send_message(message.chat.id, instruction, parse_mode='html')
    elif message.text == 'Контакти':
        bot.send_message(message.chat.id, contacts)



@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:

        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = '../' + file_info.file_path;
        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
           etalon_hesh = CalcImageHash('../' + file_info.file_path)
           simg = []
           path = '../'
           with open(path + "catalog.txt") as f:
               clist = f.read().splitlines()
           current_folder = 0
           manufacturer = None

           while current_folder < len(clist):
               pathn = path + 'shops/' + '/'
               file = open(pathn + clist[current_folder] + '.txt', "r+")

               y = 0
               with io.open(pathn + clist[current_folder] + '.txt') as file:
                   for line in file:
                       if etalon_hesh in line:
                           manufacturer = (clist[current_folder])
                           bot.reply_to(message, f'Виробник: <b>{manufacturer}</b>\nПеревірено <b>{sum(simg)}</b> фото.', parse_mode='html')
                           break
                       else:
                           y = y + 1
               simg.append(y)
               current_folder += 1
        if manufacturer == None:
            bot.reply_to(message, f'Цього фото не має в базі.🤷‍♀\nПеревірено <b>{sum(simg)}</b> фото.', parse_mode='html')


    except Exception as e:
        bot.reply_to(message,e)


bot.polling(none_stop=True)
