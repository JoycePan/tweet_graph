import unittest
import os
import datetime
import dateutil
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src/')
from tweet_parser import *

class TestTweetParser(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(TestTweetParser, self).__init__(*args, **kwargs)
    self.tweet_parser = TweetParser()
    self.file_dir = os.path.dirname(os.path.realpath(__file__))

  def test_parse_raw_tweet(self):
    with open(self.file_dir + '/raw_tweet.txt') as f:
      raw_tweet = json.load(f)
      text, date_string = self.tweet_parser.parse_raw_tweet(raw_tweet)
      self.assertEqual(text, "I'm at Terminal de Integrao do Varadouro in Joo Pessoa, PB https://t.co/HOl34REL1a")
      self.assertEqual(date_string, "Sun Nov 01 23:34:40 +0000 2015")

  def test_parse_raw_tweet_with_abnormal_tweet(self):
    with open(self.file_dir + '/raw_tweet_abnormal.txt') as f:
      raw_tweet = json.load(f)
      text, date_string = self.tweet_parser.parse_raw_tweet(raw_tweet)
      self.assertEqual(text, None)
      self.assertEqual(date_string, None)

  def test_get_datetime(self):
    date_string = "Sun Nov 01 23:34:40 +0000 2015"
    date = self.tweet_parser.get_datetime(date_string)
    self.assertEqual(date, datetime.datetime(2015, 11, 1, 23, 34, 40, tzinfo=dateutil.tz.tzutc()))

  def test_get_hashtag_pair_list(self):
    text = "Just saw a great post on Insight Data Engineering #Apache #Hadoop #Storm #Storm"
    hashtag_pair_list = self.tweet_parser.get_hashtag_pair_list(text)
    self.assertEqual(hashtag_pair_list, [('#apache', '#hadoop'), ('#apache', '#storm'), ('#hadoop', '#storm')])

  def test_get_hashtag_pair_list_with_comma(self):
    text = "22h,#reto800risah,#amandapasucasa,#sofiaganadora,#teamsofia"
    hashtag_pair_list = self.tweet_parser.get_hashtag_pair_list(text)
    self.assertEqual(hashtag_pair_list, [('#amandapasucasa', '#reto800risah'), \
      ('#amandapasucasa', '#sofiaganadora'), ('#amandapasucasa', '#teamsofia'), \
      ('#reto800risah', '#sofiaganadora'), ('#reto800risah', '#teamsofia'), ('#sofiaganadora', '#teamsofia')])

if __name__ == '__main__':
    unittest.main()