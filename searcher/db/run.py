from .load_data import Loader
from .calculate_freq import Calculator

def load(config):
	l = Loader(config)
	l.load()
	c = Calculator()
	c.run()