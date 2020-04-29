from flask import Flask, redirect, render_template, request, session
from flask_session import Session
# mkdtemp stores session in filesystem (?)
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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

@app.route("/")
@login_required
def index():
    return "TODO"

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return "TODO: Provide username"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "TODO: Provide Password"

        # Query database for username
        # TODO

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            # TODO

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")