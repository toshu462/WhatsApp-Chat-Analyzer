import pandas as pd
import re

def data_preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s[A|P]M\s-\s'
    ext_data = re.split(pattern,data, maxsplit = 1)
    date_time = re.findall(pattern,data)
    
    ext_data = re.split(pattern,data)[1:]
    
    df = pd.DataFrame({'messages':ext_data,'datetime':date_time})
    df.drop(df.index[0],axis=0,inplace=True)
    
    user = []
    messages_info = []
    message_text = []
    for message in df['messages']:
        message_data = re.split(r'([\w\W]+?):\s',message)
        messages_info.append(message_data)
    for i in range(len(messages_info)): 
        user.append(messages_info[i][1])
        message_text.append(messages_info[i][2])
        
    df['user'] = user
    df['message'] = message_text
    
    df.drop('messages',axis = 1, inplace = True)
    
    df['datetime'] = pd.to_datetime(df['datetime'],format= '%m/%d/%y, %I:%M %p - ')

    df['year'] = pd.DatetimeIndex(df['datetime']).year
    df['month'] = pd.DatetimeIndex(df['datetime']).month
    df['month_name'] = pd.DatetimeIndex(df['datetime']).month_name()
    df['date'] = pd.DatetimeIndex(df['datetime']).day
    df['week_day'] = pd.DatetimeIndex(df['datetime']).weekday
    df['weekday_name'] = pd.DatetimeIndex(df['datetime']).day_name()
    df['hour'] = pd.DatetimeIndex(df['datetime']).hour
    df['minute'] = pd.DatetimeIndex(df['datetime']).minute
    
    df.drop('datetime',axis = 1, inplace = True)
    
    return df