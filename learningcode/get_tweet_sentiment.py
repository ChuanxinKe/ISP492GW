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
import TerDec as td #个人开发模块,需要TerDec.py支持

mission_inti=td.Mission('开始初始化')

mission0_1=td.Mission('初始化变量并接连主数据库,目前有bug数据更改在根目录')
analyzer = SentimentIntensityAnalyzer()
ct=td.counter(count='      No. of Tweets put into database: ')
conn = sqlite3.connect('twitter_sentiment.db') #use whichever name you like for your db. just make sure you use the same db name in your subsequent scripts (i.e. Pt2-4)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
conn.commit()
mission0_1.end()

mission0_2=td.Mission('接连today备份数据库,目前有bug,数据更改在根目录')
conn_today=sqlite3.connect('(today)twitter_sentiment.db')#建议当天跑完后重命名,然后从空表格(model)twitter_sentiment.db复制重命名,做到每日数据有个备份文件
c_today=conn_today.cursor()
c_today.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
conn.commit()
conn_today.commit()
mission0_2.end()

mission0_3=td.Mission('读取API Keys')
ckey=""
csecret=""
atoken=""
asecret=""
mission0_3.end()

mission_inti.end()
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
            
            c_today.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",(time_ms, tweet, sentiment))
            conn.commit()
            conn_today.commit()
            ct.flush()

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)


mission1=td.Mission('开始主程序,获取tweets推送并录入数据库,显示数据量提示')
try:
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["a","e","i","o","u"]) #best means of fetching 'everything' from twitter.

except Exception as e:
    print(str(e))
    time.sleep(5)
