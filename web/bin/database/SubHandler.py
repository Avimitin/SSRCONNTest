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
            response = {"ok": True, "results": []}
            for result in results:
                ID, NAME, LINK = result
                response["results"].append({"ID": ID, "NAME": NAME, "LINK": LINK})
            return response
        return {"ok": False, "descriptions": "Empty result"}

    def add_new_subscriptions(self, name, link):
        sql = "INSERT INTO subscriptions (Name, SubLink) VALUES (%s, %s)"
        val = (name, link)
        results = self._safe_execute(sql, val)
        if not isinstance(results, Exception):
            sql = "SELECT * FROM subscriptions WHERE NAME = %s"
            val = (name,)
            results = self._safe_execute(sql, val)
            if results:
                return {"ok": True}
            return {"ok": False, "descriptions": "Fail to insert into table"}

        return {"ok": False, "descriptions": results}

    def edit_subscriptions(self, name, link):
        sql = "UPDATE subscriptions SET LINK=%s WHERE NAME=%s"
        val = (name, link)
        results = self._safe_execute(sql, val)

        if not isinstance(results, Exception):
            sql = "SELECT * FROM subscriptions WHERE NAME = %s"
            val = (name, )
            results = self._safe_execute(sql, val)
            if results:
                f_list = []
                for result in results:
                    ID, NAME, LINK = result
                    f_list.append({"ID": ID, "NAME": NAME, "LINK": LINK})
                return {"ok": True, "NewResult": f_list}

            return {"ok": False, "descriptions": "Fail to update subs info"}

        return {"ok": False, "descriptions": results}

    def delete_link(self, name, **kwargs):
        ID = kwargs.get("id")
        if ID:
            sql = "DELETE FROM subscriptions WHERE NAME = %s AND ID = %s"
            val = (name, ID)
        else:
            sql = "DELETE FROM subscriptions WHERE NAME = %s"
            val = (name, )
        results = self._safe_execute(sql, val)

        if isinstance(results, Exception):
            return {"ok": False, "descriptions": Exception}

        return {"ok": True}


if __name__ == '__main__':
    s = SubHandler()
    print(s.get_sub_link_by_name("oxygenproxy"))
