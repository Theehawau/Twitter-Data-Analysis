import json
import pandas as pd
from textblob import TextBlob

def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = [(user.get('user',{})).get(statuses_count, 0) for user in self.tweets_list]
        return statuses_count 
        
    def find_full_text(self)->list:

        texts=[]
        for tweet in self.tweets_list:
            if 'extended_tweet' in tweet.keys():
                texts.append(tweet['extended_tweet']['full_text'])
            elif 'retweeted_status' in tweet.keys():
                if 'quoted_status' in tweet['retweeted_status'].keys():
                    texts.append(tweet['retweeted_status']['text'])
                elif tweet['retweeted_status']['truncated'] == False:
                    texts.append(tweet['retweeted_status']['text'])
                else:
                    texts.append(tweet['retweeted_status']['extended_tweet']['full_text'])
            elif tweet['truncated'] == False:
                texts.append(tweet['text'])
        return texts
       
    
    def find_sentiments(self, text)->list:
        polarity = []
        subjectivity = []
        for txt in text:
              if (txt):
                sentiment = TextBlob(str(txt)).sentiment
                polarity.append(sentiment.polarity)
                subjectivity.append(sentiment.subjectivity)
        
        return polarity,subjectivity

    def find_created_time(self)->list:
        created_at = [tweet['created_at'] for tweet in self.tweets_list]
        return created_at

    def find_source(self)->list:
        return [tweet['source'] for tweet in self.tweets_list]

    def find_screen_name(self)->list:
        screen_name = [tweet['user']['screen_name'] for tweet in self.tweets_list]
        return screen_name
    def find_followers_count(self)->list:
       return [tweet['user']['followers_count'] for tweet in self.tweets_list]

    def find_friends_count(self)->list:
        return [tweet['user']['friends_count'] for tweet in self.tweets_list]
    def is_sensitive(self)->list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = None

        return is_sensitive

    def find_favourite_count(self)->list:
        return [tweet['favorite_count'] for tweet in self.tweets_list]    
    
    def find_retweet_count(self)->list:
        return [tweet['retweet_count'] for tweet in self.tweets_list]

    def find_hashtags(self)->list:
        hashtags=[]
        for tags in [tweet['entities']['hashtags'] for tweet in self.tweets_list]:
            tag = [x['text'] for x in tags[:]]
            hashtags.append(tag) if len(tag) > 0 else hashtags.append('')
        return hashtags
    def find_mentions(self)->list:
        return [tweet['entities']['user_mentions'] for tweet in self.tweets_list]

    def find_location(self)->list:
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''
        
        return location
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("../covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above

    
