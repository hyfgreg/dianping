# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class MongoPipeline(object):

    # collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # self.db[self.collection_name].insert_one(dict(item))
        # if item.__class__ == 'categoryItem':
        if item.__class__.__name__ == 'categoryItem':
            self.db[item.category].update({'categoryId':item['categoryId']},{'$set':item},True)
        if item.__class__.__name__ == 'shopItem':
            # item['categoryName'] = self.db['category'].find_one({'categoryId': item['categoryId']}).get('categoryName')
            self.db[item['categoryId']].update({'shopId': item['shopId']}, {'$set': item}, True)
        return item