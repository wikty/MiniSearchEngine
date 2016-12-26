from bs4 import BeautifulSoup
import nltk

class Cleaner(object):
	@staticmethod
	def extract_text(html=''):
		soup = BeautifulSoup(html, "html.parser")
		
		# kill all script and style elements
		for script in soup(["script", "style"]):
			script.decompose()

		# get text
		text = soup.get_text()

		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
		text = '\n'.join(chunk for chunk in chunks if chunk)
		return text

	@staticmethod
	def remove_stopwords(tokens):
		if not tokens:
			return []
		stopwords = set(nltk.corpus.stopwords.words('english'))
		stopwords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '/', '...', '-', '+'])
		return [1 if t.lower() not in stopwords else 0 for t in tokens]