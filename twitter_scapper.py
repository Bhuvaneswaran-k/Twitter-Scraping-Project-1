import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo
import datetime
from datetime import date
import time

st.set_page_config(
    page_title="Twitter Scraper",
    page_icon="chart_with_upwards_trend",
layout="wide")

Header = st.container()
with Header:
    st.sidebar.title("""
    Please enter your requirement
    """)
st.title("""
    Twitter Scrapping using Snscrape and Streamlit:
    """)


today=date.today()
NAME = st.sidebar.text_input('What do you want to search for?')
search_radio = st.sidebar.radio('Type of search',['Username', 'hashtag', 'Messages'])
search_type=''
if search_radio=="Username":
    Search_type="from"
elif search_radio=="hashtag":
    search_type="#"
else:
    search_type=" "
count = st.sidebar.number_input('Enter the limit',min_value=0)
start_date=st.sidebar.date_input('enter the start date',datetime.date(2022, 1, 1))
end_date=st.sidebar.date_input('enter the end date',today)

csv = st.sidebar.radio("Download option", ['CSV', 'Json', 'Export'])

count = int(count)
submit_button = st.sidebar.button(label='Search')

tweets_list1 = []

if submit_button:
    for i , tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_type}:{NAME} since:{start_date} until:{end_date}').get_items()):
        if i > count-1:
            break
        tweets_list1.append(
            [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.likeCount, tweet.retweetCount,
             tweet.sourceLabel, tweet.user.location])
        tweet_df = pd.DataFrame(tweets_list1, columns=["Date", "Id", "Content", "Username", "LikeCount", "RetweetCount",
                                                       "SourceLabel", "Location"],index=None)

    st.dataframe(tweet_df)


    st.success("you have Extracted the data ")

    if csv == "CSV":
        file_converted = tweet_df.to_csv()
        st.download_button(
            label="Download data as CSV",
            data=file_converted,
            file_name=f'{NAME}_Twitter.csv',
            mime='text/csv',
        )
    elif (csv == 'Json'):
        file_converted = tweet_df.to_json()
        st.download_button(
            label="Download data as json",
            data=file_converted,
            file_name=f'{NAME}_Twitter.json',
            mime="application/json",
        )
    elif csv == "Export":
        export_button = st.button(label="Export")
        now = datetime.datetime.now()
        client = pymongo.MongoClient("mongodb+srv://bhuvaneswarank:Krishna12@cluster0.7hwuocf.mongodb.net/?retryWrites=true&w=majority")
        db = client.Tweeter_scrap
        records = db.Scrap_data
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_type}:{NAME}  since:{start_date} until:{end_date}').get_items()):
            if i > count - 1:
                break
            tweets_list1.append(
                [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.likeCount, tweet.retweetCount,
                 tweet.sourceLabel, tweet.user.location])
            tweet_df = pd.DataFrame(tweets_list1,
                                    columns=["Date", "Id", "Content", "Username", "LikeCount", "RetweetCount",
                                             "SourceLabel", "Location"], index=None)
            l = {"Scraped_Name": NAME, "Time": now, "Scraped_data": [
                    {"Date_Time": tweet.date, "Tweet_ID": tweet.id, "Tweet_content": tweet.content,
                     "Username": tweet.user.username,
                     "Like Count": tweet.likeCount, "ReTweet Count": tweet.retweetCount, "Source": tweet.sourceLabel,
                     "Location": tweet.user.location}]}
            records.insert_one(l)
            if export_button:
                st.success("Data has uploaded in Mongodb Server")