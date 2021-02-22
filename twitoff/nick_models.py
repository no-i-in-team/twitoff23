"""SQLAlchemy Database"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# User Table using SQLAlchemy syntax
class User(DB.Model):
    """Twitter Users that correspond to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)


# Tweet Table using SQLAlchemy syntax
class Tweet(DB.Model):
    """Twitter Tweets that corresspond to users"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)


def insert_example_users():
    """Will get error ran twice, data to play with"""
    nick = User(id=1, name="nick")
    elonmusk = User(id=2, name="elon musk")
    DB.session.add(nick)
    DB.session.add(elonmusk)
    DB.session.commit()
