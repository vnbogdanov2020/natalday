# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import telebot
from setting import bot, mlink#, a_id1, a_id2
import requests
import json
import schedule
import time


#Подключаемся к боту       
bot_token = bot
bot = telebot.TeleBot(bot_token)
'''
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=1)
keyboard.row('Очистить сообщения')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в систему оповещения', reply_markup=keyboard)  

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'очистить сообщения':
        for numid in range(message.message_id-10,message.message_id-1):
            bot.delete_message(message.chat.id, numid)
        
   
'''     

#Функция оповещения
def job():
    #Читаем данные с сервера
    response = requests.get(mlink, verify=False)
    todos = json.loads(response.text)
    
    
    #Заголовок сообщения
    #bot.send_message('708061023', 'Доброе утро! Информация о событиях на 05.05.2020')
    
    #print (todos["items"])
    
    if response.status_code != 404:    
        for person in todos["items"]:
                #Отправим фото
                if person['photo']:
                    resphoto = requests.get(person['photo'], verify=False)
                    if resphoto.status_code != 404:
                        bot.send_photo(person['user_id'],person['photo'])
                        
                #Отправим текст
                bot.send_message(person['user_id'], 
                                 person['name']+chr(10)+chr(10)+
                                 person['position']+chr(10)+chr(10)+
                                 'День рождения: '+chr(10)+
                                 person['natalday']+' ('+person['age']+' лет)'+chr(10)+
                                 'тел: +'+person['phone']
                                 )
    else:
         bot.send_message(a_id1,'Проблема с доступом к сервису оповещений natalday_bot')
         bot.send_message(a_id2,'Проблема с доступом к сервису оповещений natalday_bot')

# Подключаем планировщик повторений    
schedule.every().day.at("22:52").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

bot.polling()