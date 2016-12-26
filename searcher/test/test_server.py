from searcher.server.db_proxy import DBProxy
from searcher.server.query import process

def test_db_proxy():
	db = DBProxy()
	print(db.get_doc_list(["children", "london"]))
	print(db.get_doc_info(["children", "london"]))

def test_query_process():
	db = DBProxy()
	print(process(db, "children london"))

def test():
	#test_db_proxy()
	test_query_process()