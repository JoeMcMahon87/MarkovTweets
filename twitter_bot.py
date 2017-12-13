from creds import *
import tweepy
import markovify
import os
import argparse

# Execute in script directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def generate_tweet(test_mode=False):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Read content to feed Markov model
    with open("tweet-content.txt", 'r') as f:
        text = f.read()
    text_model = markovify.NewlineText(text)

    # Generate the tweet text (use Twitter regular form of 140 characters)
    tweet = text_model.make_short_sentence(140)

    if test_mode:
        print(tweet)
    else:
        api.update_status(tweet)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a random tweet using Markov chain generation and post it.')
    parser.add_argument('--test', action='store_true', help='Test the functionality by printing the tweet')

    args = parser.parse_args()
    generate_tweet(args.test)
