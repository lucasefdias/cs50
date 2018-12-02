import os

from cs50 import SQL
from datetime import datetime, timezone
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Retrieve user's portfolio from database
    portfolio = db.execute("SELECT symbol, SUM(shares) shares FROM portfolio WHERE id = :user_id GROUP BY symbol ",
                           user_id=session["user_id"])

    # Retrieve user's cash from database
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

    # Initialize user's total amount (user portfolio + cash)
    total = cash[0]['cash']

    # Create array of stock objects and loop through portfolio, adding each stock's symbol and shares
    stocks = []

    for item in portfolio:

        # Lookup name and updated price from user's stocks
        quote = lookup(item["symbol"])

        # Create stock object and assign corresponding values
        stock = {}

        stock['symbol'] = item["symbol"]
        stock['name'] = quote["name"]
        stock['shares'] = item["shares"]
        stock['price'] = usd(quote["price"])
        stock['total'] = usd(item["shares"] * quote["price"])

        # Add current stock's total to user's total amount
        total += quote["price"] * item["shares"]

        # Append stock object to stocks array
        stocks.append(stock)

    return render_template("index.html", stocks=stocks, cash=usd(cash[0]['cash']), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure that symbol is not blank
        if not request.form.get("symbol"):
            return apology("must input a symbol", 400)

        # Ensure that number of shares is not blank
        if not request.form.get("shares"):
            return apology("must specify a number of shares", 400)

        # Ensure that number of shares is valid (not fractional, negative or non-numeric)
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        # Lookup stock quote using lookup function
        quote = lookup(request.form.get("symbol"))

        # Ensure that the stock is valid
        if not quote:
            return apology("stock is not valid", 400)

        # Check if user can afford stock
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

        amount = quote["price"] * shares

        if cash[0]["cash"] < amount:
            return apology("you can't afford the stock", 400)

        # If user can afford stock, buy and add to portfolio
        bought = db.execute("INSERT INTO portfolio (id, symbol, shares, price, transacted) "
                            + "VALUES(:user_id, :symbol, :shares, :price, datetime('now'))",
                            user_id=session["user_id"], symbol=quote["symbol"],
                            shares=shares, price=quote["price"])

        if not bought:
            return apology("could not process purchase", 400)

        # Update user's cash
        updated = db.execute("UPDATE users SET cash = cash - :amount WHERE id = :user_id",
                             amount=amount, user_id=session["user_id"])

        if not updated:
            return apology("failed to update cash", 400)

        # Redirect to index route
        flash("Successfully bought shares!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Retrieve user's history from database
    log = db.execute("SELECT symbol, shares, price, transacted FROM portfolio WHERE id = :user_id ORDER BY transacted",
                     user_id=session["user_id"])

    # Create array of stock objects and loop through portfolio, adding each stock's symbol and shares
    history = []

    for entry in log:

        # Create event object and assign corresponding values
        event = {}

        event['symbol'] = entry["symbol"]
        event['shares'] = entry["shares"]
        event['price'] = usd(entry["price"])
        event['transacted'] = entry["transacted"]

        # Append stock object to stocks array
        history.append(event)

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash(f"Welcome back, {rows[0]['username']}!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logged out")
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure that symbol is not blank
        if not request.form.get("symbol"):
            return apology("must input a symbol", 400)

        # Lookup stock quote using lookup function
        quote = lookup(request.form.get("symbol"))

        # Ensure that the stock is valid
        if not quote:
            return apology("stock is not valid", 400)

        # Render template displaying corresponding stock quote
        return render_template("quoted.html", name=quote["name"], price=usd(quote["price"]), symbol=quote["symbol"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure there are no blank fields
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords did not match", 400)

        # Hashes the password
        password_hash = generate_password_hash(request.form.get("password"))

        # Stores user in the database (INSERT query returns primary key value for newly inserted row)
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :password_hash)",
                            username=request.form.get("username"), password_hash=password_hash)

        # If query failed (username is not available), apologize
        if not result:
            return apology("username not available", 400)

        # Logs the user automatically by remember their id in session
        session["user_id"] = result

        # Redirect user to home page
        flash(f"Welcome, {request.form.get('username')}!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Retrieve user's portfolio from database
    portfolio = db.execute("SELECT symbol, SUM(shares) shares FROM portfolio WHERE id = :user_id GROUP BY symbol",
                           user_id=session["user_id"])

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        shares = int(request.form.get("shares"))

        # Loop through portfolio until stock is found (ensure user has amount of shares)
        for item in portfolio:
            if item["symbol"] == request.form.get("symbol"):
                # Ensure user has specified amount of shares
                if shares > item["shares"]:
                    return apology("you don't have the specified number of shares", 400)

        # Retrieve updated price for specified stock
        quote = lookup(request.form.get("symbol"))

        # Log sale as negative number of shares to keep track of history
        sold = db.execute("INSERT INTO portfolio (id, symbol, shares, price, transacted) " +
                          "VALUES(:user_id, :symbol, :shares, :price, datetime('now'))",
                          user_id=session["user_id"], symbol=request.form.get("symbol"),
                          shares=-shares, price=quote["price"])

        if not sold:
            return apology("could not process sale", 403)

        # Calculate total value of sold shares
        amount = quote["price"] * shares

        # Update user's cash
        updated = db.execute("UPDATE users SET cash = cash + :amount WHERE id = :user_id",
                             amount=amount, user_id=session["user_id"])

        if not updated:
            return apology("failed to update cash", 403)

        # Redirect to home page
        flash("Successfully sold shares!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", portfolio=portfolio)

# -------------------
# PERSONAL TOUCHES
# -------------------

# PERSONAL TOUCH 1.a: Account page - change password link


@app.route("/account")
@login_required
def account():
    """ Shows account page """

    # Retrieves user info from database
    user = db.execute("SELECT username FROM users WHERE id = :user_id",
                      user_id=session["user_id"])

    if not user:
        return apology("could not retrieve user information", 403)

    return render_template("account.html", username=user[0]["username"])

# PERSONAL TOUCH 1.b: Change password route


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """ Enables password change """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("current"):
            return apology("must provide current password", 403)

        # Ensure current password is correct
        # Query database for user's current password
        rows = db.execute("SELECT hash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

        if not check_password_hash(rows[0]["hash"], request.form.get("current")):
            return apology("invalid current password", 403)

        # Ensure password was submitted
        if not request.form.get("new"):
            return apology("must provide new password", 403)

        # Ensure password confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must confirm new password", 403)

        # Ensure password and confirmation match
        if request.form.get("new") != request.form.get("confirmation"):
            return apology("passwords did not match", 403)

        # Hashes new password
        password_hash = generate_password_hash(request.form.get("new"))

        # Updates password in the database
        updated = db.execute("UPDATE users SET hash = :password_hash WHERE id = :user_id",
                             password_hash=password_hash, user_id=session["user_id"])

        # If query failed, apologize
        if not updated:
            return apology("could not change password", 403)

        # Redirect user to home page
        flash("Successfully altered password!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")


# PERSONAL TOUCH 2: Cash management page
@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """ Enables user to add cash or cash out """

    # Retrieves user's cash from database and passes it to template
    row = db.execute("SELECT cash FROM users WHERE id = :user_id",
                     user_id=session["user_id"])

    cash = row[0]["cash"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure user selects an operation
        if not request.form.get("operation"):
            return apology("you must select an operation", 403)

        # Ensure inputs an amount
        if not request.form.get("amount"):
            return apology("you must input an amount", 403)

        # Evaluates and executes corresponding operation
        if request.form.get("operation") == "add":
            message = "added"
            cash += float(request.form.get("amount"))
        else:
            message = "cashed out"
            cash -= float(request.form.get("amount"))

        # Updates user's cash
        updated = db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                             cash=cash, user_id=session["user_id"])
        if not updated:
            return apology("operation failed", 403)

        # Redirect to cash page
        flash(f"Successfully {message} {usd(float(request.form.get('amount')))}!")
        return redirect("/cash")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("cash.html", cash=usd(cash))


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
