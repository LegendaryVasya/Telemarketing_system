import tkinter as tk
from tkinter import messagebox
import webbrowser
import pyodbc
from tkinter import *
import re
import datetime


class NewWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title('Union Bank')
        self.window.geometry("400x200")
        # set minimum window size value
        self.window.minsize(400, 200)
        # set maximum window size value
        self.window.maxsize(400, 200)
        screen_width = self.window.winfo_screenwidth()  # Width of the screen
        screen_height = self.window.winfo_screenheight()
        x = (screen_width / 2) - (400 / 2)
        y = (screen_height / 2) - (200 / 2)
        self.window.geometry('%dx%d+%d+%d' % (400, 200, x, y))

def Surveys_button1():
        add_surveys('example','example@example.com','Вопрос','Как дела?','Yes','2023-05-17 05:42:37')



def Surveys_button2():
    w2.window.withdraw()
    w4 = NewWindow()
    frame = tk.Frame(w4.window)
    frame.pack(pady=70)

    enabled = IntVar()
    label = Label(frame, text="Сортировка по")
    entry_f = Entry(frame)


    entry_f.config(state="disabled")
    label.grid(row=0, column=1, padx=(0,40))
    entry_f.grid(row=1, column=1, padx=10)

    def check_box():
        if enabled.get() == 1:
            entry_f.config(state="normal")
            entry_f.grid(row=1, column=1, padx=10)
            button1 = Button(frame, text="Найти", command=search2, height=2, width=20)
            button1.grid(row=0, column=0, padx=(0, 10))
            # получаю значения

        else:
            entry_f.config(state="disabled")
            entry_f.grid(row=1, column=1, padx=10)
            button1 = Button(frame, text="Найти", command=search, height=2, width=20)
            button1.grid(row=0, column=0, padx=(0, 10))
    enabled_checkbutton = Checkbutton(frame, text="Включить", variable=enabled, command=check_box)


    def close_user_rights_window():
        w4.window.destroy()
        w2.window.deiconify()

    w4.window.protocol("WM_DELETE_WINDOW", close_user_rights_window)

    def search2():

        entry_val = entry_f.get()

        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-KTVBTD1H;DATABASE=Telemarketing_Center_DB;')
        cursor = conn.cursor()

        sql = """\
                    SET NOCOUNT ON;
                    DECLARE @RC int;
                    EXEC @RC = [Telemarketing_Center_DB].[dbo].[sort_surveys] ?;
                    SELECT @RC AS rc;
                    """
        values = (entry_val)
        cursor.execute(sql, values)
        rc = cursor.fetchval()


        if rc == 1:
            messagebox.showerror("Error", "Такого стобца нет")
            cursor.close()
            conn.close()
        else:
            query = f"exec [Telemarketing_Center_DB].[dbo].[sort_surveys] @table_name = {entry_val}"
            cursor.execute(query)

            results = cursor.fetchall()

            list_ = []
            for row in results:
                item_dict = {}
                item_dict["Survey_id"] = row[0]
                item_dict["Customer_id"] = row[1]
                item_dict["Date"] = row[2]
                item_dict["Type_of_deal"] = row[3]
                item_dict["deal"] = row[4]
                item_dict["suggection"] = row[5]
                list_.append(item_dict)



            w6 = NewWindow()
            w6.window.geometry("1200x720")
            # set minimum window size value
            w6.window.minsize(1200, 700)
            # set maximum window size value
            w6.window.maxsize(1200, 700)
            screen_width = w6.window.winfo_screenwidth()  # Width of the screen
            screen_height = w6.window.winfo_screenheight()
            x = (screen_width / 2) - (1200 / 2)
            y = (screen_height / 2) - (700 / 2)
            w6.window.geometry('%dx%d+%d+%d' % (1200, 700, x, y))
            # frame_ = tk.Frame(w5.window)
            # frame_.pack(pady=10)
            list = Listbox(w6.window, height=10, width=197)
            list.pack(side=LEFT, fill=BOTH)
            scroll_bar = Scrollbar(w6.window)
            scroll_bar.pack(side=RIGHT, fill=BOTH)
            for line in list_:
                list.insert(END, f"SurveysID: {line['Survey_id']}; CustomerID: {line['Customer_id']}; Date: {line['Date']}; Type_of_deal: {line['Type_of_deal']}; Deal: {line['deal']}; Suggestions: {line['suggection']}")

            list.config(yscrollcommand=scroll_bar.set)
            scroll_bar.config(command=list.yview)

            cursor.close()
            conn.close()
            entry_f.delete(0, 'end')




    def search():
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-KTVBTD1H;DATABASE=Telemarketing_Center_DB;')
        cursor = conn.cursor()

        cursor.execute(f"EXEC [Telemarketing_Center_DB].[dbo].[select_surveys]")


        results = cursor.fetchall()


        list_ = []
        for row in results:
            item_dict = {}
            item_dict["Survey_id"] = row[0]
            item_dict["Customer_id"] = row[1]
            item_dict["Date"] = row[2]
            item_dict["Type_of_deal"] = row[3]
            item_dict["deal"] = row[4]
            item_dict["suggection"] = row[5]
            list_.append(item_dict)

        w5 = NewWindow()
        w5.window.geometry("1200x720")
        # set minimum window size value
        w5.window.minsize(1200, 700)
        # set maximum window size value
        w5.window.maxsize(1200, 700)
        screen_width = w5.window.winfo_screenwidth()  # Width of the screen
        screen_height = w5.window.winfo_screenheight()
        x = (screen_width / 2) - (1200 / 2)
        y = (screen_height / 2) - (700 / 2)
        w5.window.geometry('%dx%d+%d+%d' % (1200, 700, x, y))
        # frame_ = tk.Frame(w5.window)
        # frame_.pack(pady=10)
        list = Listbox(w5.window, height = 10, width = 197)
        list.pack(side=LEFT, fill=BOTH)
        scroll_bar = Scrollbar(w5.window)
        scroll_bar.pack(side = RIGHT, fill = BOTH)
        for line in list_:
            list.insert(END, f"SurveysID: {line['Survey_id']}; CustomerID: {line['Customer_id']}; Date: {line['Date']}; Type_of_deal: {line['Type_of_deal']}; Deal: {line['deal']}; Suggestions: {line['suggection']}")

        list.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=list.yview)



    button1 = Button(frame, text="Найти", command=search, height=2, width=20)
    button1.grid(row=0, column=0, padx=(0, 10))

    enabled_checkbutton.grid(row=1, column=0)
def Surveys():
    w.window.withdraw()
    global w2
    w2 = NewWindow()
    button_frame = tk.Frame(w2.window)
    button_frame.pack(pady=70)
    button1 = tk.Button(button_frame, text="Добавить", command=add_surveys_window, height=2, width=20)
    button2 = tk.Button(button_frame, text="Просмотреть", command=Surveys_button2, height=2, width=20)
    button1.grid(row=0, column=0, padx=(0, 10))
    button2.grid(row=0, column=1, padx=(10, 0))

    def close_user_rights_window():
        w2.window.destroy()
        w.window.deiconify()

    w2.window.protocol("WM_DELETE_WINDOW", close_user_rights_window)

def add_surveys_window():
    w2.window.withdraw()
    w3 = NewWindow()
    w3.window.geometry("1000x200")
    # set minimum window size value
    w3.window.minsize(1000, 200)
    # set maximum window size value
    w3.window.maxsize(1000, 200)


    screen_width = w3.window.winfo_screenwidth()
    screen_height = w3.window.winfo_screenheight()
    center_x = int((screen_width - 1000) / 2)  # Adjust the width of the window as needed
    center_y = int((screen_height - 200) / 2)
    w3.window.geometry("400x200+{}+{}".format(center_x, center_y))

    frame_ = tk.Frame(w3.window)
    frame_.pack(pady=50)

    label1 = tk.Label(frame_, text="Имя")
    global entry1
    entry1 = tk.Entry(frame_)
    label2 = tk.Label(frame_, text="Адрес\nэлектронной почты", justify=LEFT)
    global entry2
    entry2 = tk.Entry(frame_)
    label3 = tk.Label(frame_, text="Характер обращения")
    global entry3
    entry3 = tk.Entry(frame_)
    label4 = tk.Label(frame_, text="Ваше обращение")
    global entry4
    entry4 = tk.Entry(frame_)
    label5 = tk.Label(frame_, text="Предложения\nпо улучшению", justify=LEFT)
    global entry5
    entry5 = tk.Entry(frame_)
    label6 = tk.Label(frame_, text="Дата")
    global entry6
    entry6 = tk.Entry(frame_)

    button = tk.Button(frame_, text="Добавить", command=add_surveys, height=1, width=10)

    label1.grid(row=0, column=0, padx=(0,100))
    entry1.grid(row=1, column=0, padx=10)

    label2.grid(row=0, column=1, padx=(0,10),pady=(0,10))
    entry2.grid(row=1, column=1, padx=10)

    label3.grid(row=0, column=2, padx=(0,10))
    entry3.grid(row=1, column=2, padx=10)

    label4.grid(row=0, column=3, padx=(0,30))
    entry4.grid(row=1, column=3, padx=10)

    label5.grid(row=0, column=4, padx=(0,40))
    entry5.grid(row=1, column=4, padx=10)

    label6.grid(row=0, column=5, padx=(0,97))
    entry6.grid(row=1, column=5, padx=10)

    button.grid(row=2, column=0,pady=(10,0),padx=(0,45))



    def close_user_rights_window():
        w3.window.destroy()
        w2.window.deiconify()

    w3.window.protocol("WM_DELETE_WINDOW", close_user_rights_window)
    pass


def add_surveys():
    #проверить формат данных
    #заствлять ввести все основные или все

    name = entry1.get()
    mail = entry2.get()
    t_deal = entry3.get()
    deal = entry4.get()
    suggetion = entry5.get()
    date = entry6.get()


    if (name and mail and t_deal and deal and suggetion and date) != '':
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        date_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        if name.isdigit():
            messagebox.showerror("Error", "Non valid Name - Name is string")
            entry1.delete(0, 'end')
        if re.match(email_pattern, mail) == None:
            messagebox.showerror("Error", "Non valid mail")
            entry2.delete(0, 'end')
        if re.match(date_pattern, date) == None:
            messagebox.showerror("Error", "Datetime format need (YYYY-MM-DD HH:MM:SS)")
            entry6.delete(0, 'end')
        else:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-KTVBTD1H;DATABASE=Telemarketing_Center_DB;')
            cursor = conn.cursor()

            query = f"exec [Telemarketing_Center_DB].[dbo].[surveys_insert] @Name = '{name}', @Email = '{mail}', @t_deal= '{t_deal}', @Deal_ = '{deal}', @sugg ='{suggetion}',@Date_ = '{date}'"
            cursor.execute(query)
            conn.commit()

            sql = """\
            SET NOCOUNT ON;
            DECLARE @RC int;
            EXEC @RC = [Telemarketing_Center_DB].[dbo].[surveys_insert] ?, ?, ?, ?, ?, ?;
            SELECT @RC AS rc;
            """
            values = (name ,mail,t_deal,deal,suggetion,date)
            cursor.execute(sql, values)
            rc = cursor.fetchval()

            if rc == 1:
                messagebox.showerror("Error", "Такого юзера не существует")
                cursor.close()
                conn.close()
            else:
                messagebox.showinfo('', 'Succsese')
                cursor.close()
                conn.close()
                entry1.delete(0, 'end'), entry2.delete(0, 'end'), entry3.delete(0, 'end'), entry4.delete(0, 'end'),
                entry5.delete(0, 'end'), entry6.delete(0, 'end')
    else:
        messagebox.showerror("Error", "Fields empty")




def Check_Surveys():
    webbrowser.open('https://docs.google.com/forms/d/1lz1McyQ7aqBApq0oIFoj5LlBZvQqeI2TPEuwi64mtb0/edit#responses')

# def button3_clicked():
#     print("Button 3 clicked")

def button4_clicked():
    w.window.withdraw()
    global w7
    w7 = NewWindow()
    button_frame = Frame(w7.window)
    button_frame.pack(pady=70)
    button1 = Button(button_frame, text="Добавить", command=add_news, height=2, width=20)
    button2 = Button(button_frame, text="Просмотреть", command=check_news, height=2, width=20)
    button1.grid(row=0, column=0, padx=(0, 10))
    button2.grid(row=0, column=1, padx=(10, 0))

    def close_user_rights_window():
        w7.window.destroy()
        w.window.deiconify()

    w7.window.protocol("WM_DELETE_WINDOW", close_user_rights_window)


def check_news():
    w7.window.withdraw()
    w9 = NewWindow()
    frame = tk.Frame(w9.window)
    frame.pack(pady=20)

    enabled = IntVar()
    label = Label(frame, text="Сортировка по")
    entry_ = Entry(frame)

    entry_.config(state="disabled")
    label.grid(row=0, column=1, padx=(0, 40))
    entry_.grid(row=1, column=1, padx=10)



    def check_box_new():
        if enabled.get() == 1:
            entry_.config(state="normal")
            button1 = Button(frame, text="Найти", command=search_new, height=2, width=20)
            button1.grid(row=1, column=0, padx=(0, 10))
        else:
            entry_.config(state="disabled")
            button1 = Button(frame, text="Найти", command=search_new, height=2, width=20)
            button1.grid(row=1, column=0, padx=(0, 10))



    enabled_checkbutton = Checkbutton(frame, text="Включить", variable=enabled, command=check_box_new)
    enabled_checkbutton.grid(row=2, column=0)

    def search_new():
        sort_ = entry_.get()
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-KTVBTD1H;DATABASE=Telemarketing_Center_DB;')
        cursor = conn.cursor()

        sql = """\
                    SET NOCOUNT ON;
                    DECLARE @RC int;
                    EXEC @RC = [Telemarketing_Center_DB].[dbo].[select_news] ?;
                    SELECT @RC AS rc;
                    """
        values = (sort_)
        cursor.execute(sql, values)
        rc = cursor.fetchval()
        if rc == -1:
            messagebox.showerror("Error", "Такого стобца нет")
            cursor.close()
            conn.close()
        else:
            query = f"exec [Telemarketing_Center_DB].[dbo].[select_news] @colum_ = '{sort_}'"
            cursor.execute(query)

            results = cursor.fetchall()

            list_ = []
            for row in results:
                item_dict = {}
                item_dict["NewID"] = row[0]
                item_dict["New"] = row[1]
                item_dict["AccauntID"] = row[2]
                list_.append(item_dict)

            w10= NewWindow()
            w10.window.geometry("1200x720")
            # set minimum window size value
            w10.window.minsize(1200, 700)
            # set maximum window size value
            w10.window.maxsize(1200, 700)
            screen_width = w10.window.winfo_screenwidth()  # Width of the screen
            screen_height = w10.window.winfo_screenheight()
            x = (screen_width / 2) - (1200 / 2)
            y = (screen_height / 2) - (700 / 2)
            w10.window.geometry('%dx%d+%d+%d' % (1200, 700, x, y))
            # frame_ = tk.Frame(w5.window)
            # frame_.pack(pady=10)
            list = Listbox(w10.window, height=10, width=197)
            list.pack(side=LEFT, fill=BOTH)
            scroll_bar = Scrollbar(w10.window)
            scroll_bar.pack(side=RIGHT, fill=BOTH)
            for line in list_:
                list.insert(END, f"NewID: {line['NewID']}; New: {line['New']}; AccountID: {line['AccauntID']}")

            list.config(yscrollcommand=scroll_bar.set)
            scroll_bar.config(command=list.yview)

            cursor.close()
            conn.close()
            entry_.delete(0, 'end')

    button1 = Button(frame, text="Найти", command=search_new, height=2, width=20)
    button1.grid(row=1, column=0, padx=(0, 10))

    def close_user_rights_window():
        w9.window.destroy()
        w7.window.deiconify()

    w9.window.protocol("WM_DELETE_WINDOW", close_user_rights_window)
def add_news():
    w7.window.withdraw()
    global w8
    w8 = NewWindow()
    frame = Frame(w8.window)
    frame.pack(pady=50)

    label1 = Label(frame, text="Текст новости")
    entry1 = Entry(frame)

    label2 = Label(frame, text="id аккаунта")
    entry2 = Entry(frame)

    def send():
        text = entry1.get()
        id_ = entry2.get()

        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-KTVBTD1H;DATABASE=Telemarketing_Center_DB;')
        cursor = conn.cursor()

        sql = """\
                    SET NOCOUNT ON;
                    DECLARE @RC int;
                    EXEC @RC = [Telemarketing_Center_DB].[dbo].[add_news] ?, ?;
                    SELECT @RC AS rc;
                    """
        values = (text,id_)
        try:
            cursor.execute(sql, values)
            rc = cursor.fetchval()
            if rc == 1:
                messagebox.showerror("Error", "Юзера с таким id не существует")
            else:
                conn.commit()
                messagebox.showinfo('', 'Succsese')
                entry1.delete(0, 'end'), entry2.delete(0, 'end')
        except pyodbc.Error as e:
            print("Error:", str(e))
            messagebox.showerror("Error", "Текст новостей не должен совпадать")
        finally:
            # Close the cursor and the connection
            cursor.close()
            conn.close()



    button = Button(frame, text="Добавить", command=send, height=2, width=10)



    label1.grid(row=0, column=0, padx=(0, 70))
    entry1.grid(row=1, column=0, padx=(0, 20))

    label2.grid(row=0, column=1, padx=(0, 40))
    entry2.grid(row=1, column=1, padx=(20, 0))

    button.grid(row=2, column=0, pady=(10,0),padx=(0, 60))

    def close_user_rights_window():
        w8.window.destroy()
        w7.window.deiconify()
    w8.window.protocol("WM_DELETE_WINDOW", close_user_rights_window)

def authenticate(username, password):

    try:
        #Encrypt=yes; TrustServerCertificate=yes;
        pyodbc.connect(f'DRIVER={{SQL Server}};SERVER=LAPTOP-KTVBTD1H;DATABASE=Telemarketing_Center_DB;Trusted_Connection=no; UID={username};PWD={password}')
    except:
        return False
    else:
        global safe_name
        safe_name = username
        return True
    # return (username == 'admine', password == 'password')

def login():
    username = entry_username.get()
    password = entry_password.get()
    # global safe_user, safe_pass
    # safe_user = username
    # safe_pass = password
    # if authenticate(username, password) and username != '' and password !='':
    if authenticate(username, password):
        root.withdraw()  # Hide the root window
        open_user_rights_window()
    else:
        messagebox.showerror("Authentication Failed", "Invalid username or password.")

def open_user_rights_window():
    global w
    w = NewWindow()
    button_frame = tk.Frame(w.window)
    button_frame.pack(pady=20)

    label = tk.Label(button_frame, text=f"Welcome {safe_name}")
    # label = tk.Label(button_frame, text=f"Welcome admin")

    button1 = tk.Button(button_frame, text="Опросы в БД", command=Surveys,height=2, width=20)
    button2 = tk.Button(button_frame, text="Статистика опросов", command=Check_Surveys,height=2, width=20)
    # button3 = tk.Button(button_frame, text="Button 3", command=button3_clicked,height=2, width=20)
    button4 = tk.Button(button_frame, text="Новости банка", command=button4_clicked,height=2, width=20)
    label.grid(row=0, column=0, padx=(0, 10), pady=(0, 10))
    button1.grid(row=1, column=0, padx=(0,10), pady=(0,10))
    button2.grid(row=1, column=1, padx=(10,0), pady=(0,10))
    # button3.grid(row=2, column=0, padx=(0,10), pady=(10,0))
    button4.grid(row=2, column=1, padx=(10,0), pady=(10,0))



    def close_user_rights_window():
        w.window.destroy()  # Close the user rights window
        root.deiconify()  # Show the main root window

    w.window.protocol("WM_DELETE_WINDOW", close_user_rights_window)



# Create the root window
root = tk.Tk()

root.title('Union Bank')
root.geometry("400x200")
# set minimum window size value
root.minsize(400, 200)

# set maximum window size value
root.maxsize(400, 200)


screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight()

x = (screen_width/2) - (400/2)
y = (screen_height/2) - (200/2)



# Create username label and entry
label_username = tk.Label(root, text="Username:")
label_username.pack(pady=(40,0))
entry_username = tk.Entry(root)
entry_username.pack()

# Create password label and entry
label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Create login button
btn_login = tk.Button(root, text="Login", command=login)
btn_login.pack(pady=10)



# Start the Tkinter event loop
root.geometry('%dx%d+%d+%d' % (400, 200, x, y))
root.mainloop()
