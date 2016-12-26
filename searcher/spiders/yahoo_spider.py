import os, hashlib
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class YahooSpider(scrapy.Spider):
	name = 'yahoo-spider'
	start_urls = ['https://www.yahoo.com/news/']
	custom_settings = {
		'USER_AGENT': 'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
		'DOWNLOAD_DELAY': 5,
		'RANDOMIZE_DOWNLOAD_DELAY': True,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
		'CONCURRENT_REQUESTS_PER_IP': 8,
		'LOG_FILE': 'logs'
	}
	data_dir = '../data/'

	def start_requests(self):
		for url in self.start_urls:
			request = scrapy.Request(
				url,
				callback=self.parse,
				errback=self.errback,
				dont_filter=True)
			yield request

	def errback(self, failure):
		# log all failures
		self.logger.error(repr(failure))

		# in case you want to do something special for some errors,
		# you may need the failure's type:

		if failure.check(HttpError):
		    # these exceptions come from HttpError spider middleware
		    # you can get the non-200 response
		    response = failure.value.response
		    self.logger.error('HttpError on %s', response.url)

		elif failure.check(DNSLookupError):
		    # this is the original request
		    request = failure.request
		    self.logger.error('DNSLookupError on %s', request.url)

		elif failure.check(TimeoutError, TCPTimedOutError):
		    request = failure.request
		    self.logger.error('TimeoutError on %s', request.url)

	def parse(self, response):
		xpath = '//div[contains(@class, "mainNavInnerWrapper")]//ul/li/a'
		for category in response.xpath(xpath)[:6]:
			url = category.xpath('@href').extract_first()

			if url is not None:
				url = response.urljoin(url)
				request = scrapy.Request(url, callback=self.parse_category)
				yield request

	def parse_category(self, response):
		cname = response.url.strip('/').split('/')[-1]
		dirname = self.data_dir+cname
		if not os.path.exists(dirname):
			os.makedirs(dirname)
		#xpath1 = '//div[@id="tgtm-YDC-Stream"]/ul/li//h3/a'
		#xpath2 = '//div[@id="tgtm-YDC-Stream"]//div[contains(@class, "js-stream-content")]//a'
		#articles = response.xpath(xpath1)[:100] + response.xpath(xpath2)[:100]
		xpath = '//div[@id="YDC-Stream"]/ul/li[contains(@class, "js-stream-content")]//a'
		articles = response.xpath(xpath)
		for article in articles:
			url = article.xpath('@href').extract_first()
			title = article.xpath('div/text()').extract_first()

			if url is not None and title:
				url = response.urljoin(url)
				request = scrapy.Request(url, callback=self.parse_article)
				request.meta['category_name'] = cname
				request.meta['title'] = title
				yield request

	def parse_article(self, response):
		aname = response.url.strip('/').split('/')[-1]
		aname = hashlib.md5(aname.encode('utf-8')).hexdigest() + '.html'
		apath = self.data_dir + response.meta['category_name'] + '/' + aname
		title = response.meta['title']

		xpath = '//article[1]//p/text()'
		content = '\n'.join(response.xpath(xpath).extract())
		with open(apath, 'w', encoding='utf-8') as f:
			f.write(content)
		with open(apath+'.meta', 'w', encoding='utf-8') as f:
			f.write(response.url)
			f.write('\n')
			f.write(title)
		# if not self.check_cache(response, apath):
		# 	with open(apath, 'wb') as f:
		# 		f.write(response.body)
		# 	with open(apath+'.meta', 'w') as f:
		# 		f.write(response.url)