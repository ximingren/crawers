# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os

import pymongo
from numpy import unicode
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter


class _58CrawerPipeline(object):
    collection_name = 'film2'

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
            item=item['item']
            EnMovieID=item['EnMovieID']
            self.db[self.collection_name].update({'EnMovieID': EnMovieID}, {'$set': dict(item)}, True)
            logging.info("插入数据成功%s,ID为%s"%(str(item['MovieName']),str(EnMovieID)))
            return item
        except Exception as e:
            print(e)

class EbotappPipeline(object):
    collection_name = 'film2'

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
            item=item['item']
            EnMovieID=item['EnMovieID']
            self.db[self.collection_name].update({'EnMovieID': EnMovieID}, {'$set': dict(item)}, True)
            logging.info("插入数据成功%s,ID为%s"%(str(item['MovieName']),str(EnMovieID)))
            return item
        except Exception as e:
            print(e)

class ZooplaPipeline(object):
    collection_name = 'maoyan11'

    def __init__(self, mongo_url, mongo_db,address_list):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        # self.ids_seen=set()
        # self.exporter={}
        # self.file={}
        # self.address_list=address_list
        # if not os.path.exists('data'):
        #     os.mkdir('data')
        # for address in address_list:
        #     self.file[address]=open('data/'+address+'.csv','wb')
        #     self.exporter[address]=CsvItemExporter(self.file[address])
        #     self.exporter[address].start_exporting()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_url=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE'),address_list=crawler.settings.get('ADDRESS_LIST'))

    def open_spider(self, spider):
        logging.info("开启MongoDB连接")
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()
        # for address in self.address_list:
        #     self.file[address].close()
        #     self.exporter[address].finish_exporting()
        logging.info("关闭MongoDB连接")

    def process_item(self, item, spider):
        try:
                item=item['item']
                # address=item['bigAddress']
            # if item['id'] in self.ids_seen:
            #     raise DropItem('Duplicate item found: %s'%item)
            # else:
            #     self.exporter[address].export_item(item)
            #     print('插入数据到%s文件成功'%address)
                self.db[self.collection_name].update({'id':item['id']}, {'$set': dict(item)}, True)
                logging.info("插入数据成功,ID为%s"%(item['id']))
                return item
        except Exception as e:
            print('插入数据错误',e)
