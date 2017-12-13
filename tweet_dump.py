import tweepy
from creds import *
import re
import argparse


URL_PATTERN = r'(http[s]?|ftp):\/?\/?([^:\/\s]+)((\/\w+))'


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    oldest_id = 0

    # Get oldest tweet pulled
    try:
        with open('last_id.txt', 'r') as infile:
            line = infile.readline()
            oldest_id = int(line)
    except IOError:
        print("Couldn't read oldest id")

    # initialize a list to hold all the tweepy Tweets
    all_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    # save most recent tweets
    all_tweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1
    newest = all_tweets[0].id
    with open('last_id.txt', 'w') as outfile:
        outfile.write(str(newest))

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0 and oldest > oldest_id:
        print("getting tweets before %s" % oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        # save most recent tweets
        all_tweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(all_tweets)))

    with open('tweet-content.txt', 'a') as file_handle:
        for tweet in all_tweets:
            if tweet.id > oldest_id:
                try:
                    txt = tweet.full_text
                    filtered = re.sub(URL_PATTERN, "", txt)
                    file_handle.write('\n' + filtered)
                except AttributeError:
                    txt = tweet.text
                    filtered = re.sub(URL_PATTERN, "", txt)
                    file_handle.write('\n' + filtered)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update Markov chain text source with latest set of tweets.')
    parser.add_argument('screen_name', help='Screen name to scrape text from to build content model')

    args = parser.parse_args()
    get_all_tweets(args.screen_name)
