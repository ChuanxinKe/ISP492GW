#LIBRARIES
import pandas as pd
import sqlite3
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.casual import TweetTokenizer
from nltk.corpus import wordnet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import TerDec as td # Personal module,needs TerDec.py
############################

mission0=td.Mission('Initial')
dbpath=td.setpath(r'./data/JAMCS_0513.db') #Path tool from TerDec.py
dbpath.askupdate('Path of database') # Ask if path need change. Input y or n.
kwpath=td.setpath(r'./data/key_words.csv')
kwpath.askupdate('Path of key words list')
lwpath=td.setpath(r'./data/location_words.csv')
lwpath.askupdate('Path of location words list')
expath=td.setpath(r'./data/target.xlsx')
expath.askupdate('Path of output excel file')
conn = sqlite3.connect(dbpath.path)
c = conn.cursor()
mission0.end()

mission1=td.Mission("Prepare word lists")
mission1_1=td.Mission('Get filter words (key & location) from csv data')
key_words = pd.read_csv(kwpath.path)
location_words = pd.read_csv(lwpath.path)
keywords_list = ""
location_list=""
print('Key words:\n',key_words)
print('Locations:\n',location_words)

mission1_2=td.Mission('Initial stop words list')
# The complex of tweets needs special words list. We drop punctuations and tokentize before stop words.
# So the im, dont, youre needed. If drop stop words first, there are still other problems.
stop_words = set(stopwords.words('english'))
special_stopwords=['rt','amp','im','u','could','dont','youre','would','uk'] 

mission1_3=td.Mission('Form filter lists and update special stop words')
for index,row in key_words.iterrows():
    keywords_list = keywords_list+row['keywords'] +'|'
    special_stopwords.append(row['keywords'])
keywords_input = keywords_list[:-1] #delete the last '|'
for index,row in location_words.iterrows():
    location_list = location_list+row['location'] +'|'
location_input = location_list[:-1]
stop_words.update(special_stopwords)
mission1.end()

mission2=td.Mission("Get all data from database")
df = pd.read_sql("SELECT * FROM raw_tweets", conn) #Get all data
print('Check Data Structure and first 5:\n')
df.info()
print('\n',df.head())
mission2.end()

mission3=td.Mission('Filter by multiple constrains')
df_kw=df.loc[df['tweets'].str.contains(keywords_input,flags=re.IGNORECASE, regex=True)]
df_kw_have=df_kw.loc[pd.notna(df_kw['user_location'])]
df_kw_nan=df_kw.loc[pd.isna(df_kw['user_location'])]
df_fl_1=df_kw_have.loc[df_kw_have['user_location'].str.contains(location_input,flags=re.IGNORECASE, regex=True)]
df_fl_2=df_kw_nan.loc[df_kw_nan['tweets'].str.contains(location_input,flags=re.IGNORECASE, regex=True)]
df_fl=df_fl_1.append(df_fl_2)
mission3.end()

mission4=td.Mission('Drop duplicates, format Date')
df_fl.drop_duplicates(subset='tweets', inplace=True)
df_fl.loc[:,'timestamp_ms'] = pd.to_datetime(df_fl['timestamp_ms'],unit='ms')
print('Check Filtered Data Structure: \n')
df_fl.info()
print(df_fl.head())
mission4.end()

mission5=td.Mission('Setup text processing functions')
def deEmojify(inputString): 
    return inputString.encode('ascii', 'ignore').decode('ascii')
def drop_at_url(inputString):
    #From string to list, after processing back to string. Not efficient, but work and fit other processes
    cached=inputString.split()
    new=[]
    for i in cached:
        if "@" in i or r"http:/" in i or r"https:/" in i:
            pass
        else:
            new.append(i)
    outstring=" ".join(new)
    return outstring
def drop_stop(lists):
    #You can add stop words by the golbal variable, stop_words 
    new=[]
    global stop_words
    for i in lists:
        if i not in stop_words:
            new.append(i)
    return new
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
tokenizer=TweetTokenizer()
wnl = WordNetLemmatizer()
mission5.end()

mission6=td.Mission('Text processes')
mission6_1=td.Mission('Lowcase, drop emoji')
df_fl.loc[:,"cleaning"] = df_fl["tweets"]
df_fl.loc[:,"cleaning"]  = [deEmojify(i) for i in df_fl["cleaning"]]
df_fl.loc[:,"cleaning"]  = [i.lower() for i in df_fl["cleaning"]]

mission6_2=td.Mission('Drop url, retweet_at and punctuation')
df_fl.loc[:,"cleaning"]   = [drop_at_url(i) for i in df_fl["cleaning"]]

mission6_3=td.Mission('Drop punctuation')
df_fl.loc[:,"cleaning"] = [re.sub('[^a-zA-Z]', ' ',i) for i in df_fl["cleaning"]]

mission6_4=td.Mission('Tokenize')
df_fl.loc[:,"cleaning"] = df_fl["cleaning"].apply(lambda tweet: tokenizer.tokenize(tweet))
mission6_4.end()

mission6_5=td.Mission('Lemmatize')
df_fl.loc[:,"cleaning"] = [lemmatizeWords(i) for i in df_fl["cleaning"]]
mission6_5.end()

mission6_6=td.Mission('Drop stop words')
df_fl.loc[:,"cleaning"] = [drop_stop(i) for i in df_fl["cleaning"]]

print('\nPrint cleaned Data:')
df_fl.info()
print('\n',df_fl.head())
mission6.end()

mission7=td.Mission('Get Vader sentiment intensity scores')
analyzer = SentimentIntensityAnalyzer()
df_fl.loc[:,"compound"] = [analyzer.polarity_scores(i)['compound'] for i in df_fl["tweets"]]
mission7.end()

mission8=td.Mission('Export to Excel')
df_fl.to_excel(expath.path,index=False)
mission8.end()