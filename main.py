# pip install snscrape pandas tqdm textblob

import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter
from textblob import TextBlob

# twitter account you want to analyze
twitter_user = "naval"

# use snscrape to scrape the last 100 tweets from the twitter account you specified 
scraper = sntwitter.TwitterSearchScraper(f"from:{twitter_user}")

tweets_list = []

for tweet in scraper.get_items():
    if len(tweets_list) >= 100:
        break
    tweets_list.append([tweet.date, tweet.rawContent, tweet.likeCount, tweet.retweetCount])

# convert the list to a pandas df
tweets_df = pd.DataFrame(tweets_list, columns=['date', 'text', 'likes', 'retweets'])

# clean the text data
tweets_df['text'] = tweets_df['text'].str.replace('\n', '')
tweets_df['text'] = tweets_df['text'].str.replace('http\S+|www.\S+', '', case=False)

# define a function to get the polarity and subjectivity of a text
# polarity is a float which lies between [-1, 1] where 1 means positive and -1 means negative
# subjectivity is a float which lies between [0, 1] where it says if sentences generally refer to personal opinion, emotion, or judgment where objectivity refers to factual information

def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return sentiment, subjectivity

# apply the function to the text column of the DataFrame
tweets_df[['sentiment', 'subjectivity']] = tweets_df['text'].apply(get_sentiment).apply(pd.Series)

# export the df to a csv file
tweets_df.to_csv(f'{twitter_user}_sentiment.csv', index=False)
