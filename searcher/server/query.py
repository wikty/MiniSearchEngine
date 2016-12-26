from searcher.indexer.pipelines import Pipeline
from .ranker import rank
from .extractor import extract

def process(db, query):
	[terms, _] = Pipeline.preprocess(query)
	doc_info = db.get_doc_info(terms)
	doc_list = rank(db, doc_info, terms)
	return extract(doc_list)