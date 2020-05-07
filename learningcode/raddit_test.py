import praw #PRAW stands for Python Reddit API Wrapper
import pandas as pd
import datetime

#Functions
#def get_date(created):
#    return dt.datetime.fromtimestamp(created)

#connect to reddit - SETUP AN ACCOUNT ON REDDIT AND OBTAIN THE FOLLOWING:
reddit = praw.Reddit(client_id='', \
                     client_secret='', \
                     user_agent='', \
                     username='', \
                     password='')

subreddit = reddit.subreddit('all')

#top_
#ask_subreddit = subreddit.top()

ask_subreddit = subreddit.search("elearning", limit=5000)

csvfile = 'elearning_test.csv'

topics_dict = { "title":[], \
                "id":[], \
                "body":[], \
                "created":[], \
                "url":[], \
                "subreddit":[] }

for submission in ask_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["id"].append(submission.id)
    topics_dict["body"].append(submission.selftext)
    topics_dict["created"].append(datetime.datetime.utcfromtimestamp(submission.created).strftime('%m-%d-%Y'))
    topics_dict["url"].append(submission.url)
    topics_dict["subreddit"].append(submission.subreddit)

topics_data = pd.DataFrame(topics_dict)


#_timestamp = topics_data["created"].apply(get_date)
#topics_data = topics_data.assign(timestamp = _timestamp)

#print (topics_data)

topics_data.to_csv(csvfile, index=False) 