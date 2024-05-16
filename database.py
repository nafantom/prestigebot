import sqlite3

database = sqlite3.connect('users.db')
cursor = database.cursor()


def create_users_table():
    cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    full_name VARCHAR(50),
    phone_number VARCHAR(50),
    date VARCHAR(50),
    time INTEGER 
    )
    ''')

create_users_table()
database.commit()
database.close()