import math
from searcher.db.client.db import SQLiteDB

class Calculator(object):
	def __init__(self):
		self.db = SQLiteDB()

	def update_terms(self):
		r = {}
		doc_count = self.db.count_table('docs')
		for term_id, doc_freq in self.db.select_table('terms', ['id', 'doc_freq']):
			idf = math.log(doc_count/(1+doc_freq))
			self.db.update_table('terms', {'inverse_doc_freq': idf}, 'id={}'.format(term_id))
			r[term_id] = idf
		return r

	def update_docs(self, idf):
		r = {}
		for doc_id in self.db.select_table('docs', ['id']):
			doc_id = doc_id[0]
			vector_len = 0.0
			for term_id, term_freq in self.db.select_table('term2doc', ['term_id', 'term_freq'], 'doc_id={}'.format(doc_id)):
				vector_len +=term_freq*idf[term_id]
			vector_len = math.sqrt(vector_len)
			self.db.update_table('docs', {'vector_len': vector_len}, 'id={}'.format(doc_id))
			r[doc_id] = vector_len
		return r

	def run(self):
		idf = self.update_terms()
		doc_vector_len = self.update_docs(idf)