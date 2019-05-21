"""
BITTERMELON TWITTER BOT

This is a module of a twitter bot with handle @bitterMelon20, created as a
learning material in using Python in automating tasks, i.e., keyword-triggered
replies on Twitter.

supported use cases:
*) @bitterMelon20 bot will only reply to a tweet where it is mentioned AND
   and containing one of the defined keywords
*) the canned replies depend on the keyword tweeted to bot. see unsupported use
   cases for more details

unsupported use cases:
*) unique / customized reply with the same keyword. this is due to each reply
   corresponds to one keyword, by far. further customization and possible
   machine learning integration can be part of future improvements
*) any twitter user to get a reply from @bitterMelon20 at any time of day.
   so far bot is running on a PC. hence there's a limit to the uptime of the
   bot. additionally, bot still requires manual run from PC to start up
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
         "Confusing the celebrity with your integrity. You drinkin' Hennessy \
          for your therapy",
         "We're all slaves to a generation socialized and sickness is in the \
          mind",
         "And even when you laughed, you cried",
         "We're all in denial and it's all cool until you're suicidal"
         )


def retrieve_last_seen_id(file_name):
    """
    This function allows bot to detect whether the tweet ID seen at the time
    of polling mentions belongs to a status it already replied. This prevents
    bot to spam users it has already replied to

    Args:
        file_name (string): name of a text file from which bot
                            retrieves last ID

    Returns:
        int: returns the ID of last mention tweet replied to

    Raises:
        None

    """
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
    """
    This function allows bot to store the ID of the last mention it replied
    to. Used in the main function (reply_to_tweets())

    Args:
        last_seen_id (int): ID of the tweet status bot last replied to
        file_name (string): name of the text file to store last_seen_id

    Returns:
        None

    Raises:
        None

    """

    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    """
    Main function of the bot module. First, this function grabs the ID
    of the last tweet it replied to, so that mentions_timeline only returns
    statuses with ID greater than last_seen_id. Then bot would respond to
    only statuses containing one of the defined keywords, from oldest to
    newest. While responding, bot also stores last_seen_id to text file
    to keep ignoring statuses bot has already replied

    Args:
        None

    Returns:
        None

    Raises:
        None

    """
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
    # letting the bot to running continuousky until manual termination by user
    reply_to_tweets()
    time.sleep(10)
