# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/11 9:25
from web.bin.database.SafeExecute import safe_execute


class UserHandler:
    def __init__(self):
        self._safe_execute = safe_execute

    def _get_all_user(self):
        """
        Alert: This method is design for testing.
        """
        sql = "SELECT * FROM USERS"
        val = ()
        result = self._safe_execute(sql, val)
        return result

    def get_user_by_keyword(self, **kwargs):
        if not kwargs:
            raise TypeError("get_user_by_keyword() missing required arguments")

        uid = kwargs.get("uid")
        if uid:
            sql = "SELECT * FROM USERS WHERE UID=%s"
            val = (uid,)
            results = self._safe_execute(sql, val)
            if results:
                return {"ok": True, "results": self._format_result(results)}
            return {"ok": False, "descriptions": "Empty result"}

        name = kwargs.get("name")
        if name:
            sql = "SELECT * FROM USERS WHERE NAME=%s"
            val = (name,)
            results = self._safe_execute(sql, val)
            if results:
                return {"ok": True, "results": self._format_result(results)}
            return {"ok": False, "descriptions": "Empty result"}

        permission = kwargs.get("permission")
        if permission:
            sql = "SELECT * FROM USERS WHERE PERMISSION=%s"
            val = (permission,)
            results = self._safe_execute(sql, val)
            if results:
                return {"ok": True, "results": self._format_result(results)}
            return {"ok": False, "descriptions": "Empty result"}

        raise TypeError("get_user_by_keyword() got unexpected arguments")

    def add_users(self, uid: int, name: str, permission: str):
        ALLOW_PERMISSION = ["admin", "manager"]
        if permission not in ALLOW_PERMISSION:
            raise TypeError("add_users() got unexpected permission: '%s'" % permission)

        sql = "INSERT INTO USERS (UID, NAME, PERMISSION) VALUES (%s, %s, %s)"
        val = (uid, name, permission)
        results = self._safe_execute(sql, val)
        if not isinstance(results, Exception):
            sql = "SELECT UID FROM USERS WHERE UID = %s"
            val = (uid,)
            results = self._safe_execute(sql, val)
            if results and results[0][0] == uid:
                return {"ok": True}

        return {"ok": False, "descriptions": results}

    def delete_user(self, uid):
        sql = "DELETE FROM USERS WHERE UID = %s"
        val = (uid, )
        result = self._safe_execute(sql, val)
        if not isinstance(result, Exception):
            return {"ok": True}
        return {"ok": False, "descriptions": result}

    def edit_user_info(self, uid, **kwargs):
        name = kwargs.get("name")
        permission = kwargs.get("permission")
        ALLOW_PERMISSION = ["admin", "manager"]
        if permission and permission not in ALLOW_PERMISSION:
            raise TypeError("edit_user_info() got unexpected permission: '%s'" % permission)

        if name and permission:
            sql = "UPDATE USERS SET NAME=%s, PERMISSION=%s WHERE UID=%s"
            val = (name, permission, uid)
        elif name:
            sql = "UPDATE USERS SET NAME=%s WHERE UID=%s"
            val = (name, uid)
        elif permission:
            sql = "UPDATE USERS SET PERMISSION=%s WHERE UID=%s"
            val = (permission, uid)
        else:
            raise TypeError("edit_user_info() need at least one argument but got none")

        result = self._safe_execute(sql, val)

        if not isinstance(result, Exception):
            return {"ok": True}

        return {"ok": False, "descriptions": result}

    @staticmethod
    def _format_result(results):
        formatted_list = []
        for result in results:
            UID, PERMISSION, NAME = result
            d = {"UID": UID, "PERMISSION": PERMISSION, "NAME": NAME}
            formatted_list.append(d)
        return formatted_list


if __name__ == '__main__':
    u = UserHandler()
    print(u.add_users(123, "test", "manager"))
