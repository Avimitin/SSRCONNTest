# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/10 16:10
import telebot
import configparser
import os
print(os.getcwd())

config = configparser.ConfigParser()
config.read("./BotConfig/conf.ini")

TOKEN = config["BOT"]["TOKEN"]
ADMIN = config["ADMIN"]["ID"]

BOT = telebot.TeleBot(TOKEN)
