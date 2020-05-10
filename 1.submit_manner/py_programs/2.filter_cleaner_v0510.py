#LIBRARIES
import pandas as pd
import sqlite3
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
#from nltk.tokenize import sent_tokenize
#from nltk.tokenize import word_tokenize

import TerDec as td # Personal module,needs TerDec.py needs pandas
############################

mission0=td.Mission('Initial')
ct=td.counter(count='      Tweets into database') #Counter from TerDec.py
dbpath=td.setpath('./data/tweets_raw.db') #Path tool from TerDec.py
dbpath.askupdate('Path of database')
kwpath=td.setpath('./data/key_words.csv')
kwpath.askupdate('Path of key words list')
expath=td.setpath('./data/target.xlsx')
expath.askupdate('Path of export excel file')
stop_words = set(stopwords.words('english'))
conn = sqlite3.connect(dbpath.path)
c = conn.cursor()
df = pd.read_sql("SELECT * FROM raw_tweets", conn)
filter_list = ""
print('Check Data Structure and first 5:\n')
df.info()
print('\n',df.head())
mission0.end()

mission1=td.Mission('Filter from csv list')
key_words = pd.read_csv(kwpath.path)
print(key_words)
for index,row in key_words.iterrows():
    filter_list = filter_list+row['keywords'] +'|'
filter_input = filter_list[:-1]
df_fl=df.loc[df['tweets'].str.contains(filter_input)]
df_fl['timestamp_ms'] = pd.to_datetime(df_fl['timestamp_ms'],unit='ms')
print('Check Filtered Data Structure: \n')
df_fl.info()
print(df_fl.head())
mission1.end()

mission2=td.Mission('Text processing')
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')
def removeURLs(str):
    ans = ""
    clean_tweet1 = re.match('(.*?)http.*?\s?(.*?)', str)
    clean_tweet2 = re.match('(.*?)https.*?\s?(.*?)', str)
    if clean_tweet1:
        ans=ans+clean_tweet1.group(1)
        ans=ans+clean_tweet1.group(2)
    elif clean_tweet2: 
        ans=ans+clean_tweet2.group(1)
        ans=ans+clean_tweet2.group(2)
    else:
        ans = str
    return ans
ps = PorterStemmer()
def stemWords(word):
    if word in specialWords:
            return word
    else:
        return ps.stem(word)
specialWords = ["coronavirus", "covid","quarantine","coronavirusoutbreak","virus","corona","lockdown"]
wnl = WordNetLemmatizer()
def lemmatizeWords(word):
    if word in specialWords:
            return word
    else:
        return wnl.lemmatize(word)

df_fl["cleaning"] = df_fl["tweets"]
df_fl["cleaning"] = [re.sub('[^a-zA-Z]', ' ',i) for i in df_fl["cleaning"]]
df_fl["cleaning"] = [i.lower() for i in df_fl["cleaning"]]
df_fl["cleaning"]  = [deEmojify(i) for i in df_fl["cleaning"]]
df_fl["cleaning"]  = df_fl["cleaning"] .apply(lambda tweet: removeURLs(tweet))
df_fl["cleaning"] = df_fl["cleaning"].apply(lambda tweet: ' '.join([word for word in tweet.split() if word not in stop_words]))
df_fl["cleaning"] = df_fl["cleaning"].apply(lambda tweet: ' '.join([stemWords(word) for word in tweet.split()]))
df_fl["cleaning"]  = df_fl["cleaning"] .apply(lambda tweet: ' '.join([lemmatizeWords(word) for word in tweet.split()]))
print('Check cleaned Data Structure and samples: \n')
df_fl.info()
print('\n',df_fl.head())
mission2.end()

mission3=td.Mission('Export to Excel')
df_fl.to_excel(expath.path,index=False)
mission3.end()
