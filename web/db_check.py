from db import ItemDatabase
from flask import request
import bcrypt
class Item:

    def __init__(self):
        self.db1 = ItemDatabase()

    def check(self, req):
        result = {}
        db_items1, db_items2 = self.db1.get_items()
        if req == "POST":
            user_log = request.form["nm"]
            user_pass = request.form["ps"]
            bytes = user_pass.encode('utf-8')
            for i in db_items1:
                if i["login"] == user_log and bcrypt.checkpw(bytes, i["password"].encode('utf-8')):
                    result["worker"] = user_log
            for i in db_items2:
                if i["login"] == user_log and bcrypt.checkpw(bytes, i["password"].encode('utf-8')):
                    result['user'] = user_log
            return result

