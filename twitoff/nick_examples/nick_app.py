"""Main app/routing file for Twitoff"""

from os import getenv
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import update_all_users, add_or_update_user
from .predict import predict_user


def create_app():
    """Create Flask Application"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route("/")
    def root():
        """At end point '/'"""
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route("/compare", methods=["POST"])
    def compare():
        user0, user1 = sorted([request.values["user0"],
                               request.values["user1"]])
        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])

            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values["tweet_text"], user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template("prediction.html", title="Prediction", message=message)

    @app.route("/user", methods=["POST"])
    @app.route("/user/<name>", methods=["GET"])
    def user(name=None, message=""):
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)

            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)

            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    @app.route('/update')
    def update():
        """Updates each user"""
        update_all_users()
        return render_template("base.html", title="Users Updated!", users=User.query.all())

    @app.route("/reset")
    def reset():
        """reset DB using drop_all()"""
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="RESET", users=User.query.all())

    return app