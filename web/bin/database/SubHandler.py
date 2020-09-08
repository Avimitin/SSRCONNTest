# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/8 11:27
from web.bin.database import DBConnector


class SubHandler:
    def __init__(self):
        self.db = DBConnector.DBConnect()

    def get_sub_link_by_name(self, name):
        sql = "SELECT * FROM subscriptions WHERE NAME=%s"
        val = (name,)
        self._safe_execute(sql, val)

    def add_new_subscriptions(self, name, link):
        sql = "INSERT INTO subscriptions (Name, SubLink) VALUES (%s, %s)"
        val = (name, link)
        self._safe_execute(sql, val)

    def _safe_execute(self, sql: str, val: tuple):
        db = self.db.get_db()
        cur = self.db.get_cur()
        try:
            cur.execute(sql, val)
            db.commit()
            return cur.fetchall()
        except Exception as e:
            db.rollback()
            return e
        finally:
            cur.close()

