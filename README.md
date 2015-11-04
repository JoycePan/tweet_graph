Insight Data Engineering - Implement Coding Challenge
===========================================================
For this coding challenge, I will develop a tool that could help analyze the community of Twitter users.

## Challenge Requirement

This challenge is to implement two features:

1. Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.
2. Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.

## Development Summary

Based on the requirement, I've implemented 2 features. In order to evaluate my tool and adapt different usage, my tool can parse realtime tweets and pre_created local tweets. 

These are features of my tool:

1. Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.
2. Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.
3. Based on feature 1 and feature 2, implement the tool in 2 ways: process pre_created local tweets and process realtime tweets. Process local tweets to get performance data about this tool. The experienment data is about 9 seconds to parse 18729 tweets. Process realtime tweets to meet higher requirement

## Algorithm and Datastructure
Implement the hashtag graph with LRU algorithm and graph adjacent set.

1. LRU (least recently used) algorithm: Aims to keep twwets in last 60 seconds and get edge nubmer. It's implemented with HashMap and Double LinkedList. Key of the HashMap is hashtag_pair(e.g. ('#apache', '#hadoop')), value is related Double LinkedList Node, which contains hashtag_pair, datetime and two pointers. The Double LinkedList is sorted in ascending order with datetime. Whenever I update the graph, I will add new edges and remove timeout edges, which is outside the latest 60 seconds window.
2. Graph Adjacent Set: Aims to get total nodes in the graph. Store the whole graph information with HashMap, which key is node (hashtag) in the graph, value is a set of neighbor (hashtags appear in the same tweet with the key). I choose HashMap and HashSet because get() and set() of them are O(1) time complexity. Whenever I update the graph, I will add new nodes and related neighbours and remove timeout nodes and related neighbours.


## How to test and run the code
- run_test.sh : run testcase
- run_pre_create.sh : run script that process pre created tweets in ./tweet_input/pre_create_tweets.txt
- run_realtime.sh : run script that process realtime tweets 

To run run_realtime.sh, you need .twitter under ./data-gen/, and .twitter should contains twitter credential as following.

	{
	"access_token":"your access_token",
	"access_token_secret":"your access_token_secret",
	"consumer_key":"your consumer_key",
	"consumer_secret":"your consumer_secret"
	}
