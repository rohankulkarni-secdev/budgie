import os
from datetime import datetime, timedelta
from functools import wraps

import requests
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from db import connect_db, init_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "budgie-dev-secret-2026")

EXCHANGE_API_KEY = "c9d8658bae2aed70b2c65b52"
EXCHANGE_RATE_CACHE = {}

COUNTRY_CURRENCY = {
    "India": "INR", "Ireland": "EUR", "United Kingdom": "GBP",
    "United States": "USD", "Germany": "EUR", "France": "EUR",
    "Canada": "CAD", "Australia": "AUD", "Japan": "JPY",
    "China": "CNY", "Netherlands": "EUR", "Spain": "EUR",
    "Italy": "EUR", "Sweden": "SEK", "Switzerland": "CHF",
    "New Zealand": "NZD", "Singapore": "SGD", "UAE": "AED",
    "South Korea": "KRW", "Poland": "PLN",
}


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("loginPage"))
        return f(*args, **kwargs)
    return wrapper


def get_rates(base_currency):
    cached = EXCHANGE_RATE_CACHE.get(base_currency)
    if cached and datetime.now() - cached["fetched_at"] < timedelta(hours=12):
        return cached["rates"]

    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base_currency}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    rates = response.json()["conversion_rates"]

    EXCHANGE_RATE_CACHE[base_currency] = {"rates": rates, "fetched_at": datetime.now()}
    return rates

def convert(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return round(amount, 2)
    try:
        rates = get_rates(from_currency)
        rate = rates.get(to_currency)
        return round(amount * rate, 2) if rate else round(amount, 2)
    except requests.RequestException:
        return round(amount, 2)

    
@app.route("/", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        home_country = request.form["home_country"]
        destination_country = request.form["destination_country"]
        user_type = request.form["user_type"]
        budget = request.form["budget"]

        con = connect_db()
        try:
            con.execute(
                """INSERT INTO users
                   (email, password_hash, home_country, home_currency,
                    destination_country, destination_currency, user_type, budget, savings)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    email,
                    generate_password_hash(password),
                    home_country,
                    COUNTRY_CURRENCY[home_country],
                    destination_country,
                    COUNTRY_CURRENCY[destination_country],
                    user_type,
                    budget,
                    budget,
                )
            )
            con.commit()
        finally:
            con.close()

        return redirect(url_for("loginPage"))

    return render_template("sign_up.html", countries=COUNTRY_CURRENCY)


@app.route("/login", methods=["GET", "POST"])
def loginPage():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        con = connect_db()
        try:
            user = con.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        finally:
            con.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("homePage"))

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("loginPage"))


@app.route("/home", methods=["GET", "POST"])
@login_required
def homePage():
    return render_template("home.html")


@app.route("/log", methods=["GET", "POST"])
@login_required
def expenses():
    con = connect_db()
    try:
        if request.method == "POST":
            if request.form["date"]:
                con.execute(
                    """INSERT INTO expenses (user_id, category, amount, currency, note, date)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (

                        session["user_id"],
                        request.form["category"],
                        request.form["amount"],
                        request.form.get("currency"),
                        request.form.get("note", ""),
                        request.form["date"],
                        
                    )
                )
            else:
                con.execute("""INSERT INTO expenses (user_id, category, amount, currency, note, date)
                                    VALUES (?, ?, ?, ?, ?, ?)""",
                                    (
                
                                        session["user_id"],
                                        request.form["category"],
                                        request.form["amount"],
                                        request.form.get("currency"),
                                        request.form.get("note", ""),
                                        datetime.now().strftime("%Y-%m-%d"),

                                        
                                    )
                                )
                
            con.commit()
            return redirect(url_for("expenses"))

        current_user = con.execute(
            "SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()

        budget = current_user["budget"] if current_user else None
        destination_currency = current_user["home_currency"] if current_user else None
        home_currency = current_user["destination_currency"] if current_user else None
        rows = con.execute(
            "SELECT * FROM expenses WHERE user_id = ? ORDER BY category, date DESC",
            (session["user_id"],)).fetchall()
        
        
        grouped = {}
        grand_total_destination = 0
        grand_total_home = 0
        savings = 0

        for row in rows:
            row = dict(row)
            row["converted_amount"] = convert(row["amount"], row["currency"], destination_currency)
            grand_total_destination += row["converted_amount"]
            grand_total_home += convert(row["amount"], row["currency"], home_currency)
            savings = budget - grand_total_home
            print(savings)
            con.execute("UPDATE users SET savings = ? where id = ?", (savings,session["user_id"]))
            con.commit()

            grouped.setdefault(row["category"], []).append(row)

        
        return render_template(
            "expenses.html",
            grouped=grouped,
            home_currency=home_currency,
            destination_currency=destination_currency,
            grand_total_destination=round(grand_total_destination, 2),
            grand_total_home=round(grand_total_home, 2),
        )

    finally:
        con.close()

#this is a comment just for test
@app.route("/log/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):
    con = connect_db()
    try:
        current_user = con.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        home_currency = current_user["destination_currency"] if current_user else None
        expense = con.execute("SELECT * FROM expenses WHERE id = ? AND user_id = ?", (expense_id, session["user_id"])).fetchone()
        amount_spent = convert(expense["amount"], expense["currency"], home_currency)
        
        con.execute("UPDATE users SET savings = savings + ? WHERE id = ?", (amount_spent,session["user_id"]))
        con.commit()
        con.execute(
            "DELETE FROM expenses WHERE id = ? AND user_id = ?",
            (expense_id, session["user_id"])
        )
        con.commit()
    finally:
        con.close()
    return redirect(url_for("expenses"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profilePage():
    if request.method=="GET":
        try:
            con=connect_db()
            user = con.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        finally:
            con.close()
    return render_template("profile.html", user=user)


@app.route("/profile/delete", methods=["POST", "GET"])
@login_required
def delete_account():
    try:
        con=connect_db()
        con.execute("DELETE FROM expenses WHERE id= ?", (session["user_id"],)) #remove data
        con.execute("DELETE FROM users WHERE id= ?", (session["user_id"],)) #remove acc
    finally:
        con.commit()
        con.close()
    session.pop("user_id", None)
    return redirect(url_for("signUp"))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    con = connect_db()
    try:
        user = con.execute(
            "SELECT * FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()
        expenses = con.execute(
            "SELECT * FROM expenses WHERE user_id = ? ORDER BY date",
            (session["user_id"],),
        ).fetchall()
    finally:
        con.close()

    currency = user["home_currency"]
    category_totals = {}
    month_totals = {}
    day_totals = {}
    day_counts = {}
    total_spent = 0
    total_eur = 0
    total_inr = 0

    for expense in expenses:
        amount = convert(expense["amount"], expense["currency"], currency)
        total_eur += convert(expense["amount"], expense["currency"], "EUR")
        total_inr += convert(expense["amount"], expense["currency"], "INR")
        expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
        month_key = expense_date.strftime("%Y-%m")
        day_key = expense_date.strftime("%Y-%m-%d")

        category_totals[expense["category"]] = (
            category_totals.get(expense["category"], 0) + amount
        )
        month_totals[month_key] = month_totals.get(month_key, 0) + amount
        day_totals[day_key] = day_totals.get(day_key, 0) + amount
        day_counts[day_key] = day_counts.get(day_key, 0) + 1
        total_spent += amount

    months = [
        {
            "label": datetime.strptime(month, "%Y-%m").strftime("%b %Y"),
            "total": round(amount, 2),
        }
        for month, amount in sorted(month_totals.items())
    ]
    categories = [
        {"label": category, "total": round(amount, 2)}
        for category, amount in sorted(
            category_totals.items(), key=lambda item: item[1], reverse=True
        )
    ]
    high_days = [
        {
            "label": datetime.strptime(day, "%Y-%m-%d").strftime("%b %d, %Y"),
            "total": round(amount, 2),
            "count": day_counts[day],
        }
        for day, amount in sorted(
            day_totals.items(), key=lambda item: item[1], reverse=True
        )[:5]
    ]
    average_monthly = total_spent / len(months) if months else 0

    dashboard_data = {
        "currency": currency,
        "total": round(total_spent, 2),
        "total_eur": round(total_eur, 2),
        "total_inr": round(total_inr, 2),
        "expense_count": len(expenses),
        "average_monthly": round(average_monthly, 2),
        "months": months,
        "categories": categories,
        "high_days": high_days,
    }
    return render_template(
        "dashboard.html", user=user, dashboard_data=dashboard_data
    )

init_db()
if __name__ == "__main__":
    app.run(debug=True)
