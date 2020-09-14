# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/9 17:23
from utils.database.DBConnector import DBConnect

db = DBConnect()


def safe_execute(sql: str, val: tuple):
    """
    Usage: Input sql order and value, This functions will connect to
    database and finally close all reference to induce memory.

    :params sql: sql order in MySQL grammar
    :params val: value that need to input into database
    :return: return a tuple of result if no exceptions. Else return
    exceptions.
    """
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
