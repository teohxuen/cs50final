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
    # if num is string change it to a float
    if type(num) == str:
        num = float(num)
    # if num is a whole number conver it to an integer
    if num.is_integer():
        num = int(num)
    # if num is a float, round it to 2dp
    else:
        num = round(num,2)
    return num