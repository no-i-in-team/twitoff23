"""Main main/routing file for Twitoff"""

from os import getenv
from flask import Flask, render_template, request, Blueprint
from flask_login import LoginManager, login_required, current_user
from .models import DB, User
from .twitter import aou_user, uall_users
from .predict import predict_user

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def root():
    return render_template("base.html", title= "Home",
    cred= current_user.name, users=User.query.all())


@main.route("/compare", methods=["POST"])
def compare():
    user0, user1 = sorted([request.values["user0"],
                            request.values["user1"]])

    if user0 == user1:
        message = "Cannot compare a user to itself!"

    else:
        prediction = predict_user( 
            user0, user1, request.values["tweet_text"])

        message = "'{}' is more likely a tweet by @{} than @{}".format(
            request.values["tweet_text"], user1 if prediction else user0, user0 if prediction else user1)

    return render_template("prediction.html", title="Prediction", message=message)


@main.route("/user/", methods = ["POST"])
@main.route("/user/<name>", methods = ["GET"])
def user(name=None, message=""):
    name = name or request.values["user_name"]

    try:
        if request.method == "POST":
            aou_user(name)
            message = "User {} successfully added!".format(name)

        tweets = User.query.filter(User.name == name).one().tweets

    except Exception as e:
        message = "Error adding '{}': {}".format(name, e)

        tweets = [] 

    return render_template("user.html",
                user=User.query.filter(User.name == name).one(), 
                tweets=tweets, 
                message=message)


@main.route("/update")
def update():
    """Update users"""
    uall_users()
    return render_template("base.html", title="Users Updated!", users=User.query.all())


@main.route("/reset")
def reset():
    """Reset database"""
    DB.drop_all()
    DB.create_all()
    return render_template("base.html", title="RESET",
        users=User.query.all())
