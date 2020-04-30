from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
# mkdtemp stores session in filesystem (?)
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required

# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request # Runs after each request
def after_request(response):
    # response headers are HTTP header that are used in HTTP response
    # cache-control hold instructions for caching request and response
    # no-cache means response can be stored by any cache however stored response must go though validation with origin server
    # no-store response may not be stored in any cache
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # Expire headers contain the date/time in which the response is considered stale
    # value '0' indicates that resources is already expired
    response.headers["Expires"] = 0
    # used for backward compatibility where Cache-control is not yet present
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
# sore session on on a directory made by mkdtemp()
# mkdtep() creates a temporary directory in most secure manner
# there is no race conditions, direcotry is readable, writable and searchable
# need to delete directory when done with it
app.config["SESSION_FILE_DIR"] = mkdtemp()
# session will not be permanent
app.config["SESSION_PERMANENT"] = False
# FileSystemSessionInterface
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fitness.db")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
    # HTML forces users to enter username and password

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", msg="invalid username and/or password", num=403, link="/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/goals", methods=["GET","POST"])
def goals():
    return TODO


@app.route("/stats")
def stats():
    return TODO


@app.route("/history")
def history():
    return TODO


@app.route("/ippt", methods=["GET", "POST"])
def ippt():
    return TODO


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        # HTML checks if all fields are filled
        # Ensure password was submitted and the passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("error.html", num=403, msg="Both password must match", link="/register")

        username = request.form.get("username")

        rows = db.execute("SELECT * FROM users WHERE name = :username",
                          username=username)

        # there is already someone with this username
        if len(rows) > 0:
            return render_template("error.html", msg="Username has been taken. Please choose a new username", link="/register")

        # get the hashed password
        password = generate_password_hash(request.form.get("password"))

        # format 2.4 run time
        run = "00:" + request.form.get("min") + ":" + request.form.get("sec")

        # insert the new user into the database
        db.execute("INSERT INTO users (name, birthday, pushup, situp, run, hash)\
                    VALUES (:name, :birthday, :pushup, :situp, :run, :hash)",
                   name=username, birthday=request.form.get("birthday"), 
                   pushup=request.form.get("pushup"), situp=request.form.get("situp"),
                   run=run, hash=password)        

        # redirect users to the index page
        return redirect("/login")
