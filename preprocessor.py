import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm|AM|PM)\s-\s'     
    messages = re.split(pattern, data, flags=re.IGNORECASE)[1:]
    dates = re.findall(pattern, data)
    dates_clean = []
    for timestamp in dates:
        clean_timestamp = timestamp.replace('\u202f', ' ')
        dates_clean.append(clean_timestamp)
    def parse_date(date_str):
        try:
            # Try MM/DD/YY format with the dash
            return pd.to_datetime(date_str, format='%m/%d/%y, %I:%M %p - ')
        except ValueError:
            try:
                # Try DD/MM/YYYY format with the dash
                return pd.to_datetime(date_str, format='%d/%m/%Y, %I:%M %p - ')
            except ValueError:
                print(f"Failed to parse: {date_str}")
                return pd.NaT

    # Apply the parsing function
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['date'] = df['message_date'].apply(parse_date)

    # Drop the original message_date column
    df = df.drop(['message_date'], axis=1)
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
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))
    df['period'] = period
    return df

