# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/9 17:23
from web.bin.database.DBConnector import DBConnect

db = DBConnect()


def safe_execute(sql: str, val: tuple):
    db_ref = db.get_db()
    cur = db.get_cur()
    try:
        cur.execute(sql, val)
        db_ref.commit()
        return cur.fetchall()
    except Exception as e:
        db_ref.rollback()
        return e
    finally:
        cur.close()
