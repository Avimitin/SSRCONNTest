# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/10 16:10
import telebot
import json
from .BotConfig import conf

TOKEN = conf.BOT_TOKEN
ALLOW_USERS = conf.ALLOW_USERS

for user in ALLOW_USERS:
    if user["Permission"] == "admin":
        ADMIN = user["ID"]
        break

BOT = telebot.TeleBot(TOKEN)


if __name__ == '__main__':
    BOT.polling(none_stop=True)
