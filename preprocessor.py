import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[apAP][mM]\s-\s'
    pattern2 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[apAP][mM]\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern2, data)
    df = pd.DataFrame({'User_Message': message, 'Message_Dates': dates})
    df['Message_Dates'] = pd.to_datetime(df['Message_Dates'], format='%d/%m/%y, %I:%M\u202f%p ')
    df.rename(columns={'Message_Dates': 'Date'}, inplace=True)
    users = []
    messages = []
    for message in df['User_Message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notifications')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns='User_Message', inplace=True)
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Day_Name']=df['Date'].dt.day_name()
    df['Minute'] = df['Date'].dt.minute
    df['month_num'] = df['Date'].dt.month
    df['only_date'] = df['Date'].dt.date

    period = []
    for hour in df[['Day_Name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df

def preprocess1(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'User_Message': message, 'Message_Dates': dates})
    # convert message_date type
    df['Message_Dates'] = pd.to_datetime(df['Message_Dates'], format='%d/%m/%Y, %H:%M - ')

    df.rename(columns={'Message_Dates': 'Date'}, inplace=True)

    users = []
    messages = []
    for message in df['User_Message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns='User_Message', inplace=True)
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Minute'] = df['Date'].dt.minute
    df['month_num'] = df['Date'].dt.month
    df['only_date'] = df['Date'].dt.date

    period = []
    for hour in df[['Day_Name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
