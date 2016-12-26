import os, pickle
import nltk
import pipelines
from db import SQLiteDB
from id_manager import IDManager

class Loader(object):
	def __init__(self, config):
		self.db = SQLiteDB(config['db'])
		self.idmanager = IDManager()
		self.term_id_prefix = 'term_id_'
		self.doc_id_prefix = 'doc_id_'
		self.datadir = config['datadir']
		self.file_suffix = config['file_suffix']
		self.meta_suffix = config['meta_suffix']
		self.tbl_docs = {
			'tbl_name': 'docs',
			'fields': {
				'url': 's',
				'path': 's',
				'word_count': 'i'
			}
		}
		
		self.tbl_terms = {
			'tbl_name': 'terms',
			'fields': {
				'term': 's',
				'doc_freq':'i'
			}
		}

		self.tbl_term2doc = {
			'tbl_name': 'term2doc',
			'fields': {
				'term_id': 'i',
				'doc_id': 'i',
				'start':'i',
				'end': 'i',
				'term_freq': 'i'
			}
		}

		self.db.create_table(self.tbl_docs['tbl_name'], self.tbl_docs['fields'])
		self.db.create_table(self.tbl_terms['tbl_name'], self.tbl_terms['fields'])
		self.db.create_table(self.tbl_term2doc['tbl_name'], self.tbl_term2doc['fields'])

	def scandir(self):
		dirname = self.datadir
		filelist = []
		if not os.path.exists(dirname):
			raise Exception('data directory {} not existed'.format(dirname))

		for directory, subdirs, files in os.walk(dirname):
			if directory != '.' and directory != '..':
				for fname in files:
					if not fname.endswith(self.file_suffix):
						continue
					path = os.sep.join([directory, fname])
					filelist.append(path)
		return sorted(filelist)

	def insert_docs(self, url, path, word_count):
		doc_id = self.db.insert_table(self.tbl_docs['tbl_name'], {
			'url': url,
			'path': path,
			'word_count': word_count
		})
		return doc_id

	def insert_terms(self, term):
		term_row = self.db.select_table(self.tbl_terms['tbl_name'], fields=['id', 'doc_freq'], where_condition='term="{}"'.format(term))
		if term_row:
			term_id = term_row[0][0]
			doc_freq = term_row[0][1]+1
			self.db.update_table(self.tbl_terms['tbl_name'], {'doc_freq': doc_freq}, where_condition='term="{}"'.format(term))
		else:
			doc_freq = 1
			term_id = self.db.insert_table(self.tbl_terms['tbl_name'], {'term': term, 'doc_freq': doc_freq})
		return term_id

	def insert_term2doc(self, term_id, doc_id, term_freq, start, end):
		self.db.insert_table(self.tbl_term2doc['tbl_name'], {
			'term_id': term_id,
			'doc_id': doc_id,
			'term_freq': term_freq,
			'start': start,
			'end': end
		})
	
	def load(self):
		for filename in self.scandir():
			content = ''
			with open(filename, 'r', encoding='utf-8') as f:
				content = f.read()
			if content:
				url = ''
				with open(filename+self.meta_suffix, 'r', encoding='utf-8') as f:
					url = f.read().strip()

				[tokens, positions] = pipelines.Pipeline.preprocess(content)
				doc_id = self.insert_docs(url, filename, len(tokens))
				self.idmanager.insert(self.doc_id_prefix+filename, doc_id)

				fd = pipelines.Pipeline.calculate_tf(tokens)
				# fd.plot(10)
				tokens_set = set()
				for token, i in zip(tokens, range(0, len(tokens))):
					if token in tokens_set:
						continue
					tokens_set.update([token])
					term_id = self.insert_terms(token)
					self.idmanager.insert(self.term_id_prefix+token, term_id)
					self.insert_term2doc(term_id, doc_id, fd[token], positions[i][0], positions[i][1])
		self.idmanager.dump()