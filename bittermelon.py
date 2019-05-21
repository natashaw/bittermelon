"""
TODO: project description (aka documentation) (make it legible)
TODO: cover valid and invalid use cases
"""
import tweepy
import time
import os

CONSUMER_KEY = 'HIDDEN FOR SECURITY'
CONSUMER_SECRET = 'HIDDEN FOR SECURITY'
ACCESS_KEY = 'HIDDEN FOR SECURITY'
ACCESS_SECRET = 'HIDDEN FOR SECURITY'

FILE_NAME = 'last_seen_id.txt'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# DEV NOTE: length of keywords and salts must be identical
keywords = ("how are you",
            "how you doin",
            "what's up",
            "what's good",
            "waddup")

salts = ("Can't get no peace of mind, can't get no serenity",
         "Confusing the celebrity with your integrity. You drinkin' Hennessy for your therapy",
         "We're all slaves to a generation socialized and sickness is in the mind",
         "And even when you laughed, you cried",
         "We're all in denial and it's all cool until you're suicidal"
         )


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    if os.stat(file_name).st_size != 0:
        last_seen_id = int(f_read.read().strip())
    else:
        print("Empty last_seen_id! Using an old mention ID")
        last_seen_id = 1127325363376394243
        # 1127325363376394243 -- bitterMelon20: @bitterMelon20 42
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        for i in range(len(keywords)):
            if keywords[i] in mention.full_text.lower():
                print("responding back to: " + '@' +
                      mention.user.screen_name, flush=True)
                api.update_status('@' + mention.user.screen_name + ' ' +
                                  salts[i], mention.id)


while True:
    reply_to_tweets()
    time.sleep(10)
