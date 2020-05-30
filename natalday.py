import telebot
from setting import bot, mlink, a_id1, a_id2
import requests
import json
import schedule
import time
from multiprocessing import Process

# Подключаемся к боту
bot_token = bot
bot = telebot.TeleBot(bot_token)


# Функция оповещения
def job():
        # Читаем данные с сервера
    response = requests.get(mlink, verify=False)
    todos = json.loads(response.text)

    # Заголовок сообщения
    # bot.send_message('708061023', 'Доброе утро! Информация о событиях на 05.05.2020')

    # print (todos["items"])

    if response.status_code != 404:
        for person in todos["items"]:
            # Отправим фото
            if person['photo']:
                resphoto = requests.get(person['photo'], verify=False)
                if resphoto.status_code != 404:
                    try:
                        bot.send_photo(person['user_id'], person['photo'])
                    except Exception as e:
                        bot.send_message(a_id1, 'Проблема с отправкой фото:' + str(e))
                        bot.send_message(a_id2, 'Проблема с отправкой фото:' + str(e))

            # Отправим текст
            try:
                bot.send_message(str(person['user_id']),
                                 str(person['name']) + chr(10) + chr(10) +
                                 str(person['position']) + chr(10) + chr(10) +
                                 'День рождения: ' + chr(10) +
                                 str(person['natalday']) + ' (' + str(person['age']) + ' лет)' + chr(10) +
                                 'тел: +' + str(person['phone'])
                                 )
            except Exception as e:
                bot.send_message(a_id1, 'Проблема с отправкой сообщения:' + str(e))
                bot.send_message(a_id2, 'Проблема с отправкой сообщения:' + str(e))
    else:
        bot.send_message(a_id1, 'Проблема с доступом к сервису оповещений natalday_bot')
        bot.send_message(a_id2, 'Проблема с доступом к сервису оповещений natalday_bot')


# Подключаем планировщик повторений    
#schedule.every().day.at("05:00").do(job)

@bot.message_handler(commands=['start'])
def send_text(message):
    bot.send_message(message.chat.id, "Ваш ID: " + str(message.chat.id) + ". Сообщите его администратору бота.")


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

#Включение бота на прием сообщений
# обернуто в try, потому что если Telegram сервер станет недоступен, возможен крэш
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        # повторяем через 15 секунд в случае недоступности сервера Telegram
        time.sleep(15)
