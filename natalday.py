
import telebot
from setting import bot, mlink#, a_id1, a_id2
import requests
import json
import schedule
import time
from multiprocessing import Process

#Подключаемся к боту
bot_token = bot
bot = telebot.TeleBot(bot_token)

# Обработка сообщений

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
schedule.every().day.at("20:00").do(job)

@bot.message_handler(content_types=['text'])
def send_text(message):

    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Ваш ID: " + str(message.chat.id)+". Сообщите его администратору бота.")

# это функция отправки сообщений по таймеру
def check_send_messages():
    while True:
        # ваш код проверки времени и отправки сообщений по таймеру
        # пауза между проверками, чтобы не загружать процессор
        schedule.run_pending()
        time.sleep(60)
    # а теперь запускаем проверку в отдельном потоке

p1 = Process(target=check_send_messages, args=())
p1.start()

'''''
while True:
    schedule.run_pending()
    time.sleep(1)
'''''
# а это включение бота на прием сообщений
# обернуто в try, потому что если Telegram сервер станет недоступен, возможен крэш
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        # повторяем через 15 секунд в случае недоступности сервера Telegram
        time.sleep(15)
#bot.polling()