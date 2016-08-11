# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from medcitynews.items import MedcitynewsItem
import re
import pybloomfilter
import os
from datetime import datetime
import config
import test

class MedCityNewsSpider(scrapy.Spider):

	name = 'medcitynews_spider'

	def __init__(self,category=None,*args,**kwargs):

		super(MedCityNewsSpider,self).__init__(*args,**kwargs)

		self._HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',}

		if os.path.exists('./medcitynews.bloom'):
			self.blfilter = pybloomfilter.BloomFilter.open('medcitynews.bloom')
		else:
			self.blfilter = pybloomfilter.BloomFilter(1000000,0.01,'medcitynews.bloom')

	def start_requests(self):

		yield scrapy.Request('http://medcitynews.com/%s/%s' % (config.YEAR,config.MONTH),headers=self._HEADERS,encoding='utf-8',method='GET',dont_filter=True,callback=self.process_urls)


	def process_urls(self,response):

		urls = response.css('.page-main').xpath('descendant::a/@href').re(r'http://medcitynews.com/%s/%s/.*' % (config.YEAR,config.MONTH))
		for each in urls:
			print each
		for _url in urls:
			if _url in self.blfilter:
				print "url is crawled"
				pass
			else:
				self.blfilter.add(_url)
				yield scrapy.Request(_url,headers=self._HEADERS,encoding='utf-8',method='GET',dont_filter=True,callback=self.process_item)


	def process_item(self,response):
		
		item = MedcitynewsItem()
		title = response.css('.post-title').xpath('./text()').extract()
		author = response.css('header p.byline a').xpath('./text()').extract()
		content = response.css('.main>.entry>.content p').xpath('string(.)').extract()
		while '' in content:
			content.remove('');
		topics= response.css('.postTags p a').xpath('./text()').extract()
		image_url = response.css('.main>.entry>.content img').xpath('./@src').extract()
		crawled_url = response.url
		crawled_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		item['title'] = title
		item['author'] = author
		item['content'] = content
		item['topics'] = topics
		item['image_url'] = image_url
		item['crawled_url'] = crawled_url
		item['crawled_time'] = crawled_time
		yield item
