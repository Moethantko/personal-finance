import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session


app = Flask(__name__)

db = SQL("sqlite:///personalFinance.db")

@app.route("/", methods=["GET", "POST"])
def index():

    expenses = db.execute("SELECT * FROM expenditure")

    expensesTotal = 0.0     #for stickers

    for expense in expenses:
        expensesTotal = expensesTotal + float(expense["amount"])
        
    balance = str(0.0 - expensesTotal)
    expensesTotal = str(expensesTotal)

    return render_template("home.html", expenses=expenses, expensesTotal=expensesTotal, balance=balance)


@app.route("/expense", methods=["GET", "POST"])
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


        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", username=username, password=password)

        return redirect("/")


