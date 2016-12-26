from tokenization import Tokenizer

def test_tokenizer():
	print(Tokenizer.word_tokenize2('"A wasp in my car caused me to have an accident and my tax return, which was inside, was destroyed," was another, while several blamed children, partners or colleagues for inadvertently destroying their forms.'))

if __name__ == '__main__':
	test_tokenizer()