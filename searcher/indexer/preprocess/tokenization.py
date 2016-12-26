import re
import nltk

class Tokenizer(object):

	@staticmethod
	def word_tokenize(text=''):
		if not text:
			return []
		return nltk.word_tokenize(text)

	@staticmethod
	def word_tokenize2(text=''):
		if not text:
			return []
		pattern = r'''(?x)          # set flag to allow verbose regexps
			(?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
			| \w+(?:-\w+)*        # words with optional internal hyphens
			| \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
			| \.\.\.              # ellipsis
			| [][.,;"'?():_`-]    # these are separate tokens; includes ], [
		'''

		tokens = []
		positions = []
		for m in re.finditer(pattern, text):
			start = m.start()
			end = m.end()
			tokens.append(text[start:end])
			positions.append([start, end])
		return [tokens, positions]
		#return nltk.regexp_tokenize(text, pattern)