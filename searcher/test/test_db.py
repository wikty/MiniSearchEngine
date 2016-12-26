from searcher.db.client.db import SQLiteDB
from searcher.db.load_data import Loader
from searcher.utils.trie import Trie
from searcher.db.calculate_freq import Calculator

def test_db():
	db = SQLiteDB()
	db.create_table('test', {'name':'s','age':'i'})
	# print(db.insert_table('test', {'name': 'xiao', 'age': 23}))
	# print(db.select_table('test', ['id', 'name']))
	# print(db.count_table('test', {'id':'>0'}))
	print(db.select_table('test', ['id', 'name', 'age']))
	print(db.update_table('test', {'age': '1'}, 'name="xiao"'))
	print(db.select_table('test', ['id', 'name', 'age']))

def test_tire():
	indexer = Trie()
	print(indexer.insert('name', 'xiaowenbin'))
	print(indexer.insert('name', 'xiaowenbin'))
	print(indexer.insert('age', 23))
	print(indexer.index('name'))
	print(indexer.index('age'))
	#indexer.dump('test.txt')
	# indexer.load('test.txt')
	# print(indexer.index('name'))
	# print(indexer.index('age'))

def test_load_data():
	l = Loader({
		'datadir': 'searcher/data',
		'file_suffix': '.html',
		'meta_suffix': '.meta'
	})
	l.load()

def test_calculate_freq():
	c = Calculator()
	c.run()

def test():
	#test_db()
	#test_tire()
	#test_load_data()
	#test_calculate_freq()
	pass