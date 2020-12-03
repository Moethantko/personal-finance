import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///personalFinance.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    expenses = db.execute("SELECT * FROM expenditure")

    expensesTotal = 0.0     #for stickers

    for expense in expenses:
        expensesTotal = expensesTotal + float(expense["amount"])

    balance = str(0.0 - expensesTotal)
    expensesTotal = str(expensesTotal)

    return render_template("home.html", expenses=expenses, expensesTotal=expensesTotal, balance=balance)


@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    if (request.method == "GET"):

        return render_template("expense.html")

    else:

        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        memo = request.form.get("memo")

        db.execute("INSERT INTO expenditure (amount, category, date, memo) VALUES (:amount, :category, :date, :memo)", amount=amount, category=category, date=date, memo=memo)

        return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if (request.method == "GET"):

        return render_template("signup.html")

    else:

        username = request.form.get("username")
        password = request.form.get("password")

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=generate_password_hash(password))

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():

    if (request.method == "GET"):

        return render_template("login.html")

    else:

        username = request.form.get("username")
        password = request.form.get("password")

        users = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(users) != 1 or not check_password_hash(users[0]["hash"], password):

            return render_template("login.html")

        else:

            session["user_id"] = users[0]["id"]

            return redirect("/")


@app.route("/logout")
def logout():

    session.clear()

    return render_template("login.html")

