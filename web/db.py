import pyodbc


class ItemDatabase:
    def __init__(self):
        # self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-KTVBTD1H;DATABASE=WebTest;')
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-KTVBTD1H;DATABASE=Telemarketing_Center_DB;')
        self.cursor = self.conn.cursor()


    def get_items(self):

        item_dict_admin = []
        item_dict_user = []
        query_admin = "select Accounts.AccountID, Accounts.username, Accounts.password, Accounts.session_id, Accounts.room from Accounts where AccountID in (select Employees.AccountID from Employees );"
        query_users = "select Accounts.AccountID, Accounts.username, Accounts.password, Accounts.session_id, Accounts.room from Accounts where AccountID in (select Customers.AccountID from Customers );"

        self.cursor.execute(query_admin)
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["accountID"] = row[0]
            item_dict["login"] = row[1]
            item_dict["password"] = row[2]
            item_dict["cookie"] = row[3]
            item_dict["room"] = row[4]
            item_dict_admin.append(item_dict)

        self.cursor.execute(query_users)
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["accountID"] = row[0]
            item_dict["login"] = row[1]
            item_dict["password"] = row[2]
            item_dict["cookie"] = row[3]
            item_dict["room"] = row[4]
            item_dict_user.append(item_dict)
        return item_dict_admin, item_dict_user

    def put_item(self, cookie, login):
        query = f"update Accounts set session_id = '{cookie}' where username = '{login}'"
        self.cursor.execute(query)
        # завершение транзакции
        self.conn.commit()

    def put_room(self, login, room):
        query = f"update Accounts set room = '{room}' where username = '{login}'"
        self.cursor.execute(query)
        self.conn.commit()

    def delete_room(self, login):
        query = f"update Accounts set room = Null where username = '{login}'"
        self.cursor.execute(query)
        self.conn.commit()

    def get_news(self):
        news_list = []
        # query = f"select Bank_News.New, Bank_News.AccountID from Bank_News where AccountID in (select Customers.AccountID from Customers );"
        query = f"select Bank_News.New, Bank_News.AccountID from Bank_News;"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["new"] = row[0]
            item_dict["accountID"] = row[1]
            news_list.append(item_dict)
        return news_list

    def get_details(self):
        news_list = []
        # query = f"select * from Details where Details.AccountID in (select Customers.AccountID from Customers );"
        query = f"select * from Details;"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["Number"] = row[0]
            item_dict["Type"] = row[1]
            item_dict["Balance"] = row[2]
            item_dict["accountID"] = row[3]
            news_list.append(item_dict)
        return news_list



    def put_bill(self, ammount, date, detail,number):
        # query = f"update Bills set Date = '{date}', Amount = '{ammount}', Sent_to = '{number}'  where Number = '{detail}'"
        query = f"exec [WebTest].[dbo].[add_bill] @Date_ = '{date}', @Amount_ = '{ammount}', @Number_= '{detail}', @Sent_to_ = '{number}'"
        self.cursor.execute(query)
        self.conn.commit()


    def get_bill(self):
        news_list = []
        query = f"select Bills.Date, Bills.Amount,Bills.Number, Bills.Sent_to from Bills;"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["date"] = row[0]
            item_dict["amount"] = row[1]
            item_dict["number_ac"] = row[2]
            item_dict["taker"] = row[3]
            news_list.append(item_dict)
        return news_list
# db = ItemDatabase()
# # db.put_item(login = 'admin',cookie = 'afghfghfghdmin')

# res1, res2 = db.get_items()
# print(res1)
# print(res2)
