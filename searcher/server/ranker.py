import math

def term_weight(terms, doc_len):
	w = {}
	for term in terms:
		tf = term['term_freq']
		idf = term['inverse_doc_freq']
		w[term['term_id']] = (tf/doc_len)*idf
	return w

def query2vector(db, terms):
	term_count = {}
	for term in terms:
		if term not in term_count:
			term_count[term] = 0
		term_count[term] += 1
	t = []
	doc_len = 0
	for term, term_id, idf in db.get_term_info(terms):
		doc_len += 1
		t.append({
			'term_freq': term_count[term],
			'inverse_doc_freq': idf,
			'term_id': term_id
		})
	return term_weight(t, doc_len)

def document2vector(doc, terms):
	terms = set(terms)
	doc_len = doc['doc_word_count']
	t = []
	for term in doc['terms']:
		if term['term'] in terms:
			t.append({
				'term_freq': term['term_freq'],
				'inverse_doc_freq': term['term_inverse_doc_freq'],
				'term_id': term['term_id']
			})
	return term_weight(t, doc_len)

def vector_dot(v1, v2):
	s = 0.0
	for k in v1:
		if k in v2:
			s += v1[k]*v2[k]
	return s

def vector_len(v):
	s = 0.0
	for k in v:
		s += v[k]
	return math.sqrt(s)

def rank(db, doc_info, terms):
	doc_list = []
	for doc_id in doc_info:
		doc_list.append(doc_info[doc_id])
	query_vector = query2vector(db, terms)
	
	def k(doc):
		nonlocal terms
		nonlocal query_vector
		document_vector = document2vector(doc, terms)
		score = vector_dot(query_vector, document_vector)/(vector_len(query_vector)*doc['doc_vector_len'])
		return score
	
	return sorted(doc_list, reverse=True, key=k)