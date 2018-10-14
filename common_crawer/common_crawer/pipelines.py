# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo


class _58CrawerPipeline(object):
    collection_name = 'cboocn2'

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_url=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE'))

    def open_spider(self, spider):
        logging.info("开启MongoDB连接")
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()
        logging.info("关闭MongoDB连接")

    def process_item(self, item, spider):
        try:
            # item=item['item']
            EnMovieID=item['EnMovieID']
            self.db[self.collection_name].update({'EnMovieID': EnMovieID}, {'$set': dict(item)}, True)
            logging.info("插入数据成功%s,ID为%s"%(str(item['name']),str(EnMovieID)))
            return item
        except Exception as e:
            print(e)
