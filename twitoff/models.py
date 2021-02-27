"""SQLAlchemy Database"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

DB = SQLAlchemy()

# User Table using sqlalchemy syntax
class User(DB.Model):
    """Twitter users that correspond to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    full_name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: '{}'>".format(self.name)


# Tweet Table
class Tweet(DB.Model):
    """Twitter tweets that correspond to users"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey("user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: '{}'>".format(self.text)

# Login Credentials
class Credential(UserMixin, DB.Model):

    userid = DB.Column(DB.Integer, primary_key=True) #sqlite_autoincrement=True?
    username = DB.Column(DB.String(50), unique=True)
    password = DB.Column(DB.String(50))
    email = DB.Column(DB.String, unique=True)

    def __repr__(self):
        return "<Credentials: '{}'>".format(self.username)