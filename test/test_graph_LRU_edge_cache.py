import unittest
import os
import datetime
import dateutil
from dateutil import parser
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../src/')
from graph_LRU_edge_cache import *

class TestGraphLRUEdgeCache(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(TestGraphLRUEdgeCache, self).__init__(*args, **kwargs)
    self.file_dir = os.path.dirname(os.path.realpath(__file__))
    self.edge_cache = GraphLRUEdgeCache()

  def test_set_non_existed_value(self):
    self.edge_cache.set(('#apache', '#hadoop'), parser.parse('Thu Oct 29 17:51:01 +0000 2015'))
    self.edge_cache.set(('#apache', '#storm'), parser.parse('Thu Oct 29 17:51:30 +0000 2015'))
    result = self.edge_cache.list_to_string()

    expected_list = str(('#apache', '#hadoop')) + ', (2015-10-29 17:51:01+00:00)\n'\
          + str(('#apache', '#storm')) + ', (2015-10-29 17:51:30+00:00)\n'
    self.assertEqual(result, expected_list)

    expected_map_keyset = set([('#apache', '#hadoop'), ('#apache', '#storm')])
    self.assertEqual(set(self.edge_cache.cache.keys()), expected_map_keyset)

  def test_set_existed_value(self):
    self.edge_cache.set(('#apache', '#hadoop'), parser.parse('Thu Oct 29 17:51:01 +0000 2015'))
    self.edge_cache.set(('#apache', '#storm'), parser.parse('Thu Oct 29 17:51:30 +0000 2015'))
    self.edge_cache.set(('#apache', '#hadoop'), parser.parse('Thu Oct 29 17:51:57 +0000 2015'))
    result = self.edge_cache.list_to_string()

    expected_list = str(('#apache', '#storm')) + ', (2015-10-29 17:51:30+00:00)\n'\
          + str(('#apache', '#hadoop')) + ', (2015-10-29 17:51:57+00:00)\n'
    self.assertEqual(result, expected_list)

    expected_map_keyset = set([('#apache', '#hadoop'), ('#apache', '#storm')])
    self.assertEqual(set(self.edge_cache.cache.keys()), expected_map_keyset)

  def test_set_hashtag_pair_list_non_remove_old_node(self):
    remove_list = []
    hashtag_pair_list = [('#apache', '#hadoop'), ('#apache', '#storm'), ('#hadoop', '#storm')]
    remove_list += self.edge_cache.set_hashtag_pair_list(hashtag_pair_list, parser.parse('Thu Oct 29 17:51:30 +0000 2015'))
    result = self.edge_cache.list_to_string()

    expected_list = str(('#apache', '#hadoop')) + ', (2015-10-29 17:51:30+00:00)\n'\
          + str(('#apache', '#storm')) + ', (2015-10-29 17:51:30+00:00)\n'\
          + str(('#hadoop', '#storm')) + ', (2015-10-29 17:51:30+00:00)\n'
    self.assertEqual(result, expected_list)
    self.assertEqual(remove_list, [])

    expected_map_keyset = set([('#apache', '#hadoop'), ('#apache', '#storm'), ('#hadoop', '#storm')])
    self.assertEqual(set(self.edge_cache.cache.keys()), expected_map_keyset)

  def test_set_hashtag_pair_list_remove_old_node(self):
    remove_list = []
    hashtag_pair_list = [('#apache', '#hadoop'), ('#apache', '#storm'), ('#hadoop', '#storm')]
    remove_list += self.edge_cache.set_hashtag_pair_list(hashtag_pair_list, parser.parse('Thu Oct 29 17:51:30 +0000 2015'))
    hashtag_pair_list = [('#flink', '#spark')]
    remove_list += self.edge_cache.set_hashtag_pair_list(hashtag_pair_list, parser.parse('Thu Oct 29 17:51:56 +0000 2015'))
    hashtag_pair_list = [('#apache', '#hadoop')]
    remove_list += self.edge_cache.set_hashtag_pair_list(hashtag_pair_list, parser.parse('Thu Oct 29 17:52:05 +0000 2015'))
    hashtag_pair_list = []
    remove_list += self.edge_cache.set_hashtag_pair_list(hashtag_pair_list, parser.parse('Thu Oct 29 17:52:35 +0000 2015'))
    result = self.edge_cache.list_to_string()

    expected_list = str(('#flink', '#spark')) + ', (2015-10-29 17:51:56+00:00)\n'\
          + str(('#apache', '#hadoop')) + ', (2015-10-29 17:52:05+00:00)\n'
    self.assertEqual(result, expected_list)
    self.assertEqual(remove_list, [('#apache', '#storm'), ('#hadoop', '#storm')])

    expected_map_keyset = set([('#flink', '#spark'), ('#apache', '#hadoop')])
    self.assertEqual(set(self.edge_cache.cache.keys()), expected_map_keyset)

if __name__ == '__main__':
    unittest.main()