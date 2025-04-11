from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
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
    wc = WordCloud(width=500, height=500 ,min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=' '))
    return df_wc