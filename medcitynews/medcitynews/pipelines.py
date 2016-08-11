# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import uuid



class MySQLStorePipeline(object):

	def __init__(self):
		
		self.connection = MySQLdb.connect('localhost','root','dongmai','_vcbeat',use_unicode=True,charset='UTF8')
		self.cursor = self.connection.cursor()


	def process_item(self,item,spider):

		sql = "insert into medcitynews(id,title,author,topics,content,crawled_url,crawled_time) values(%s,%s,%s,%s,%s,%s,%s)"
		_id = ''.join(str(uuid.uuid4()).split('-'))
		_data = (_id,item['title'],item['author'],','.join(item['topics']),'\n'.join(item['content']),item['crawled_url'],item['crawled_time'])

		try:
			self.cursor.execute(sql,_data)
			self.connection.commit()
		except MySQLdb.Error, e:
			print e

		return item