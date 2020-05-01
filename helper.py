from flask import redirect, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f) #wraps and replace the function
    def decorated_function(*args, **kwargs):
        # if no user_id means the user did not login
        if session.get("user_id") is None:
            # redirect user to login page
            return redirect("/login")
        # runs the original function
        return f(*args, **kwargs)
    return decorated_function


def convert(num):
    if type(num) == str:
        num = round(float(num),2)
    if num.is_integer():
        num = int(num)
    return num