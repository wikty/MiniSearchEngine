def extract_sentence(raw, term_start, term_end):
	s = set(',.?')
	for i in range(term_start, -1, -1):
		if raw[i] in s:
			break
	for j in range(term_end, len(raw)):
		if raw[j] in s:
			break
	#return raw[i+1:j]
	return raw[i+1:term_start]+'<em class="text-red">'+raw[term_start:term_end]+'</em>'+raw[term_end:j]

def extract(doc_list):
	results = []
	for doc in doc_list:
		doc_id = doc['doc_id']
		doc_path = doc['doc_path']
		doc_url = doc['doc_url']
		doc_title = doc['doc_title']
		raw = ''
		with open(doc_path, 'r', encoding='utf-8') as f:
			raw = f.read()
		sentences = []
		for term in doc['terms']:
			term_start = term['term_start']
			term_end = term['term_end']
			sentences.append(extract_sentence(raw, term_start, term_end))
		results.append({
			'title': doc_title,
			'url': doc_url,
			'snippet': ' '.join(sentences)
		})
	return results