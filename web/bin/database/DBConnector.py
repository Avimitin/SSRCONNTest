# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/8/30 16:31
import pymysql
from configs import db_cfg

DATABASE_CFG = db_cfg.CONFIG


class DBConnect:
    def __init__(self):
        self.database = pymysql.connect(
            host=DATABASE_CFG["host"],
            user=DATABASE_CFG["user"],
            password=DATABASE_CFG["password"],
            database=DATABASE_CFG["database"]
        )

    def get_db(self):
        return self.database

    def get_cur(self):
        return self.database.cursor()

    def close_connect(self, curIsOpen=False):
        if curIsOpen:
            self.cur.close()
        self.database.close()


if __name__ == '__main__':
    pass
