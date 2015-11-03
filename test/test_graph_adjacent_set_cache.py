import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src/')
from graph_adjacent_set_cache import *

class TestGraphAdjacentSetCache(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestGraphAdjacentSetCache, self).__init__(*args, **kwargs)
		self.file_dir = os.path.dirname(os.path.realpath(__file__))
		self.adj_graph_cache = GraphAdjacentSetCache()

	def test_set_hashtag_pair_list_without_exist(self):
		hashtag_pair_list = [('#apache', '#hadoop'), ('#apache', '#storm'), ('#hadoop', '#storm')]
		self.adj_graph_cache.set_hashtag_pair_list(hashtag_pair_list)
		expected = {'#apache': set(['#hadoop', '#storm']), '#hadoop': set(['#apache', '#storm']), \
					'#storm': set(['#apache', '#hadoop'])}
		self.assertEqual(self.adj_graph_cache.cache, expected)

	def test_set_hashtag_pair_list_without_exist(self):
		hashtag_pair_list = [('#apache', '#hadoop'), ('#apache', '#storm'), ('#hadoop', '#storm')]
		self.adj_graph_cache.set_hashtag_pair_list(hashtag_pair_list)
		hashtag_pair_list = [('#apache', '#hadoop')]
		self.adj_graph_cache.set_hashtag_pair_list(hashtag_pair_list)
		expected = {'#apache': set(['#hadoop', '#storm']), '#hadoop': set(['#apache', '#storm']), \
					'#storm': set(['#apache', '#hadoop'])}
		self.assertEqual(self.adj_graph_cache.cache, expected)

	def test_remove_hashtag_pair(self):
		hashtag_pair_list = [('#apache', '#hadoop'), ('#apache', '#storm'), ('#hadoop', '#storm')]
		self.adj_graph_cache.set_hashtag_pair_list(hashtag_pair_list)
		self.adj_graph_cache.remove_hashtag_pair([('#apache', '#storm'), ('#hadoop', '#storm')])
		expected = {'#apache': set(['#hadoop']), '#hadoop': set(['#apache'])}
		self.assertEqual(self.adj_graph_cache.cache, expected)

if __name__ == '__main__':
    unittest.main()