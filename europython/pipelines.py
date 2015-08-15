# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.contrib.exporter import XmlItemExporter
import codecs
import json
import csv
import MySQLdb

class EuropythonPipeline(object):	
	def __init__(self):
		self.file = codecs.open('europython_items.json', 'w+b', encoding='utf-8')

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False) + "\n"
		self.file.write(line)
		return item

	def spider_closed(self, spider):
		self.file.close()

class EuropythonXmlExport(object):
	
	def __init__(self):
		self.files = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		file = open('europython_items.xml', 'w+b')
		self.files[spider] = file
		self.exporter = XmlItemExporter(file)
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
		
		
class EuropythonMySQLPipeline(object):

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline
		
	def spider_opened(self, spider):
		self.conexion = MySQLdb.connect(user='mysql', passwd='mysql', db='dbeuropython', host='localhost', charset="utf8", use_unicode=True)
		self.cursor = self.conexion.cursor()
		self.cursor.execute("""DELETE FROM conferences""")
		self.conexion.commit()

	def spider_closed(self, spider):
		self.conexion.close()
		 
	def process_item(self, item, spider):
		try:
	
			#strTags = ','.join(item['tags'])
			strAuthor = str(item['author'])
			strAuthor = strAuthor[3:len(strAuthor)-2]
			
			strTitle = str(item['title'])
			strTitle = strTitle[3:len(strTitle)-2]
			
			strDescription = str(item['description'])
			strDescription = strDescription[3:len(strDescription)-2]
			
			strDate = str(item['date'])
			strDate = strDate[3:len(strDate)-2]
			strDate = strDate.replace("[u'", "").replace("']", "").replace("u'", "").replace("',", ",")
			
			strTags = str(item['tags'])
			strTags = strTags.replace("[u'", "").replace("']", "").replace("u'", "").replace("',", ",")
			query = ("INSERT INTO conferences (author,title,description,date,tags) VALUES (%s, %s, %s, %s,%s);",(strAuthor,strTitle,strDescription,strDate,strTags))
			
			print query
			self.cursor.execute(*query)
			self.conexion.commit()

		except MySQLdb.Error, e:
			print "Error al procesar los items en la BD %d: %s" % (e.args[0], e.args[1])

		return item