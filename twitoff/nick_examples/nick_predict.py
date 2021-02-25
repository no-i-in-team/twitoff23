"""A module that will predict who is more likely to say a hypothetical tweet"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine and return which user is more likely to say a given hypothetical
    tweet.
    Example run: predict_user("AOC", "elonmusk", "I like tesla")
        Returns either a 0 (AOC) or 1 (elonmusk)
    """
    # Grab each user from our SQLAlchemy DB
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()
    # Grab each tweet vetor from each user tweets list
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])
    # Vertically stack each users vector array on top of each other
    # We will then have an array of vects with user 0 vects on top of user 1
    vects = np.vstack([user0_vects, user1_vects])
    # Create labels for each tweet vector in vects
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])
    # Fit model
    log_reg = LogisticRegression().fit(vects, labels)
    # vectorize hypothetical tweet text and reshape to fit .predict format
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1, -1)

    # returns either a zero or 1
    return log_reg.predict(hypo_tweet_vect)