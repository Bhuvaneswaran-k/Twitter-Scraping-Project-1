import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo
import datetime
from datetime import date

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

if 'active_state' not in st.session_state:
    st.session_state.active_state=False

today=date.today()
NAME = st.sidebar.text_input('What do you want to search for?')
search_radio = st.sidebar.radio('Type of search',['Username', 'hashtag', 'Messages'])
search_type=''
if search_radio=="Username":
    Search_type="from"
elif search_radio=="Hashtag":
    search_type="#"
else:
    search_type=" "
count = st.sidebar.number_input('Enter the limit',min_value=0)
start_date=st.sidebar.date_input('enter the start date',datetime.date(2022, 1, 1))
end_date=st.sidebar.date_input('enter the end date',today)

csv = st.sidebar.checkbox('Download',value=True)
csv1 = st.sidebar.checkbox('Export')
count = int(count)
submit_button = st.sidebar.button(label='Search')

tweets_list1 = []

if submit_button or st.session_state.active_state:
    st.session_state.active_state=True
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
    # aranging buttons in side by side position
    col1, col2, col3 = st.columns([6, 6, 6])

    if csv or st.session_state.active_state:
        st.session_state.active_state=True
        file_converted = tweet_df.to_csv()
        col1.download_button(
            label="Download data as CSV",
            data=file_converted,
            file_name=f'{NAME}_Twitter.csv',
            mime='text/csv',
        )
        file_converted = tweet_df.to_json()
        col2.download_button (
            label="Download data as json",
            data=file_converted,
            file_name=f'{NAME}_Twitter.json',
            mime="application/json",
        )
if csv1  :
    export_button = col3.button(label="Export to our MongoDB server")
    st.session_state.active_state=True

    now = datetime.datetime.now()
    client = pymongo.MongoClient("mongodb+srv://bhuvaneswarank:Krishna12@cluster0.7hwuocf.mongodb.net/?retryWrites=true&w=majority")
    db = client.Tweeter_scrap_review
    records = db.Scrap_data
    if export_button :
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search_type}:{NAME}  since:{start_date} until:{end_date}').get_items()):
            if i > count-1:
                break
            tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.likeCount, tweet.retweetCount,tweet.sourceLabel, tweet.user.location])
            l = {"Scraped_Name": NAME, "Time": now, "Scraped_data": [
                        {"Date_Time": tweet.date, "Tweet_ID": tweet.id, "Tweet_content": tweet.content,
                         "Username": tweet.user.username,
                         "Like Count": tweet.likeCount, "ReTweet Count": tweet.retweetCount, "Source": tweet.sourceLabel,
                         "Location": tweet.user.location}]}
            records.insert_one(l)
        st.success("Data has uploaded in our Mongodb Server")