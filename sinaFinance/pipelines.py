# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
from scrapy.exceptions import DropItem
import redis

class SinafinancePipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):
    def __init__(self):
        host = settings['REDIS_HOST']
        port = settings['REDIS_PORT']
        db = 0
        self.redis_db = redis.Redis(host=host, port=port, db=db)
        self.redis_data_dict = "Mongodb_Item_Data"

        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        col = settings['MONGODB_COLLECTION']
        client = pymongo.MongoClient(host=host, port=port)
        db = client[dbName]
        mongodb_data = db[col].find({}, {"link":1})

        self.redis_db.flushdb() # 将redis中的数据进行清空
        if self.redis_db.hlen(self.redis_data_dict) == 0:
            for userId_dict in mongodb_data:
                # 将mongodb中的数据插入到redis数据库中
                self.redis_db.hset(self.redis_data_dict, userId_dict['link'], 0)
        client.close()

    def process_item(self, item, spider):
        # 如果该item已经在redis中出现了，那么丢弃
        if self.redis_db.hexists(self.redis_data_dict, item['link']):
            raise DropItem("Duplicate item found: %s" % item)
            # raise DropItem("Duplicate item found!!!")
        else:
            # 如果没有出现过，那么将该item的信息插入到redis中
            self.redis_db.hset(self.redis_data_dict, item['link'], 0)
            return item

class MongodbPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        news = settings['MONGODB_COLLECTION']

        client = pymongo.MongoClient(host=host, port=port)
        db = client[dbName]
        self.post = db[news]

    def process_item(self, item, spider):
        news = dict(item)
        self.post.insert(news)
        return item