from db import ItemDatabase



class Coc:
    def __init__(self):
        self.db2 = ItemDatabase()

    def check(self,cookie):
        result = {}
        db_items1, db_items2 = self.db2.get_items()
        for item in db_items1:
            if item["cookie"] == cookie:
                user = item["login"]
                result["worker"] = user
        for item in db_items2:
            if item["cookie"] == cookie:
                user = item["login"]
                result["user"] = user
        return result
