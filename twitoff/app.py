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
        """At endpoint '/' """
        users = User.query.all()
        return render_template("base.html", title= "Home", users=users)
    
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        insert_example_users()
        return render_template("base.html", title="RESET", users=User.query.all())

    return app