from searcher.test import run as runtest
from searcher.db.run import load as loaddata
from searcher.server import run as runserver


if __name__ == '__main__':
	#runtest.testdb()
	#runtest.testserver()
	
	runserver.start()
	
	# loaddata({
	# 	'datadir': 'searcher/data',
	# 	'file_suffix': '.html',
	# 	'meta_suffix': '.meta'
	# })