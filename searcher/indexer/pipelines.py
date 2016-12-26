import nltk
from .preprocess import cleaning, normalization, tokenization

class Pipeline(object):

	@staticmethod
	def preprocess(raw):
		raw = normalization.Normalizer.lowercase(raw)
		[tokens, positions] = tokenization.Tokenizer.word_tokenize2(raw)
		tks = []
		pts = []
		for reserved, i in zip(cleaning.Cleaner.remove_stopwords(tokens), range(len(tokens))):
			if reserved:
				tks.append(tokens[i])
				pts.append(positions[i])
		tks = normalization.Normalizer.stem(tks)
		return [tks, pts]

	@staticmethod
	def calculate_tf(tokens):
		fd = nltk.FreqDist(tokens)
		return fd