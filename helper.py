from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACHING_V2"]="true"
def chat_summary(chat):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "I give you some whatsapp chat. give me summary of these chat in 100 words. chat append here:"),
            ("user", f"Chat:{chat}")
        ]
    )
    # prompt = "I give you some whatsapp chat. give me summary of these chat in 100 words. chat append here:"
    llm=Ollama(model="llama3")
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    response=chain.invoke({'chat':chat})
    return response


extractor=URLExtract()

def fatch_state(selected_user,df):
    # if selected_user=="Overall":
    #     number_messages=df.shape[0]
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split(" "))
    #
    #     return number_messages, len(words)
    # else:
    #     new_df = df[df['users']==selected_user]
    #     number_messages = new_df.shape[0]
    #     words = []
    #     for message in new_df['message']:
    #         words.extend(message.split(" "))
    #     return number_messages, len(words)

    # States level
    if selected_user!="Overall":
        df = df[df['users']==selected_user]

    #number of messages
    number_messages = df.shape[0]

    #number of words
    words = []
    for message in df['message']:
        words.extend(message.split(" "))

    #number of meida
    number_media = df[df['message']=='<Media omitted>\n'].shape[0]

    #number of links
    y=[]
    for message in df['message']:
        y.extend(extractor.find_urls(message))

    return number_messages, len(words), number_media, len(y)

def busy_user(df):
    x=df['users'].value_counts().head()
    new_df= round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','users':'Percent'})
    return x, new_df

def creat_wordclude(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    temp = df[df['users'] != "Group Notifications"]
    temp = temp[temp['message'] != "<Media omitted>\n"]
    temp = temp[temp['message'] != "This message was deleted\n"]
    temp = temp[temp['message'] != "Waiting for this message\n"]



    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(height=500,width=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def common_word(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user!="Overall":
        df = df[df['users']==selected_user]
    temp = df[df['users'] != "Group Notifications"]
    temp = temp[temp['message'] != "<Media omitted>\n"]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def monthly_timeline(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + '_' + str(timeline['Year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def weekly_activity_map(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    return df['Day_Name'].value_counts()

def monthly_activity_map(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_Name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


def summary(start_date,end_date,df):
    new_df=df.drop(['Year','Month','Day','Hour','Day_Name','Minute','month_num','only_date','period'], axis=1)
    temp = new_df[new_df['users'] != "Group Notifications"]
    temp = temp[temp['message'] != "<Media omitted>\n"]
    temp = temp[temp['message'] != "This message was deleted\n"]
    df = temp[temp['message'] != "Waiting for this message\n"]
    new_df = temp[~temp['message'].isin([""])]


    new_df = new_df[new_df['Date'].between(start_date, end_date)]
    chatlist = new_df.to_string()
    return chatlist




