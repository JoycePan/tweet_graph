import json
import os
import re
from tweet_parser import *
from graph_LRU_edge_cache import *
from graph_adjacent_set_cache import *

data = []
file_dir = os.path.dirname(os.path.realpath(__file__)) 

tweet_parser = TweetParser()
edge_cache = GraphLRUEdgeCache()
adj_graph_cache = GraphAdjacentSetCache()
remove_num = 0
# lru_total_num = 0
# adj_total_num = 0

with open(file_dir + '/../data-gen/backup/tweets.txt') as f:
	for line in f:
		tweet_json = json.loads(line)
		text, date = tweet_parser.parse_raw_tweet(tweet_json)
		if (None != text): 
			data.append(text + ' (timestamp: ' + date + ')')
			hashtag_pair_list = tweet_parser.get_hashtag_pair_list(text)
			remove_list = edge_cache.set_hashtag_pair_list(hashtag_pair_list, tweet_parser.get_datetime(date))
			adj_graph_cache.set_hashtag_pair_list(hashtag_pair_list)

			remove_num += len(remove_list)
			adj_graph_cache.remove_hashtag_pair(remove_list)

file_out = os.path.dirname(os.path.realpath(__file__)) + '/../tweet_output/ft1.txt'
f = open(file_out, 'w')
f.write('\n'.join(data))
f.close

print '**************************'
print len(edge_cache.cache)
print len(adj_graph_cache.cache)
print 'degree: ' + str(round(2.0 * len(edge_cache.cache) / len(adj_graph_cache.cache), 2))
# print 'lru_total_num: ', lru_total_num, 'adj_total_num: ', adj_total_num, ", remove_num: ", remove_num
print "remove_num: ", remove_num