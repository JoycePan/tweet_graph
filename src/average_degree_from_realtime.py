import json
import os
import sys
import re
from datetime import datetime
from dateutil import parser
from tweet_parser import *
from graph_LRU_edge_cache import *
from graph_adjacent_set_cache import *

# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class AvgDegreeGenerator:

  def __init__(self, raw_tweet_file_name, ft1_file_name, ft2_file_name):
    self.raw_tweet_file_name = raw_tweet_file_name
    self.ft1_file_name = ft1_file_name
    self.ft2_file_name = ft2_file_name
    self.tweet_parser = TweetParser()
    self.edge_cache = GraphLRUEdgeCache()
    self.adj_graph_cache = GraphAdjacentSetCache()
    self.start_time = None
    self.is_start = False

    # clear the context
    ft1 = open(self.ft1_file_name, 'w')
    ft2 = open(self.ft2_file_name, 'w')
    ft1.close()
    ft2.close()

  def parse_tweet_and_generate_degree(self, line):
    parsed_tweet, cur_time = self.parse_one_tweet_and_generate_degree(line)
    if None != parsed_tweet: 
      ft1 = open(self.ft1_file_name, 'ab')
      ft1.write(parsed_tweet + '\n')
      ft1.close()
      if False == self.is_start:
        self.start_time = cur_time
        self.is_start = True
      elif (cur_time - timedelta(seconds = 60) > self.start_time):
        ft2 = open(self.ft2_file_name, 'ab')
        if 0 == len(self.adj_graph_cache.cache):
          ft2.write(str(0) + '\n')
        else:
          ft2.write(format(2.0 * len(self.edge_cache.cache) / len(self.adj_graph_cache.cache), '.2') + '\n')
        ft2.close()

  def parse_one_tweet_and_generate_degree(self, line):
    tweet_json = json.loads(line)
    text, time = self.tweet_parser.parse_raw_tweet(tweet_json)
    if None != text:
      hashtag_pair_list = self.tweet_parser.get_hashtag_pair_list(text)
      time_format = self.tweet_parser.get_datetime(time)
      remove_list = self.edge_cache.set_hashtag_pair_list(hashtag_pair_list, time_format)
      self.adj_graph_cache.set_hashtag_pair_list(hashtag_pair_list)
      self.adj_graph_cache.remove_hashtag_pair(remove_list)
      return (text + ' (timestamp: ' + time + ')'), time_format
    return None, None

class StdOutListener(StreamListener):
    """ A listener handles tweets that are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, filename, generator):
        self.filename = filename
        self.generator = generator
        f = open(self.filename, 'w')
        f.close()

    # this is the event handler for new data
    def on_data(self, data):
        if not os.path.isfile(self.filename):    # check if file doesn't exist
            f = file(self.filename, 'w')
            f.close()
        with open(self.filename, 'ab') as f:
            # print "writing to {}".format(self.filename)
            f.write(data)
            self.generator.parse_tweet_and_generate_degree(data)
        f.closed
        
    # this is the event handler for errors    
    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    # authentication from the credentials file above
    twitter_file = open(sys.argv[1])  
    twitter_cred = json.load(twitter_file)
    twitter_file.close()
    auth = OAuthHandler(twitter_cred["consumer_key"], twitter_cred["consumer_secret"])
    auth.set_access_token(twitter_cred["access_token"], twitter_cred["access_token_secret"])

    generator = AvgDegreeGenerator(sys.argv[2], sys.argv[3], sys.argv[4])
    listener = StdOutListener(sys.argv[2], generator)

    print "Use CTRL + C to exit at any time.\n"
    stream = Stream(auth, listener)
    stream.filter(locations=[-180,-90,180,90]) # this is the entire world, any tweet with geo-location enabled