# Use Case 1: this script fetches tweets and stores to database
# cd to the directory where this script 'lives' and run it from there.

############################
# LIBRARIES
############################
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time
import TerDec as td

############################
# SETUP vader, db
############################
analyzer = SentimentIntensityAnalyzer()
conn = sqlite3.connect('twitter_sentiment.db') #use whichever name you like for your db. just make sure you use the same db name in your subsequent scripts (i.e. Pt2-4)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
conn.commit()
ct=td.counter(count='      No. of Tweets put into database: ')
############################
# Creds
############################
#your consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

############################
# class object
############################
class listener(StreamListener): #listener is being declared as a class inheriting from base class StreamListener

    def on_data(self, data): #this is therefore a method from StreamListener
        try: 
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",(time_ms, tweet, sentiment))
            conn.commit()
            ct.flush()

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)

try:
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["a","e","i","o","u"]) #best means of fetching 'everything' from twitter.

except Exception as e:
    print(str(e))
    time.sleep(5)
