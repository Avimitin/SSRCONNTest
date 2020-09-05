# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/8/31 16:47
from web.bin.database import DBConnector

db = DBConnector.DBConnect()
cur = db.get_cur()
with open("static/CreateServerDB.sql", "r", encoding="utf-8") as sql_file:
    lines = sql_file.readline()

for line in lines:
    cur.execute(line)

db.close_connect()
