import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'      
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates_clean = []
    for timestamp in dates:
        clean_timestamp = timestamp.replace('\u202f', ' ')
        dates_clean.append(clean_timestamp)
    dates_clean
    df = pd.DataFrame({'user_message': messages, 'message_date': dates_clean})
    df['datetime'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')
    df = df.drop(['message_date'], axis=1)
    df.rename(columns={'datetime': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group Notification')
            messages.append(entry[0])
    df['users'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    return df

