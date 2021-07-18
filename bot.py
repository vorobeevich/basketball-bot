from findplaces import find_places
from telebot import *

token = ""
with open("token.txt") as f:
    token = f.read()

import telebot;
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Чтобы узнать список команд для работы с ботом, напиши /help!")
    elif message.text == "/get_courts":
        text = "Сейчас ты получишь ближайшие баскетбольные площадки! Надо только получить твою геолокацию"
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        key = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(key); 
        bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши /get_courts")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(content_types=["location"])
def handle_loc(message):
    places = find_places(5, "data work/data/database.csv", message.location.latitude, message.location.longitude)
    texts = []
    photos = []
    locations = []

    for index, place in places:
        text = "Название площадки: "
        text += place["name"] + "\n"
        text += "Адрес площадки: "
        text += place["adress"] + "\n"
        texts.append(text)
        if place["photo_id"] != "0":
            photos.append("data work/data/photos/" + str(index) + ".png")
        else:   
            photos.append("0")
        locations.append((place["latitude"], place["longitude"]))
    for i in range(len(places)):
        text, photo = texts[i], photos[i]  
        bot.send_message(message.from_user.id, text)
        if photo != "0":
            bot.send_photo(message.from_user.id, photo=open(photo, 'rb'))
        else:
            bot.send_message(message.from_user.id, "Отправляйся на эту площадку и делай фото, тогда оно появится в Google Maps!")
        bot.send_location(message.from_user.id, locations[i][0], locations[i][1])
    if len(places) == 0:
        bot.send_message(message.from_user.id, "К сожалению, рядом с тобой нет баскетбольных площадок! А что вероятнее, их еще не занесли в Google Maps!")        


bot.polling(none_stop=True, interval=0)