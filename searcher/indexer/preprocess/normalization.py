import nltk

class Normalizer(object):
	@staticmethod
	def lowercase(raw):
		return raw.lower()

	@staticmethod
	def stem(tokens):
		if not tokens:
			return []
		porter = nltk.PorterStemmer()
		return [porter.stem(t) for t in tokens]

	@staticmethod
	def lemmatize(tokens):
		if not tokens:
			return []
		wnl = nltk.WordNetLemmatizer()
		return [wnl.lemmatize(t) for t in tokens]