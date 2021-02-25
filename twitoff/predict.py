"""Predicts who is more likely to say a hypothetical tweet"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet

def predict_user(user0_name, user1_name, hypothetical_tweet):
    """Determines which user is most lilely the tweet's author"""

    # Array of vectors
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    user0_vectors = np.array([tweet.vect for tweet in user0.tweets])
    user1_vectors = np.array([tweet.vect for tweet in user1.tweets])

    vectors = np.vstack([user0_vectors, user1_vectors])

    # Labels
    labels = np.concatenate(
             [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    model = LogisticRegression().fit(vectors, labels)

    hv_tweet = vectorize_tweet(hypothetical_tweet).reshape(1, -1)

    return model.predict(hv_tweet)
