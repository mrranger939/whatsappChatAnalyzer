from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
def fetch_stats(SelectedUser, df):
    extractor = URLExtract()
    if SelectedUser != 'Overall':
        df = df[df['users'] == SelectedUser]

    # no.of messages
    numMsgs = df.shape[0]
    # no.of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    numWords = len(words)
    #no.of media files init
    numMedia = df[df['message'] == '<Media omitted>\n'].shape[0]
    #no.of links
    links = []
    for msgs in df['message']:
        links.extend(extractor.find_urls(msgs))
    numLinks = len(links)
    return numMsgs, numWords, numMedia, numLinks
def mostBusyUsers(df):
    x = df['users'].value_counts().head()
    newDf = round((df['users'].value_counts().head()/df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'users': 'percent'})

    return x, newDf

def createWordCloud(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['users'] == selectedUser]
    f = open('./stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selectedUser != 'Overall':
        df = df[df['users'] == selectedUser]
    temp = df[df['users'] != 'group Notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]
    def removeStopWords(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)
        
    wc = WordCloud(width=500, height=500 ,min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(removeStopWords)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc
def mostCommonWords(selectedUser, df):
    f = open('./stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selectedUser != 'Overall':
        df = df[df['users'] == selectedUser]
    temp = df[df['users'] != 'group Notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))

def emojiHelper(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['users'] == selectedUser]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

def monthlyTimeline(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['users'] == selectedUser]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def dailyTimeline(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['users'] == selectedUser]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def weekActivityMap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['users'] == selectedUser]
    return df['day_name'].value_counts()

def monthActivityMap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['users'] == selectedUser]
    return df['month'].value_counts()    

def dailyActivityMap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['users'] == selectedUser]
    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)