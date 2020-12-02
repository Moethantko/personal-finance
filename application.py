import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session


app = Flask(__name__)

db = SQL("sqlite:///personalFinance.db")

@app.route("/", methods=["GET", "POST"])
def index():

    expenses = db.execute("SELECT * FROM expenditure")

    return render_template("home.html", expenses=expenses)
    
    
@app.route("/expense", methods=["GET", "POST"])
def expense():
    if (request.method == "GET"):

        return render_template("expense.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if (request.method == "GET"):

        return render_template("signup.html")

    else:

        username = request.form.get("username")
        password = request.form.get("password")


        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", username=username, password=password)

        return redirect("/")


