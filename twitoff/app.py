"""Main app/routing file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User, Tweet, insert_example_users


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route("/")
    def root():
        users = User.query.all()
        tweets = Tweet.query.all()
        return render_template("base.html", title= "Home", 
            users=users, tweets=tweets)
    
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        insert_example_users()
        return render_template("base.html", title="RESET",
            users=User.query.all(), tweets=Tweet.query.all())


    @app.route("/href/Nick")
    def Nick():
        return render_template("user.html", title="Nick's Tweets",
            user=User.query.filter_by(id=1),
            tweets=Tweet.query.filter_by(user_id=1))


    @app.route("/href/Elon")
    def Elon():
        return render_template("user.html", title="Elon Musk's Tweets",
            user=User.query.filter_by(id=2),
            tweets=Tweet.query.filter_by(user_id=2))

    return app