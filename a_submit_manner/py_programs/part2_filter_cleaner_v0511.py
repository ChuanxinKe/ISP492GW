#LIBRARIES
import pandas as pd
import sqlite3
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.casual import TweetTokenizer
from nltk.corpus import wordnet
import TerDec as td # Personal module,needs TerDec.py needs pandas
############################

mission0=td.Mission('Initial')
dbpath=td.setpath(r'./data/tweets_raw.db') #Path tool from TerDec.py
dbpath.askupdate('Path of database')
kwpath=td.setpath(r'./data/key_words.csv')
kwpath.askupdate('Path of key words list')
expath=td.setpath(r'./data/target.xlsx')
expath.askupdate('Path of export excel file')
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
df_fl.loc[:,'timestamp_ms'] = pd.to_datetime(df_fl['timestamp_ms'],unit='ms')
print('Check Filtered Data Structure: \n')
df_fl.info()
print(df_fl.head())
mission1.end()

mission2=td.Mission('Setup text processing functions')
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')
def removeURLs(str):
    ans = ""
    clean_tweet1 = re.match(r'(.*?)http.*?\s?(.*?)', str)
    clean_tweet2 = re.match(r'(.*?)https.*?\s?(.*?)', str)
    if clean_tweet1:
        ans=ans+clean_tweet1.group(1)
        ans=ans+clean_tweet1.group(2)
    elif clean_tweet2: 
        ans=ans+clean_tweet2.group(1)
        ans=ans+clean_tweet2.group(2)
    else:
        ans = str
    return ans
tokenizer=TweetTokenizer()
def deleterefer(word):
    new=[]
    for i in word:
        if "@" in i or "#" in i:
            pass
        else:
            new.append(i)
    return new
stop_words = set(stopwords.words('english'))
stop_words.add(r'rt')
single='''qwertyuiopasdfghjklzxcvbnm!)-][}{;:'"(\,<>./?@#$%^&*_~'''
for i in single:
    stop_words.add(i)
def drop_stop(lists):
    new=[]
    for i in lists:
        if i not in stop_words:
            new.append(i)
    return new
wnl = WordNetLemmatizer()
def lemmatizeWords(lists):
    #Map POS tag to first character lemmatize() accepts
    new=[]
    for i in lists:
        tag = nltk.pos_tag([i])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}       
        pos=tag_dict.get(tag, wordnet.NOUN)
        new.append(wnl.lemmatize(i,pos))      
    return new
mission2.end()

mission3=td.Mission('Text Process')
df_fl.loc[:,"cleaning"] = df_fl["tweets"]
df_fl.loc[:,"cleaning"]  = [deEmojify(i) for i in df_fl["cleaning"]]
df_fl.loc[:,"cleaning"]   = df_fl["cleaning"].apply(lambda tweet: removeURLs(tweet))
df_fl.loc[:,"cleaning"]  = [i.lower() for i in df_fl["cleaning"]]
df_fl.loc[:,"cleaning"]   = df_fl["cleaning"].apply(lambda tweet: tokenizer.tokenize(tweet))
df_fl.loc[:,"cleaning"]   = [deleterefer(i) for i in df_fl["cleaning"]]
df_fl.loc[:,"cleaning"]  = [drop_stop(i) for i in df_fl["cleaning"]]
df_fl.loc[:,"cleaning"]  = [lemmatizeWords(i) for i in df_fl["cleaning"]]
print('Check cleaned Data Structure and samples: \n')
df_fl.info()
print('\n',df_fl.head())
mission3.end()

mission4=td.Mission('Export to Excel')
df_fl.to_excel(expath.path,index=False)
mission4.end()
