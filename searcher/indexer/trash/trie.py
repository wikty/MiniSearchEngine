import pickle, json

class Trie(object):
	def __init__(self):
		self.trie = {}

	def _insert(self, trie, key, value, update=False):
		if key:
			first, rest = key[0], key[1:]
			if first not in trie:
				trie[first] = {}
			return self._insert(trie[first], rest, value)
		else:
			if update is False and trie.get('value', None) is not None:
				return False
			else:
				trie['value'] = value
				return True

	def insert(self, key, value, update=False):
		key = key.lower()
		return self._insert(self.trie, key, value, update)

	def _index(self, trie, key):
		if key:
			first, rest = key[0], key[1:]
			if first not in trie:
				return None
			else:
				return self._index(trie[first], rest)
		else:
			return trie.get('value', None)

	def index(self, key):
		key = key.lower()
		return self._index(self.trie, key)

	def dump(self, filename):
		with open(filename, 'wb') as f:
			pickle.dump(self.trie, f)

	def load(self, filename):
		with open(filename, 'rb') as f:
			self.trie = pickle.load(f)
