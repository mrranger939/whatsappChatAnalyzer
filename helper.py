from urlextract import URLExtract
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
