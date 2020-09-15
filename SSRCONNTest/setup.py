# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/8/31 16:47
from utils.TokenGenerator import Generator
from utils.database import DBConnector
import configparser

def set_database():
    db = DBConnector.DBConnect()
    cur = db.get_cur()
    with open("static/CreateServerDB.sql", "r", encoding="utf-8") as sql_file:
        lines = sql_file.readline()

    for line in lines:
        cur.execute(line)

    db.close_connect()

def set_start_up_token():
    config = configparser.ConfigParser()
    config.read("./web/config/settings.ini")
    g = Generator.TokenGenerator()
    StartUpToken = g.get_salt(16)
    config["Privacy"]["StartUpToken"] = StartUpToken
    with open("./web/config/settings.ini", "w") as configfile:
        config.write(configfile)
    print("=====================================================================")
    print("初次设定密钥已经生成完毕，请谨慎保存。")
    print("请将 token 复制到 http://host:port/api/v1/verify 验证管理员身份。\n")
    print("StartUpToken: {}".format(StartUpToken))
    print("=====================================================================")

if __name__ == "__main__":
    set_start_up_token()