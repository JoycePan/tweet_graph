from graph_LRU_edge_cache import *

class GraphAdjacentSetCache:
  """ Store the whole graph information with HashMap, which key is node (hashtag) in the graph, 
  value is a set of neighbor (hashtags appear in the same tweet with the key)
  """

  def __init__(self):
    self.cache = {}   # node map to a set of neighbor nodes

  # input a list of hashtag pair, store them in the data structure
  def set_hashtag_pair_list(self, hashtag_pair_list):
    for hashtag_pair in hashtag_pair_list:
      # first element of the pair
      if hashtag_pair[0] not in self.cache:
        self.cache[hashtag_pair[0]] = set([hashtag_pair[1]])
      else:
        self.cache[hashtag_pair[0]].add(hashtag_pair[1])
      # second element of the pair
      if hashtag_pair[1] not in self.cache:
        self.cache[hashtag_pair[1]] = set([hashtag_pair[0]])
      else:
        self.cache[hashtag_pair[1]].add(hashtag_pair[0])

  # input a list of hashtag pair, remove related edges in the graph
  # if the set become empty, remove related node from the graph
  def remove_hashtag_pair(self, remove_list):
    for pair in remove_list:
      self.cache[pair[0]].remove(pair[1])
      if 0 == len(self.cache[pair[0]]): 
        del self.cache[pair[0]]
      self.cache[pair[1]].remove(pair[0])
      if 0 == len(self.cache[pair[1]]): 
        del self.cache[pair[1]]
