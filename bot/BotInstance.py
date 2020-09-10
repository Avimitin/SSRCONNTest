# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/10 16:10
import telebot
import json

with open("BotConfig/botToken.json", "r", encoding="utf-8") as conf_file:
    TOKEN = json.load(conf_file)["TOKEN"]

with open("BotConfig/user.json", "r", encoding="utf-8") as user_file:
    ALLOW_USERS = json.load(user_file)["ALLOW_USER"]

for user in ALLOW_USERS:
    if user["Permission"] == "admin":
        ADMIN = user["ID"]
        break

BOT = telebot.TeleBot(TOKEN)


if __name__ == '__main__':
    with open("../web/test/test.png", "rb") as p:
        BOT.send_photo(ADMIN, p)
