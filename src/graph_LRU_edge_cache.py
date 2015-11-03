from datetime import *

class GraphLRUEdgeCache:

	# Double LinkedList Node
	class Node:
		def __init__(self, key, val):
			self.key = key	# hashtage_pair
			self.val = val	# datetime
			self.prev = None
			self.next = None

	def __init__(self):
		self.cache = {}	# hashtag_pair map to related Node
		self.head = self.Node(None, None)
		self.tail = self.Node(None, None)
		self.head.next = self.tail
		self.tail.next = self.head

	def get(self, key):
		if key not in self.cache:
			return None
		else:
			current = self.cache[key]
			current.prev.next = current.next
			current.next.prev = current.prev
			self.move_to_tail(current)
			return current.val

	def set(self, key, value):
		if None != self.get(key):
			self.cache.get(key).val = value
		else:
			current = self.Node(key, value)
			if 0 == len(self.cache):
				self.head.next = current
				current.prev = self.head
				current.next = self.tail
				self.tail.prev = current
			else:
				self.move_to_tail(current)
			self.cache[key] = current

	def move_to_tail(self, current):
		self.tail.prev.next = current
		current.prev = self.tail.prev
		current.next = self.tail
		self.tail.prev = current

	# return a list of hashtag_pair that need to remove
	def set_hashtag_pair_list(self, hashtag_pair_list, time):
		for hashtag_pair in hashtag_pair_list:
			self.set(hashtag_pair, time)
		return self.remove_old_hashtag_pair(time)

	def remove_old_hashtag_pair(self, current_time):
		remove_list = []
		compare_time = current_time - timedelta(seconds = 60)
		current = self.head.next
		while (current != self.tail and current.val < compare_time):
			self.head.next = current.next
			current.next.prev = self.head
			remove_list.append(current.key)
			del self.cache[current.key]
			current = current.next
		return remove_list

	def list_to_string(self):
		result = ""
		if 0 != len(self.cache):
			current = self.head.next
			while current != self.tail:
				result += str(current.key) + ', (' + str(current.val) + ')\n'
				current = current.next
		return result