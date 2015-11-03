#!/usr/bin/env bash

# argv[0]: script that process pre created tweets
# argv[1]: directory of pre_create_tweet file
# argv[2]: directory of feature 1's result
# argv[3]: directory of feature 2's result
python ./src/average_degree_from_local_tweet.py ./tweet_input/pre_create_tweets.txt ./tweet_output/ft1.txt ./tweet_output/ft2.txt