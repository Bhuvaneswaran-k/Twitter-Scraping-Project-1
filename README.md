# Twitter-Scraping-Project-1
# snscrape

snscrape is a scraper for social networking services (SNS). It scrapes things like user profiles, hashtags, or searches and returns the discovered items, e.g. the relevant posts.

The following services are currently supported:

Facebook: user profiles, groups, and communities (aka visitor posts)\
Instagram: user profiles, hashtags, and locations\
Reddit: users, subreddits, and searches (via Pushshift)\
Telegram: channels\
Twitter: users, user profiles, hashtags, searches, tweets (single or surrounding thread), list posts, and trends\

# Requirements
snscrape requires Python 3.8 or higher. The Python package dependencies are installed automatically when you install snscrape.
# Installation
          pip3 install snscrape
          pip3 install streamlit
          pip3 install pymongo
  incase if you use pycharm click on python pakages below the console and search streamlit,snscrape and pymongo then click install respectively. 

# How to use Twitter scraping 

1. Type the keyword you want to search for the tweets
2. Select the date range for which the tweets need to be displayed
3. Enter the number of tweets to be displayed 
4. click on Download CSV button or json button  to dowload the file
5. Or else click export button to export the data to MongoDB
6. Click on Search button
7. After the tweets are displayed 
8. if you want to download data means click on download or click on export 

# Sample Input
![name](https://user-images.githubusercontent.com/117283354/214275851-80b35ae8-a009-428f-9bdc-379856e35d2c.jpg)

# output in csv
![output_csv](https://user-images.githubusercontent.com/117283354/214276311-61622624-9b64-4396-aea4-558cac6929f1.jpg)
# output in json
![input_json](https://user-images.githubusercontent.com/117283354/214276475-df4f661d-c767-4449-8ff2-a326e1e739c1.jpg)
# output in export
![output_export](https://user-images.githubusercontent.com/117283354/214276621-29d61f7d-76b5-494c-82fb-9680df14de1e.jpg)

