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
    nick = User(id=1, name="nick")
    elon = User(id=2, name="elon musk")
    DB.session.add(nick)
    DB.session.add(elon)
    DB.session.commit()
