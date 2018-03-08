# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo

class SinafinancePipeline(object):
    def process_item(self, item, spider):
        return item

class MongodbPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        news = settings['MONGODB_SINANEWS']

        client = pymongo.MongoClient(host=host, port=port)
        db = client[dbName]
        self.post = db[news]

    def process_item(self, item, spider):
        news = dict(item)
        self.post.insert(news)
        return item