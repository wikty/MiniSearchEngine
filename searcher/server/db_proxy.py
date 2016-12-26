from searcher.db.client.db import SQLiteDB

class DBProxy(object):
	def __init__(self, db=None):
		if db:
			self.db = db
		else:
			self.db = SQLiteDB()

	def __del__(self):
		if self.db:
			self.db.close()

	def close(self):
		if self.db:
			self.db.close()

	def query(self, sql=''):
		if not sql:
			return []
		return self.db.sql(sql)

	def get_doc_list(self, terms):
		terms = ', '.join(['"{}"'.format(term) for term in terms])
		sql = 'SELECT DISTINCT(doc_id) FROM term2doc JOIN terms ON term2doc.term_id=terms.id WHERE terms.term IN ({})'.format(terms)
		return [row[0] for row in self.query(sql)]

	def get_doc_info(self, terms):
		terms = ', '.join(['"{}"'.format(term) for term in terms])
		sql = 'SELECT `doc_id`, docs.url, docs.path, docs.word_count, docs.vector_len, docs.title,`term_id`, terms.inverse_doc_freq, term2doc.term_freq, `start`, `end`, terms.term FROM term2doc JOIN terms ON term2doc.term_id=terms.id JOIN docs ON term2doc.doc_id=docs.id WHERE terms.term IN ({})'.format(terms)
		results = {}
		for row in self.query(sql):
			if row[0] not in results:
				results[row[0]] = {
					'doc_id': row[0],
					'doc_url': row[1],
					'doc_path': row[2],
					'doc_word_count': row[3],
					'doc_vector_len': row[4],
					'doc_title': row[5],
					'terms': []
				}
			results[row[0]]['terms'].append({
				'term_id': row[6],
				'term_inverse_doc_freq': row[7],
				'term_freq': row[8],
				'term_start': row[9],
				'term_end': row[10],
				'term': row[11]
			})
		return results
	
	def get_term_info(self, terms):
		terms = ', '.join(['"{}"'.format(term) for term in terms])
		sql = 'SELECT DISTINCT(term), id, inverse_doc_freq FROM terms WHERE term in ({})'.format(terms)		
		results = self.query(sql)
		return results if results else []

	# def get_term_id(self, terms):
	# 	terms = ', '.join(['"{}"'.format(term) for term in terms])
	# 	sql = 'SELECT DISTINCT(term), id FROM terms WHERE term in ({})'.format(terms)
	# 	results = self.query(sql)
	# 	return results if results else []

	# def get_term_idf(self, term):
	# 	sql = 'SELECT inverse_doc_freq FROM terms WHERE term="{}"'.format(term)
	# 	results = self.query(sql)
	# 	return results[0][0] if results else None

	def get_doc_count(self):
		return self.db.count_table('docs')