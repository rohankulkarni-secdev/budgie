from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime
from db import *

app = Flask(__name__)

@app.route("/")
def homePage():
    return render_template("home.html")

@app.route("/log", methods=['GET','POST'])
def expenses():
    con=connect_db()
    if request.method == "POST":
        con.execute(
            "INSERT INTO expenses (category, amount, currency, note, date) VALUES (?, ?, ?, ?, ?)",
            (
                request.form["category"],
                request.form["amount"],
                request.form.get("currency", "EUR"),
                request.form.get("note", ""),
                datetime.now().strftime("%Y-%m-%d"),
            )
        )
        con.commit()
        con.close()
        return redirect(url_for("expenses"))
    
    if request.method == "GET":
        rows = con.execute("SELECT * FROM expenses ORDER BY category, date DESC").fetchall()
        con.close()

        grouped_rows={}
        for row in rows:
            grouped_rows.setdefault(row['category'], []).append(row)
    return render_template('expenses.html', grouped=grouped_rows)

@app.route("/expenses/delete/<int:expense_id>", methods=['POST'])
def delete_expense(expense_id):
    con=connect_db()
    con.execute(f"DELETE FROM expenses WHERE id={expense_id}")
    con.commit()
    con.close()
    return redirect(url_for("expenses"))

init_db()
if __name__ =="__main__":
    app.run(debug=True)

