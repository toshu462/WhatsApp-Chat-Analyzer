from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
 
def stat_fetcher(name,df):
    
    if name != 'All':
        df = df[df['user']==name]

    count_message = df.shape[0]
    words = []
    df1 = df[df['message'] != '<Media omitted>\n']
    for message in df1['message']:
        words.extend(message.split())
        count_words = len(words)


    # fetching count of media shared
    media_files = df[df['message'] == '<Media omitted>\n']
    count_media = len(media_files)
    return count_message, count_words,count_media

def mostactiveuser(df):
    a = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df['user'].shape[0])*100).reset_index().rename(columns = {'index':'Name', 'user':'Active Percent'})
    df['Active Percent'] = df['Active Percent'].astype('int')
    return a, df


def get_wordcloud(name,df):
    if name != 'All':
        df = df[df['user']==name]
    clean_message = df[df['message']!='<Media omitted>\n']
    clean_message = clean_message[clean_message['message']!= 'group notification']
    cloud_word = WordCloud(width = 500, height = 500, min_font_size = 8, background_color = 'skyblue', colormap='rainbow').generate(clean_message['message'].str.cat(sep = ' '))
    
    return cloud_word


def top_used_words(name,df):
    with open('stop_hinglish.txt','r') as f:
        stop_words = f.read()
    if name != 'All':
        df = df[df['user']==name]
    words_most_used = []
    clean_message = df[df['message']!='<Media omitted>\n']
    clean_message = clean_message[clean_message['message']!= 'group notification']
    for message in clean_message['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words_most_used.append(word)
    Top10_used_word_df = pd.DataFrame(Counter(words_most_used).most_common(10),columns=['Words','Count']) 

    return Top10_used_word_df

def get_emoji(name,df):
    if name != 'All':
        df = df[df['user'] == name]
    emoji_list = []
    clean_df = df[df['message']!='<Media omitted>\n']
    clean_df = clean_df[clean_df['message']!= 'group notification']
    for i in clean_df['message']:
        for emo in i:
            if emo in emoji.EMOJI_DATA:
                emoji_list.append(emo)
    Emoji_df = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))),columns = ['Emoji','Count'])
    return Emoji_df


def months(name,df):
    if name != 'All':
        df = df[df['user']==name]

    month_study = pd.DataFrame(df.groupby(['year','month_name']).count()['message'].reset_index())

    period = []    
    for i in range(month_study.shape[0]):
        period.append(str(month_study['year'][i])+"/"+str(month_study['month_name'][i]))

    month_study['period'] = period

    return month_study


def days(name,df):
    if name != 'All':
        df = df[df['user']==name]

    day_study = pd.DataFrame(df.groupby(['month_name','weekday_name']).count()['message'].reset_index())

    period = []    
    for i in range(day_study.shape[0]):
        period.append(str(day_study['month_name'][i])+"/"+str(day_study['weekday_name'][i]))

    day_study['period'] = period

    return day_study


def daily(name,df):

    if name != 'All':
        df = df[df['user'] == name]

    daily_study = df.groupby('date').count()['message'].reset_index()

    return daily_study

def weekly_days(name,df):

    if name != 'All':
        df = df[df['user'] == name]

    return df['weekday_name'].value_counts()

def monthly_analysis(name,df):

    if name != 'All':
        df = df[df['user'] == name]

    return df['month_name'].value_counts()
