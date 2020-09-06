# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/9/2 17:36
# Program to handle all the data in table result
from web.bin.database.DBConnector import DBConnect


class ResultHandler:
    """
    Package all handler method to decrease database connect times
    """
    def __init__(self):
        """
        Database Connector Initialize
        """
        self.db = DBConnect()

    def _get_all_rows_in_result(self):
        """
        Get all rows in table !!!FOR TESTING!!! Don't use it.
        :return fetchall(): return searching result if no Exception else return Exception
        """
        sql = "SELECT * FROM `result`"
        cur = self.db.get_cur()
        try:
            cur.execute(sql)
            results = cur.fetchall()
            result_list = []
            for row in results:
                result_list = self._format_result_all(row)
            return result_list
        except Exception as e:
            return e
        finally:
            cur.close()

    def get_result_by_keyword(self, **kwargs):
        """
        get result by name
        :param name: A string object that contain name of the result
        :param time: A int object about when the result generate
        :return:
            Return result if no exception, else return exception.
            Result is a list that contain many dict object about data.
            For Example:
                >> test = ResultHandler()
                >> print(test.get_result_by_keyword("test"))
                [{'ID': 1, 'NAME': 'test', 'PLACE': 'F:/dev', 'TIME': 114514}]
            If the result doesn't exist, this will return a empty list.
        """
        if kwargs == {}:
            raise SyntaxError("You don't input any args")
        if "name" in kwargs.keys() and "time" in kwargs.keys():
            sql = "SELECT * FROM result WHERE NAME=%s AND TIME=%s"
            val = (kwargs["name"], kwargs["time"])
        elif "name" in kwargs.keys():
            sql = "SELECT * FROM `result` WHERE NAME=%s"
            val = (kwargs["name"],)
        else:
            sql = "SELECT * FROM result WHERE TIME=%d"
            val = (kwargs["time"],)
        results = self._safe_execute(sql, val)
        if results is not Exception:
            result_list = []
            for row in results:
                result_list.append(self._format_result_all(row))
            return result_list
        else:
            return results

    def add_new_result(self, name, place, time):
        sql = "INSERT INTO result (NAME, PLACE, TIME) VALUES (%s, %s, %s)"
        val = (name, place, time)
        result = self._safe_execute(sql, val)
        if result == ():
            sql = "SELECT * FROM result WHERE NAME=%s AND PLACE=%s AND TIME=%s"
            result = self._safe_execute(sql, val)
            if result != ():
                return {"OK": True}
            else:
                return {"OK": False}

    @staticmethod
    def _format_result_all(row):
        ID, NAME, PLACE, TIME = row
        format_data = {
            "ID": ID,
            "NAME": NAME,
            "PLACE": PLACE,
            "TIME": TIME
        }
        return format_data

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


if __name__ == '__main__':
    test = ResultHandler()
    print(test.add_new_result("test4", "FFFF", 11451400))