# covidtwittersentiment
GENERAL:

This repository included the required files for serving the web app UI, as well as additional files relating to my larger research goal twitter sentiment analysis.

The web app can run locally by cloning this repository, navigating to that folder in your terminal, and running “$python flask_app.py.”

Be sure that it is python3.7 or higher.


The python class for tweet analyzing is located in tweet_processor.py

“Tweets.json” and “twitter_auth.py” are not required however

Finally -- Be sure you have the following packages and libraries installed on you local machine, should you wish to run this locally:

To check, navigate your terminal to the source folder and:
“$ pip install requirements.txt”


TWEET_PROCESSOR:

Tweet processing begins with the twitter API. I used the Tweepy library to take advantage of the Cursor method, which allows me to scrape a sample of tweets. I also have to use the google maps API to convert string location lat/lon pairs for the heatmap eventually.

**Please Note**
-- I am using these APIs for free. This means that I am on their most basic plan and have very, very low limits and speeds. For example, the lookback is only a max of 8 days as the API does not provide more. Also a request with a sample size above 500/day can take long just for API processing. Expect to wait a minute or two after generating something. Go get a coffee!

After scraping tweets, I parse them into a pandas dataframe to allow easy grouping and pivoting of data.

One method I’d like to highlight is get_tweet_range_df(). This method gets a full dataframe of n random samples per day in lookback. It uses the tweet_sentiment_score() method. This is where the NLP polarity scoring takes place. For this I decided to use TextBlob’s NLP polarity scored of text method. TextBlob can be very powerful! For more https://textblob.readthedocs.io/en/dev/index.html

WEB_APP

For the web app, I used python flask, html, javascript, css, and json


