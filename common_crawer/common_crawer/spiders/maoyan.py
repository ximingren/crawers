# -*- coding: utf-8 -*-
import json
import re

import requests
from pymongo import MongoClient

import scrapy
from lxml import etree

from common_crawer.MongoQueue import MongoQueue
from scrapy import Request

from common_crawer.items import MaoyanItem

# TODO 错误了发邮件，或者提示信息。
#
class DoubanSpider(scrapy.Spider):
    name = 'douban'
    index_url = "https://piaofang.maoyan.com/movie/%s"
    honor_url = 'http://m.maoyan.com/movie/%s/honor'
    trailer_url = "https://piaofang.maoyan.com/movie/%s/promption-ajax?method=change&type=trailers&typeId=0&date=2018-10-10__2018-10-24"
    weibo_url = "https://piaofang.maoyan.com/movie/%s/promption-ajax?method=change&type=weibo&startDate=2018-10-10&endDate=2018-10-24"
    wechat_url = "https://piaofang.maoyan.com/movie/%s/promption-ajax?type=wechat&method=changeAccountChart&startDate=2018-10-10&endDate=2018-10-23"
    baidu_url = "https://piaofang.maoyan.com/movie/%s/promption-ajax?method=getIndex&type=baidu&startDate=2018-10-10&endDate=2018-10-23"
    actor_url = "https://piaofang.maoyan.com/movie/%s/celebritylist"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
    }
    indexqueue=MongoQueue('maoyan','indexurl')
    # honorqueue=MongoQueue('maoyan','honorurl')
    # trailersqueue=MongoQueue('maoyan','trailersurl')
    # weiboqueue=MongoQueue('maoyan','weibourl')
    # wechatqueue=MongoQueue('maoyan','wechaturl')
    # baiduqueue=MongoQueue('maoyan','baiduurl')
    # celebrityqueue=MongoQueue('maoyan','celebrityurl')
    cli = MongoClient('123.207.42.164')
    db = cli['maoyan']
    # document = db['maoyan11']
    document1 = db['againurl']

    def start_requests(self):
        # for id in range(250000,500000):
        #     totalData = {}
        while True:
            try:
                id,url = self.indexqueue.pop()
            except KeyError:
                print('队列没有数据')
                break
            else:
                totalData={}
        # for i in self.document1.find():
        #     id=i['id']
        #     totalData={}
            yield Request(url,
                          meta={'id': str(id), 'info': '下载%s index' % str(id), 'totalData': totalData},
                          errback=self.errback, callback=self.parse_index)

    def parse_index(self, response):
        id = response.meta['id']
        try:
            totalData = response.meta['totalData']
            totalData['id'] = id
            name = response.xpath(
                "//div[@class='info-base']/div[@class='info-detail']/div[@class='info-detail-title']//text()").extract()
            category = response.xpath(
                "//div[@class='info-base']/div[@class='info-detail']/div[@class='info-detail-extra']/div[@class='detail-list']/div[@class='detail-list-content']/p[@class='info-category']//text()").extract()
            runningTime = response.xpath("//div[@class='info-source-duration']//text()").extract()
            releaseTime = response.xpath("//div[@class='info-release']//text()").extract()
            scores_list = response.xpath("//div[@class='scores']/div[@class='percentbar']//text()").extract()
            score_count = response.xpath("//p[@class='detail-score-count']//text()").extract()
            rating_num = response.xpath("//div[@class='rating-stars']//text()").extract()
            wish_count = response.xpath("//p[@class='detail-wish-count']//text()").extract()
            totalBoxOffice = response.xpath(
                "//div[@class='info-detail-row'][1]//div[@class='info-detail-col'][1]//text()").extract()
            FirstDayBoxOffice = response.xpath(
                "//div[@class='info-detail-row'][1]//div[@class='info-detail-col'][2]//text()").extract()
            FirstWeekBoxOffice = response.xpath(
                "//div[@class='info-detail-row'][1]//div[@class='info-detail-col'][3]//text()").extract()
            predictionBoxOffice = response.xpath(
                "//div[@class='info-detail-row'][1]//div[@class='info-detail-col'][4]//text()").extract()
            totalData['name'] = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), name))))
            if totalData['name']!='' or totalData['name']:
                totalData['category'] = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), category))))
                totalData['runningTime'] = ''.join(
                    list(filter(lambda t: t != '', map(lambda x: x.strip(), runningTime)))).replace(" ", "")
                totalData['releaseTime'] = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), releaseTime))))
                totalData['scores_list'] = ';'.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), scores_list))))
                score_count = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), score_count))))
                score_count = ''.join(re.findall("\d+\.?\d*", score_count))
                totalData['score_count'] = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), score_count))))
                totalData['rating_num'] = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), rating_num))))
                wish_count = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), wish_count))))
                wish_count = ''.join(re.findall("\d+\.?\d*", wish_count))
                totalData['wish_count'] = wish_count
                totalData['totalBoxOffice'] = ''.join(
                    list(filter(lambda t: t != '', map(lambda x: x.strip(), totalBoxOffice))))[4:]
                totalData['FirstDayBoxOffice'] = ''.join(
                    list(filter(lambda t: t != '', map(lambda x: x.strip(), FirstDayBoxOffice))))[4:]
                totalData['FirstWeekBoxOffice'] = ''.join(
                    list(filter(lambda t: t != '', map(lambda x: x.strip(), FirstWeekBoxOffice))))[4:]
                totalData['predictionBoxOffice'] = ''.join(
                    list(filter(lambda t: t != '', map(lambda x: x.strip(), predictionBoxOffice))))[4:]
                item = MaoyanItem()
                item['item'] = totalData
                self.indexqueue.complete(response.url)
                yield item
                # yield Request(self.honor_url % (id), meta={'id': id, 'totalData': totalData, 'info': '下载%s honor' % id},
                #               callback=self.parse_honor, errback=self.errback)
        except Exception as e:
            print('index', e)
            self.write_error('index' + id)

    def errback(self, response):
        id = response.meta['id']
        self.write_error('download' + id)

    def write_error(self, info):
        with open('eroor', 'a') as w:
            w.write(info + '\n')
