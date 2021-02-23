from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

# User Table using sqlalchemy syntax
class User(DB.Model):
    """Twitter users that correspond to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)


# Tweet Table
class Tweet(DB.Model):
    """Twitter tweets that correspond to users"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
              "user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: {}".format(self.text)


def insert_example_users():
    """Will get error ran twice, data to play with"""
    nick = User(id=1, name="Nick")
    elon = User(id=2, name="Elon")
    tweet1 = Tweet(id=1, text="I promise it will make sense", user_id=1)
    tweet2 = Tweet(id=2, text="I'll die on Mars..", user_id=2)
    tweet3 = Tweet(id=3, text="..hopefully not on landing", user_id=2)
    tweet4 = Tweet(id=4, text="Without space, life is pointless", user_id=2)
    tweet5 = Tweet(id=5, text="Can't type today", user_id=1)
    tweet6 = Tweet(id=6, text="Vue for life", user_id=1)
    tweets = [tweet1, tweet2, tweet3, tweet4, tweet5, tweet6]
    DB.session.add(nick)
    DB.session.add(elon)
    for i in tweets:
        DB.session.add(i)
    DB.session.commit()
