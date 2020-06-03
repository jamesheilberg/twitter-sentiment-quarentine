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

For the web app, I used python flask, html, javascript, css, and json, along with a bunch of packages. Dont worry, the packages are included when running the virtual env locally.

WEB_APP INSTRUCTIONS:

I decided to use a simple csv as my database for the ease of implementation. I am confindent that querying from the csv will provide a fast enough experience client end.

For the time series visualization, and the google maps visualization the user has a choice in how many days before today to lookback. For example a look back of 7 will look from all of yesterday, up to and including 7 days before.

The tweets per day is a setting that allows the user to select how many tweets should be sampled in each days bucket when computing average tweet sentiment per day.

The sentiment value is a number -1 to 1 where -1 is the worst sentiment and 1 is the best. For the most part, I have noticed that average sentiment is usually positive, but I will keep monitoring.

In the google maps visualization, sentiment by location is displayed in heatmap format. Red hot locations are positive, green is negative, and yellow is neutral by default.

I know some users find the default color scheme a bit confusing. The color scheme can be changed however on the map.


FINAL NOTES:

This project has taken a good majority of 2 weeks for me. I was very comfortable with the data handling and analysis coming in, but I was weaker in javascript and html. As I progressed through the project however, I became more comfortable with these languages.

In the future, I would like to re-write certain parts of my app to accomodate a growing and automatically updating sqlite database. I could do this by streaming tweets in, which would enable the app to handle much larger tweets per day values, and ultimatly farther lookbacks.

Thank you very much for visiting!


