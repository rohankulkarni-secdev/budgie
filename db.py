import flask
import sqlite3
from datetime import datetime


db="budgie_expenses.db"

def connect_db():
    con = sqlite3.connect(db)
    con.row_factory=sqlite3.Row
    return con

def init_db():
    con=connect_db()
    con.execute("""CREATE TABLE IF NOT EXISTS
                  expenses(id integer primary key autoincrement, 
                           category text not null, amount real not null, 
                           currency text default "EUR", note text, date text NOT NULL)""")
    con.commit()
    con.close()



