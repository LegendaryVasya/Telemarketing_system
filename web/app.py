from flask import Flask, render_template, redirect, url_for, request, make_response, session
from db_check import Item
import string
from string import ascii_uppercase
import random
from db import ItemDatabase
from Cookie_check import Coc
from flask_socketio import SocketIO, join_room, leave_room, send
import functools
import datetime


app = Flask(__name__)
#для session
# app.secret_key = "hisfsdsdf"
app.config["SECRET_KEY"] = "hjhjsdahhds"
#web socket
socketio=SocketIO(app)

ch = Item()
db_ = ItemDatabase()
c = Coc()


letters = string.ascii_lowercase



rooms = {}




def privel_check(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if request.cookies.get('cookie') != None:
            user_cookie = request.cookies.get('cookie')
            priveleg = c.check(user_cookie)
            if 'worker' in priveleg:
                return func(*args, **kwargs)
        return redirect(url_for("index"))
    return secure_function


def user_check(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if request.cookies.get('cookie') != None:
            user_cookie = request.cookies.get('cookie')
            priveleg = c.check(user_cookie)
            if 'user' in priveleg:
                return func(*args, **kwargs)
        return redirect(url_for("index"))
    return secure_function

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code


@app.route('/')
def index():
    if request.cookies.get('cookie') != None:
        user_cookie = request.cookies.get('cookie')
        control = c.check(user_cookie)
        if 'user' in control:
            return redirect(url_for("menu"))
        elif 'worker' in control:
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.cookies.get('cookie') == None:
        rec = request.method
        if rec == 'POST':
            resultat = ch.check(rec)
            if request.form.get('remember') and resultat != {}:
                log = request.form["nm"]
                if 'user' in resultat:
                    resp = redirect(url_for('menu'))
                    cookie = ''.join(random.choice(letters) for i in range(50))
                    resp.set_cookie('cookie', cookie, max_age=60 * 60 * 24 * 365 * 5)
                    db_.put_item(cookie, log)
                    return resp
                elif 'worker' in resultat:
                    
                    resp = redirect(url_for('home'))
                    cookie = ''.join(random.choice(letters) for i in range(50))
                    resp.set_cookie('cookie', cookie, max_age=60 * 60 * 24 * 365 * 5)
                    db_.put_item(cookie, log)
                    return resp

            elif resultat != {}:
                log = request.form["nm"]
                if 'user' in resultat:
                    resp = redirect(url_for('menu'))
                    cookie = ''.join(random.choice(letters) for i in range(50))
                    resp.set_cookie('cookie', cookie)
                    db_.put_item(cookie, log)
                    return resp

                elif 'worker' in resultat:
                    resp = redirect(url_for('home'))
                    cookie = ''.join(random.choice(letters) for i in range(50))
                    resp.set_cookie('cookie', cookie)
                    db_.put_item(cookie, log)
                    return resp
            return render_template("index.html")
        else:
            return render_template("index.html")
    return redirect(url_for("index"))

@app.route("/home", methods=["POST", "GET"])
@privel_check
def home():
    # session.clear()
    items = db_.get_items()[1]
    len_ = len(items)
    admin_cookie = request.cookies.get('cookie')
    nikneym = c.check(admin_cookie)

    if request.method == "POST":
        name = nikneym["worker"]
        code = request.form.get("code")
        join = request.form.get("join", False)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name, items_ = items, items_len = len_)

        room = code

        if code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name, items_ = items, items_len = len_)

        session["room"] = room
        session["name"] = name

        return redirect(url_for("room"))
    return render_template("home.html", items_ = items, items_len = len_)


@app.route("/menu", methods=["POST", "GET"])
def menu():
    session.clear()
    if request.cookies.get('cookie') != None:
        user_cookie = request.cookies.get('cookie')
        control = c.check(user_cookie)
        if 'user' in control:
            user = control["user"]
            if request.cookies.get('session') != None:
                return redirect(url_for("room"))

            if request.method == "POST":
                create = request.form.get("create", False)
                room = ''
                if create != False:
                    room = generate_unique_code(4)
                    rooms[room] = {"members": 0, "messages": []}

                session["room"] = room
                session["name"] = user

                return redirect(url_for("room"))

            news = db_.get_news()
            details = db_.get_details()
            u_i = db_.get_items()[1]
            bill_info = db_.get_bill()


            for i in u_i:
                if user == i["login"]:
                    global id
                    id = i["accountID"]

            new_list = []
            for i in news:
                if id == i["accountID"]:
                    new_list.append(i["new"])



            details_list = []
            for i in details:
                if id == i["accountID"]:
                    details_list.append(i["Number"])
                    details_list.append(i["Type"])
                    details_list.append(i["Balance"])



            bill_list = []

            for i in details:

                if id == i["accountID"]:
                    dt = i["Number"]
                    for j in bill_info:
                        if dt == j["number_ac"]:
                            bill_list.append(j["date"])
                            bill_list.append(j["amount"])
                            bill_list.append(j["taker"])


            check_len_bill = 0
            for i in range(0,len(bill_list)):
                check_len_bill += 1

            return render_template('login.html', u = user, news_ = new_list , len_n = len(new_list), deta_i = details_list, bill_ = bill_list[::-1], bill_len = check_len_bill )
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.route("/room")
def room():
    room = session.get("room")
    name = session.get("name")
    db_.put_room(name, room)
    if room is None or name is None or room not in rooms:
        # db_.delete_room(name)
        return redirect(url_for('menu'))
    return render_template('room.html', code=room, messages=rooms[room]["messages"])


@app.route("/payment", methods=["POST", "GET"])
@user_check
def payment():
    detail_user = db_.get_details()
    user_cookie = request.cookies.get('cookie')
    user_name = c.check(user_cookie)
    user_info = db_.get_items()[1]
    safe_accout_id = {}


    for item in user_info:
        if user_name["user"] == item["login"]:
            safe_accout_id["ID"] = item["accountID"]

    if request.method == 'POST':
        rekvizit = request.form.get("ac_number")
        summa = float(request.form.get("summ"))
        pay_date = datetime.datetime.now()

        for rekv in detail_user:

            if rekvizit == str(rekv["Number"]):
                for det in detail_user:
                    if det["accountID"] == safe_accout_id["ID"]:

                        if det["Balance"] == summa or det["Balance"] >= summa:
                            db_.put_bill(summa, str(pay_date)[:19], det["Number"], rekvizit)
                            return render_template("payment.html", error='payment done')
                        else:
                            return render_template("payment.html", error='less money')

        return render_template("payment.html", error='Faild rekvizits')

    return render_template('payment.html')




@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)




@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    send({"name": name, "message": "has enter the room"}, to=room)
    rooms[room]["members"] += 1


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    # db_.delete_room(name)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)


@app.route("/logout")
def logout():
    session.clear()
    resp = redirect(url_for('login'))
    resp.set_cookie('cookie', '', expires=0)
    return resp

@app.route("/room_logout")
def room_logout():
    room = session.get("room")
    name = session.get("name")
    db_.delete_room(name)


    if room in rooms:
        rooms[room]["members"] -= 1

    return redirect(url_for('menu'))




if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)
