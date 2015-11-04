import json
import re
import string
from dateutil import parser

class TweetParser:
  """ A tweet parser that can parse raw tweets, get datetime from string of datetime,
  get a list of hashtag pair from a tweet context
  """

  # Return tweet context, datetime string from raw tweet and whether the string contains unicode
  # Return None if the input tweet has abnormal format
  def parse_raw_tweet(self, raw_tweet):
    try:  
      raw_text = raw_tweet['text']
      text = re.sub(r'[^\x00-\x7F]+', '', raw_text)
      date_string = raw_tweet['created_at']
      return text, date_string, (len(raw_text) != len(text))
    except Exception as e:
      return None, None, False   # skip abnormal tweet, like {"limit":{"track":12,"timestamp_ms":"1446253519737"}}

  # Return datetime from datetime string
  def get_datetime(self, date_string):
    return parser.parse(date_string)

  # Return a sorted hashtag_pair_list from tweet context
  def get_hashtag_pair_list(self, text):
    # create sorted hashtag_list
    string_list = text.split(' ')
    hashtag_list = []
    for s in string_list:
      if '#' in s: 
        hashtag_sub_list = s.split(',')   # some of the hashtag is connected with ','
                                          # e.g. "22h,#reto800risah,#amandapasucasa,#sofiaganadora,#teamsofia"
        for h in hashtag_sub_list:
          if (len(h) >= 1 and '#' == h[0]): hashtag_list.append(h.lower())
    hashtag_list = list(set(hashtag_list))  # remove duplicate
    hashtag_list.sort()

    # create hashtag_pair_list, hashtag list as accending order in pair
    hashtag_pair_list = []
    for i in range(0, len(hashtag_list)):
      for j in range(i + 1, len(hashtag_list)):
        hashtag_pair_list.append((hashtag_list[i], hashtag_list[j]))
    return hashtag_pair_list