import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import holdem_calc


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        hero = [request.form.get("hole1"), request.form.get("hole2")]
        villain = [request.form.get("hole3"), request.form.get("hole4")]
        board = [request.form.get("flop1"), request.form.get("flop2"), request.form.get("flop3"),
                 request.form.get("turn"), request.form.get("river")]
    
        # Fixing board input
        try:
            while True:
                board.remove('')
        except ValueError:
            pass

        odds = holdem_calc.run(hero, villain, board)

        odds1 = "Win: " + str(odds[0]) + "%, " + "Lose: " + str(odds[1]) + "%, " + "Tie: " + str(odds[2]) + "%"
        odds2 = "Win: " + str(odds[3]) + "%, " + "Lose: " + str(odds[4]) + "%, " + "Tie: " + str(odds[5]) + "%"

        return render_template("home.html", odds1=odds1, odds2=odds2)

    else:
        return render_template("home.html", odds1="", odds2="")