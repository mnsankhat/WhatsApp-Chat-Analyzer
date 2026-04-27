import pandas as pd
import re

def preprocess(data):
    data = data.replace('\u202f', ' ')

    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    pattern1 = r"\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[AP]M\s-\s"



    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if not messages:
        messages = re.split(pattern1, data)[1:]
        dates = re.findall(pattern1, data)
    elif not dates:
         messages = re.split(pattern1, data)[1:]
         dates = re.findall(pattern1, data)



    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # convert to string BEFORE .str
    df['message_date'] = df['message_date'].astype(str)
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ', regex=False)

    # convert to datetime
    df['date'] = pd.to_datetime(
        df['message_date'],
        format='%d/%m/%y, %I:%M %p - ',
        errors='coerce'
    )

    users = []
    msgs = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            msgs.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs

    df.drop(columns=['user_message', 'message_date'], inplace=True)


    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    return df
