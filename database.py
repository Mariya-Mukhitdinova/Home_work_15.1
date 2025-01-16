import sqlite3
connection = sqlite3.connect("my_bot.db")
sql = connection.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS users "
            "(name TEXT, user_id INTEGER,"
            "phone_number TEXT);")

connection.commit()

def add_user(name,user_id, phone_number):
    connection = sqlite3.connect("my_bot.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO users (name, user_id, phone_number) "
                "VALUES (?, ?, ?);", (name, user_id, phone_number))
    connection.commit()

def check_user(user_id):
    connection = sqlite3.connect("my_bot.db")
    sql = connection.cursor()
    check = sql.execute("SELECT * FROM users WHERE user_id=?", (user_id, )).fetchone()
    if check:
        return True
    elif not check:
        return False
    connection.commit()
