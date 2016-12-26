from searcher.utils.trie import Trie

class IDManager(object):
	def __init__(self, dump_file='id_data.pkl'):
		self.dump_file = dump_file
		self.indexer = Trie()

	def insert(self, id, value):
		return self.indexer.insert(id, value)

	def index(self, id):
		return self.indexer.index(id)

	def load(self, dump_file=''):
		dump_file = dump_file if dump_file else self.dump_file
		self.indexer.load(dump_file)

	def dump(self, dump_file=''):
		dump_file = dump_file if dump_file else self.dump_file
		self.indexer.dump(dump_file)