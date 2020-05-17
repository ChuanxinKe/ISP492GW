#LIBRARIES
import pandas as pd
import warnings
from collections import Counter
from ast import literal_eval
from matplotlib import pyplot as plt
from matplotlib import ticker
import seaborn as sns
from wordcloud import WordCloud
import TerDec as td # Personal module,needs TerDec.py
warnings.filterwarnings('ignore')
############################

mission0=td.Mission('Initial')
dbpath=td.setpath(r'./data/target.xlsx') #Path tool from TerDec.py
dbpath.askupdate('Path of data file') # Ask if path need change. Input y or n.
df=pd.read_excel(dbpath.path)
print('Check Data Structure and first 5:\n')
df.info()
print('\n',df.head())
mission0.end()

mission1=td.Mission('Classify sentiment score')
sent_scores_df= pd.DataFrame(df['compound'],columns=['compound'])
sent_scores_df.loc[:,'val'] = sent_scores_df['compound'].apply(lambda x: 'neutral' if x == 0 else ('positive' if x > 0 else 'negative'))
print(sent_scores_df.tail())
mission1.end()

mission2=td.Mission('Draw sentiment scores distribution')
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
sns.distplot(sent_scores_df['compound'], bins=30, ax=ax)
plt.savefig('sentiment_distribution.png')
mission2.end()

mission3=td.Mission('Draw bar chart of sentiment classify count')
sent_counts = pd.DataFrame.from_dict(Counter(sent_scores_df['val']), orient = 'index').reset_index()
sent_counts.columns = ['Sentiment', 'Count']
sns.barplot(y="Count", x='Sentiment', data=sent_counts)
for index, row in sent_counts.iterrows():
    ax.text(row.name,row["Count"]+float(15),row["Count"], color='red', ha="center")
print(sent_counts)
plt.savefig('sentiment.png')
mission3.end()

mission4=td.Mission("Make word list and count frequency")
word_list = []
for index,row in df.iterrows():
    lists=literal_eval(row['cleaning'])
    for i in lists:
        word_list.append(i)
sns.set(style="darkgrid")
counts = Counter(word_list).most_common(50)
counts_df = pd.DataFrame(counts)
counts_df.columns = ['Word', 'Frequency']
print('\n',counts_df.head())
mission4.end()

mission5=td.Mission('Draw bar chart of word count')
ax = plt.subplots(figsize = (14, 14))
ax = sns.barplot(y="Word", x='Frequency', data=counts_df)
for index, row in counts_df.iterrows():
    ax.text(row["Frequency"]+float(5),row.name,row["Frequency"], color='gray',ha='left')
plt.savefig('wordcount_bar.png')
mission5.end()

mission6=td.Mission('Word Cloud of All Words')
wordcloud = WordCloud(
    background_color='black',
    max_words=50,
    max_font_size=50, 
    scale=5,
    random_state=1,
    collocations=False,
    normalize_plurals=False
).generate(' '.join(word_list))
plt.figure(figsize = (12, 10), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.savefig('wordcloud.png')
mission6.end()

mission7=td.Mission('Draw word cloud by sentiment classify')
polar_tweets_df = pd.DataFrame()
polar_tweets_df['wordlist'] = df['cleaning']
polar_tweets_df['val'] = sent_scores_df['val']

positive = polar_tweets_df[polar_tweets_df['val'] == 'positive']['wordlist']
negative = polar_tweets_df[polar_tweets_df['val'] == 'negative']['wordlist']
neutral = polar_tweets_df[polar_tweets_df['val'] == 'neutral']['wordlist']

positive_list = [word for wordlist in positive for word in literal_eval(wordlist)]
negative_list = [word for wordlist in negative for word in literal_eval(wordlist)]
neutral_list = [word for wordlist in neutral for word in literal_eval(wordlist)]
td.printfive(positive_list, 'Resource for drawing positive words cloud')

positive_cloud = WordCloud(
    background_color='black',
    max_words=50,
    max_font_size=50, 
    scale=5,
    random_state=1,
    collocations=False,
    normalize_plurals=False
).generate(' '.join(positive_list))

negative_cloud = WordCloud(
    background_color='white',
    max_words=50,
    max_font_size=50, 
    scale=5,
    random_state=1,
    collocations=False,
    normalize_plurals=False
).generate(' '.join(negative_list))

neutral_cloud = WordCloud(
    background_color='white',
    max_words=50,
    max_font_size=50, 
    scale=5,
    random_state=1,
    collocations=False,
    normalize_plurals=False
).generate(' '.join(neutral_list))

fig, axs = plt.subplots(2, 2, figsize = (20, 12))
fig.tight_layout(pad = 0)

axs[0, 0].imshow(positive_cloud)
axs[0, 0].set_title('Words from Positive Tweets', fontsize = 20)
axs[0, 0].axis('off')

axs[0, 1].imshow(negative_cloud)
axs[0, 1].set_title('Words from Negative Tweets', fontsize = 20)
axs[0, 1].axis('off')

axs[1, 0].imshow(neutral_cloud)
axs[1, 0].set_title('Words from Neutral Tweets', fontsize = 20)
axs[1, 0].axis('off')

axs[1, 1].imshow(wordcloud)
axs[1, 1].set_title('Words from All Tweets', fontsize = 20)
axs[1, 1].axis('off')
plt.savefig('joint_cloud.png')
mission7.end()
