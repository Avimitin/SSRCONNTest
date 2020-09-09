# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/8 11:27
from web.bin.database import SafeExecute


class SubHandler:
    def __init__(self):
        self._safe_execute = SafeExecute.safe_execute

    def get_sub_link_by_name(self, name):
        sql = "SELECT * FROM subscriptions WHERE NAME=%s"
        val = (name,)
        results = self._safe_execute(sql, val)
        if results:
            response = {"ok": True, "result": []}
            for result in results:
                ID, NAME, LINK = result
                response["result"].append({"ID": ID, "NAME": NAME, "LINK": LINK})
            return response
        return False

    def add_new_subscriptions(self, name, link):
        sql = "INSERT INTO subscriptions (Name, SubLink) VALUES (%s, %s)"
        val = (name, link)
        self._safe_execute(sql, val)
        sql = "SELECT * FROM subscriptions WHERE NAME = %s"
        val = (name,)
        result = self._safe_execute(sql, val)
        return {"ok": False} if not result else {"ok": True}


if __name__ == '__main__':
    s = SubHandler()
    print(s.get_sub_link_by_name("oxygenproxy"))
