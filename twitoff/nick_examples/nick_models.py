"""SQLAlchemy Database"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# User Table using SQLAlchemy syntax
class User(DB.Model):
    """Twitter Users that correspond to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.name)


# Tweet Table using SQLAlchemy syntax
class Tweet(DB.Model):
    """Twitter Tweets that corresspond to users"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: '{}'>".format(self.text)