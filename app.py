from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
# mkdtemp stores session in filesystem (?)
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime
from helper import login_required, convert

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
# db = SQL("sqlite:///fitness.db")

# To run on heroku
db = SQL("sqlite:///fitness.db")

# get today date 
today = date.today().isoformat()


@app.route("/", methods=["GET","POST"])
@login_required
def index():
    if request.method == "GET":
        # TODO INSERT MOTIVATIONAL QUOTE
        # TODO INSERT X short of COMPLETING  goal for Y

        # Select all the exercise from this user
        exercise = db.execute("SELECT name, id FROM exercises WHERE userid = :userid",
                                userid=session["user_id"])
        # if users have no exercise they are redireced to the page to add new exercise
        if len(exercise) == 0:
            # tell users that they have to add a new exercise
            flash("You currently have no exercises. Add an exercise!")
            return redirect("/new")

        # get a random exercise which has yet to reach the goal
        random = db.execute("SELECT name,target, target-SUM(count) FROM\
                            exercises LEFT JOIN history ON exercises.id = history.exerciseid\
                            WHERE exercises.userid=:userid AND target !=''\
                            GROUP BY exercises.id\
                            HAVING target-SUM(count)>0 OR target-SUM(count) IS NULL\
                            ORDER BY RANDOM() LIMIT 1", userid=session["user_id"])
        # if there is a random exercise

        if len(random) != 0:
            if random[0]["target-SUM(count)"] == None:
                random[0]["target-SUM(count)"] = random[0]["target"]
            random[0]["target-SUM(count)"] = convert(random[0]["target-SUM(count)"])
            random[0]["target"]=convert(random[0]["target"])

        return render_template("index.html", exercise=exercise, random=random)
    else:
        # HTML ensures that at least a count is chosen
        
        time = datetime.now().strftime("%d %b %Y %A %I %M %p")

        # insert work out into exercise history
        db.execute("INSERT INTO history (exerciseid, userid, count, notes, time)\
                    VALUES (:exerciseid, :userid, :count, :notes, :time)",
                    exerciseid=request.form.get("name"), userid=session["user_id"],
                    count=request.form.get("count"), notes=request.form.get("note"),
                    time = time)
        
        # return a message to indicate that work out has been added successfully
        flash("Work out added!")
        return redirect("/")


@app.route("/new", methods=["GET","POST"])
@login_required
def new():
    if request.method == "GET":
        return render_template("new.html", today=today)
    else:
        # HTML ensures all field are filled in
        # HTML ensures that date chosen is not before the present date

        row = db.execute("SELECT * FROM exercises WHERE name = :name AND userid = :userid",
                            name = request.form.get("name"), userid=session["user_id"])
        # if the user has an exercise with the same name
        if len(row) != 0:
            return render_template("error.html",num=403,msg="You have already created an exercise with the same name", link="/new")
        
        # insert new exercise to exercises database
        db.execute("INSERT INTO exercises (name, desc, target, date, userid)\
                    VALUES (:name, :desc, :target, :date, :userid)",
                    name=request.form.get("name"), desc=request.form.get("desc"),
                    target=request.form.get("count"), date=request.form.get("date"),
                    userid=session["user_id"])

        # flash a message to indciate that new exercise has been added
        flash("New exercise added!")            
        return redirect("/")


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
@login_required
def goals():
    if request.method == "GET":
        # Select all the exercise from this user
        exercise = db.execute("SELECT * FROM exercises WHERE userid = :userid",
                            userid=session["user_id"])
        for row in exercise:
            if row["target"] != "":
                row["target"] = convert(row["target"])
            # check if target date is empty
            if row["date"] != "":
                # if target date is not empty format the date
                temp = datetime.strptime(row["date"],"%Y-%m-%d")
                row["date"] = temp.strftime("%d %b %Y")
        return render_template("goals.html", exercise=exercise, today=today)
    
    else:
        db.execute("UPDATE exercises SET target = :target, date= :date WHERE id= :id",
                    target=request.form.get("target"), date = request.form.get("date"),
                    id=request.form.get("name"))
        flash("Your goal is updated! Kepp working to hit your goals!")
        return redirect("/goals")

@app.route("/stats")
@login_required
def stats():
    # get the list of exercises under this userid
    data = db.execute("SELECT id, name, target, date FROM exercises WHERE userid = :userid",
                        userid = session["user_id"])

    if len(data) == 0:
        # if users have no exercise added, it alerts the user on how he can add it
        flash("You current have no exercises added! Get moving! Click on 'New Exercise' to add a new exercise")

    for row in data:
        temp = db.execute("SELECT SUM(count) FROM history WHERE exerciseid = :exerciseid",
                            exerciseid=row["id"])

        # if user have done no work out for that particular exercise
        if temp[0]["SUM(count)"] == None:
            # set his count to 0
            row["count"] = 0
        else:
            row["count"] = convert(temp[0]["SUM(count)"])

        # if users have a target set
        if row["target"] != "":
            # find difference between current count and target
            row["diff"] = row["count"] - float(row["target"])
            row["diff"] = convert(row["diff"])
            row["target"] = convert(row["target"])
            # if target date is not left blank
            if row["date"] !="":
                # get the target date set
                tdate = datetime.strptime(row["date"],"%Y-%m-%d").date()
                today = datetime.today().date()
                # find out how many days are between target date and today
                row["tdiff"] = (tdate-today).days

                row["date"] = tdate.strftime("%d %b %Y")
                
                # if the difference is negative (yet to hit target)
                if row["diff"] < 0:
                    # if days left is 0
                    if row["tdiff"] == 0:
                        row["gpd"] = abs(row["diff"])
                    else:
                        # find out how many count per day to hit target
                        row["gpd"] = abs(convert(row["diff"]/row["tdiff"]))
        # user did not have a target count but has a target date
        elif row["date"] != "":
            tdate = datetime.strptime(row["date"],"%Y-%m-%d")
            row["date"] = tdate.strftime("%d %b %Y")

    flash("Click on Fitness60 to add more workouts! Get Moving!")
    return render_template("stats.html", data=data)


@app.route("/history")
@login_required
def history():
    # TODO Change the time to local timezone

    # get all work out completed by this user_id
    data = db.execute("SELECT time, count, notes, exerciseid FROM history WHERE\
                        userid = :userid", userid=session["user_id"])

    if len(data) == 0:
        # if users have no work out recorded, it alerts the user on how he can add it
        flash(" You current have no work out recorded! Get moving! Click on 'Fitness60' to add a new work out")

    # for each work out
    for row in data:
        # get the name of the exercise
        temp = db.execute("SELECT name FROM exercises WHERE id= :exerciseid",
                            exerciseid = row["exerciseid"])
        row["name"] = temp[0]["name"]

        # convert the count to integer if the count is a whole number
        row["count"] = convert(row["count"])

        # Format the time
        temptime = row["time"].split(" ")
        row["date"] = f"{temptime[0]} {temptime[1]} {temptime[2]}, {temptime[3]}"
        row["time"] = f"{temptime[4]}:{temptime[5]}{temptime[6]}"

    flash("Click on Fitness60 to add more workouts! Get Moving!")
    return render_template("history.html", data = data)


@app.route("/ippt", methods=["GET", "POST"])
@login_required
def ippt():
    if request.method == "GET":
        # get data from database
        goal = db.execute("SELECT pushup,situp,run,birthday FROM users WHERE id= :userid",
                            userid=session["user_id"])
        ippt = db.execute("SELECT date,pushup,situp,run,score,notes FROM ippt WHERE userid= :userid ORDER BY date",
                            userid=session["user_id"])

        # get today date
        today = date.today()
        # formate the date nicely and convert it to date formate
        born = datetime.strptime(goal[0]["birthday"],"%Y-%m-%d").date()
        # if today date (w/o year) is before the date of the birthday date (w/o) logical expression will return 1
        # so it will subtact 1 else it will not subtact one more
        # idea from https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        for row in ippt:
            # if date is present formate the date nicely
            if row["date"] != "":
                tdate = datetime.strptime(row["date"],"%Y-%m-%d")
                row["date"] = tdate.strftime("%d %b %Y")

        return render_template("ippt.html", goal=goal, ippt=ippt, age=age, today=today)

    else:
        # format 2.4km run timing
        min = request.form.get('min').lstrip("0")
        sec = request.form.get('sec')
        if int(sec) == 0:
            sec = "00"
        else:
            sec = sec.lstrip("0")
        run = f"{min}:{sec}"
        # update IPPT goal
        if request.form.get("submit") == "update":
            db.execute("UPDATE users SET pushup=:pushup,situp=:situp,run=:run WHERE id=:userid",
                        pushup=request.form.get("pushup"), situp=request.form.get("situp"), run=run,
                        userid=session["user_id"])
            flash("IPPT Goals Updated")
        # add new ippt result
        else:
            db.execute("INSERT INTO ippt (userid,date,pushup,situp,run,score,notes)\
                        VALUES (:userid, :date, :pushup, :situp, :run, :score, :notes)",
                        userid=session["user_id"], date=request.form.get("date"),
                        pushup=request.form.get("pushup"), situp=request.form.get("situp"),
                        run=run, score=request.form.get("score"), notes=request.form.get("notes"))
            flash("IPPT Added")
        return redirect("/ippt")


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
        return render_template("register.html", maxdate = today)
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
        min = request.form.get('min').lstrip("0")
        sec = request.form.get('sec')
        if int(sec) == 0:
            sec = "00"
        else:
            sec = sec.lstrip("0")
        run = f"{min}:{sec}"

        # insert the new user into the database
        db.execute("INSERT INTO users (name, birthday, pushup, situp, run, hash)\
                    VALUES (:name, :birthday, :pushup, :situp, :run, :hash)",
                   name=username, birthday=request.form.get("birthday"), 
                   pushup=request.form.get("pushup"), situp=request.form.get("situp"),
                   run=run, hash=password)        

        flash("User registered! Please login.")
        # redirect users to the index page
        return redirect("/login")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html", msg=e.name, num=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
