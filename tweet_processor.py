import tweepy
from tweepy import *
from tweepy.auth import OAuthHandler
from tweepy.streaming import StreamListener

import numpy as np
import pandas as pd

from datetime import datetime, timedelta
from textblob import TextBlob

from googlemaps import *

import re
import csv

import matplotlib.pyplot as plt

class TwitterSentimentAnalysis():
    # This class will handle everything that is part getting a sentiment analysis
    
    def __init__(self):
        
        consumer_key = "3LntKM9D0jXZbKhE9G0ek63Ar"
        consumer_secret = "QNXlkRAUrCRiiEZacnSEnRW4Oeze3h5romq0YG48IPsb62BuoA"

        access_token = "1252051453474111491-MLxtYXJAicSFnWI0pfJiFxOd6OhICJ"
        access_token_secret = "nMjIIjMyqsMxnRUlpiOGCGOPsWCuRgByNTH3E5LS1AAS0"
        
        self.search_words = "#quarentine -filter:retweets"
        self.today = datetime.now()
        
        try:
            # handle authentication and possible issues
            
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = API(self.auth, wait_on_rate_limit=True)
            
        except:
            print("Twitter Authentication Failed! Check API")
            raise Exception()
            
        try:
            self.gmaps = Client(key='AIzaSyCdBA39xq1V7E7olkINdWijGe7bRX9UZkg')
        except:
            
            print("GMAPS Authentication Failed! Check API")
            raise Exception()
    
    def parse_tweet(self, tweet):
        # A regular expression, to clean tweets
        # This will ultimatly remove links or any special character that may interfere with NLP
        ### REMEMBER: we want a sentiment of the text, not anything linked to it
        
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    

    def tweet_sentiment_score(self, tweet):
        # This will score the tweets sentiment based on textblob's sentiment method
        # more information can be found out about textblob in the documentation
        # link here: https://textblob.readthedocs.io/en/dev/index.html
        
        # TextBlob object <-- a
        a = TextBlob(self.parse_tweet(tweet))
        
        '''
        #for debugging
        
        if a.sentiment.polarity > 0:
            print('positive')
        elif a.sentiment.polarity == 0:
            print('neutral')
        else:
            print('negative')
        '''
            
        return a.sentiment.polarity
    
    def get_df_sentiments(self, dataframe):

        df = dataframe.copy()

        try:        
            df['sentiment'] = [self.tweet_sentiment_score(tweet) for tweet in df['tweet']]
        except:
            print("error collection sentiment (is dataframe intitialized?)")
            raise Exception()

        return df
    
    def get_tweet_range_df(self, lookback, tweets_per_day, senti=True, cleanloc=True, getCentroid=True):
        # lookback = days to look back from
        # last day = end of looking period, set to today
        # resultion = tweets per day that will come up
        df = pd.DataFrame()
        
        ed = self.today
        sd = self.today - timedelta(days=lookback)
        day = timedelta(days = 1)

        days = 0
        
        # This will get us a 'random' sample of tweets each day from all across the globe
        # CONSTRAINT: MUST BE ENGLISH AND HAVING TO DO WITH QUARENTINE
        while sd < ed:
            days += 1
    
            #print(str(start_date)[:10])
            tweets = tweepy.Cursor(self.api.search,
                          q=self.search_words,
                          lang="en",
                          since=str(sd)[:10],
                          until=str(sd + day)[:10]).items(tweets_per_day)

            sd += day

            users_locs = [[
                tweet.text,
                tweet.user.screen_name,
                tweet.user.location,
                tweet.created_at,
                tweet.favorite_count] for tweet in tweets]

            dfAppend = pd.DataFrame(data=users_locs, columns=['tweet', 'user', "location", "created", "likes"])

            #print(dfAppend)

            df = df.append(dfAppend, ignore_index=True)
        #print(days)
        
        if senti:
            # add sentiment to our dataframe
            
            df = self.get_df_sentiments(df)
            
        #country_list = []
        lats = []
        lons = []
            
        if cleanloc:
            # This condition will get a lat/lon pair for the location proiveded if google maps can process it
            # if not it will remain Nan
            c = 0
            #coordSet = False
            for loc in df['location']:
                #coordSet = False
                c += 1
                #print("itter")
                    #we can use the tweet parser to also parse the addresses
                 #   print(loc)

                if loc == '': 
                    #country_list.append(np.nan)
                    lats.append(np.nan)
                    #print("adding nan to lat, itter: " + str(c))
                    lons.append(np.nan)
                    continue
                    
                gmapsRETURN = self.gmaps.geocode(loc)

                la = []
                lo = []

                count = 0

                try:
                    #x = gmapsRETURN[0]['address_components']
                    y = gmapsRETURN[0]['geometry']['bounds']
                    
                except:
                    #print("adding nan to lat, itter: " + str(c))
                    lats.append(np.nan)
                    lons.append(np.nan)
                    #country_list.append(np.nan)
                    #print('nanE')
                    continue
                
                '''   
                for item in gmapsRETURN[0]['address_components']:
                    if item['types'] == ['country', 'political']:
                        print(item['long_name'])
                        country_list.append(item['long_name'])
                '''
                for item in gmapsRETURN[0]['geometry']['bounds']:
                    for latlon in gmapsRETURN[0]['geometry']['bounds'][item]:
                        if count%2 == 0:
                            la.append(gmapsRETURN[0]['geometry']['bounds'][item][latlon])
                        else:
                            lo.append(gmapsRETURN[0]['geometry']['bounds'][item][latlon])
                        count += 1

                la = round(sum(la)/len(la), 3)
                lo = round(sum(lo)/len(lo), 3)

                #print("adding "+ str(la) +" to lat, itter: " + str(c))
                lats.append(la)
                lons.append(lo)
                continue

        #print(len(df))
        #print(len(lats), len(lons))
        #df['country'] = country_list
        df['centroid_lats'] = lats
        df['centroid_lons'] = lons
        
        return df
    
    def update(self, df, filepath='csvFiles/tweets.csv'):
        return df.to_csv(filepath, index=False)
    
    def read_csv(self, fname='csvFiles/tweets.csv'):
        df = pd.read_csv(fname)
        df['created'] = pd.to_datetime(df['created'])
        return df
    
    def get_by_date(self, df, lookback):
        firstd = self.today - timedelta(days=lookback)
        df = df[(df['created']>firstd) & (df['created']<self.today)]
        df = df.resample('D', on='created').mean()
        del df['likes']
        
        return df
        
    def get_by_country(self, df):
        df = df[df['country'].notna()]
        df = df.reset_index(drop=True)
        df = df.groupby('country').agg({'sentiment':'mean'}).reset_index()
        
        return df
    
    def get_dates_as_list(self, df):
        return [str(item)[:10] for item in df.index.to_series()]
    
    def get_lat_lons_and_senti(self, df, lookback):
        df = df[['sentiment', 'centroid_lats', 'centroid_lons', 'created']]
        df = df[df['centroid_lats'].notna()]
        df = df.reset_index(drop=True)
        df['heatmap_weight'] = [(2.5*senti+2.5) for senti in df['sentiment']]
        
        firstd = self.today - timedelta(days=lookback)
        df = df[(df['created']>firstd) & (df['created']<self.today)]
        df = df[['sentiment', 'centroid_lats', 'centroid_lons', 'created', 'heatmap_weight']]
        return df

    def get_sentiment_as_list(self, df):
        return [item for item in df['sentiment']]