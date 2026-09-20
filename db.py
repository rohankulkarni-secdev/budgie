import flask
import sqlite3
from datetime import datetime


db="budgie.db"

def connect_db():
    con = sqlite3.connect(db)
    con.row_factory=sqlite3.Row
    return con

def init_db():
    con=connect_db()
    con.execute("""CREATE TABLE IF NOT EXISTS
                  expenses(id integer primary key autoincrement, 
                           category text not null, amount real not null, 
                           currency text default "EUR", note text, date text NOT NULL, user_id INTEGER)""")
    
    con.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            home_country TEXT NOT NULL,
            home_currency TEXT NOT NULL,
            destination_country TEXT NOT NULL,
            destination_currency TEXT NOT NULL,
            user_type TEXT NOT NULL
        )""")
    
    con.commit()
    con.close()



