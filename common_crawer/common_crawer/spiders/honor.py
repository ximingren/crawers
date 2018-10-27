import json
import logging
import re
import requests
from lxml import etree
from pymongo import MongoClient
from scrapy.log import logger

import scrapy
from common_crawer.items import MaoyanItem
from scrapy import Request


class HonorSpider(scrapy.Spider):
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
    name = 'honor'
    cli = MongoClient('123.207.42.164')
    db = cli['maoyan']
    document1 = db['needAgain']

    def start_requests(self):
            result = self.document1.find({'status': 1})
            for r in result:
                id = r['id']
                totalData = {}
                yield Request(self.honor_url % id,
                              meta={'id': str(id), 'info': '下载%s honor' % str(id), 'totalData': totalData},
                              errback=self.errback, callback=self.parse_honor)

    def parse_honor(self, response):
        id = response.meta['id']
        try:
            totalData = response.meta['totalData']
            totalData['id'] = id
            festival = response.xpath("//div[@class='page-content']/div[@class='festival']")
            actor_award = []
            director_award = []
            film_award = []
            for i in range(len(festival)):
                e = festival[i]
                header = e.xpath("//div[@class='header']/h2")[i].xpath('string(.)').extract_first()
                award = e.xpath("//ul[@class='awards']")[i]
                for l in award.xpath('li'):
                    text = l.xpath('string(.)').extract_first()
                    if '演员' in text or '主角' in text or '配角' in text:
                        actor_award.append(header + ":" + text)
                    elif '导演' in text:
                        director_award.append(header + ":" + text)
                    else:
                        film_award.append(header + ":" + text)
            totalData['actor_award'] = ';'.join(actor_award)
            totalData['director_award'] = ';'.join(director_award)
            totalData['film_award'] = ';'.join(film_award)
            res = self.openlink('https://piaofang.maoyan.com/movie/%s/promotion/trailers' % id)
            tree = etree.HTML(res.text)
            traller_number = tree.xpath("//div[@class='tralier-number']/div[@class='value-style']//text()")
            trailers_play_number = tree.xpath("//div[@class='play-number']/div[@class='value-style']//text()")
            trailers_comment_number = tree.xpath("//div[@class='comment-number']/div[@class='value-style']//text()")
            totalData['traller_number'] = ';'.join((traller_number))
            totalData['trailers_play_number'] = ';'.join((trailers_play_number))
            totalData['trailers_comment_number'] = ';'.join((trailers_comment_number))
            # 如果这三个都没有的话，那就不用再请求了
            if traller_number or trailers_play_number or trailers_comment_number:
                yield Request(self.trailer_url % id,
                              meta={'id': id, 'totalData': totalData, 'info': "下载 %s trailer" % id},
                              callback=self.parse_trailers, errback=self.errback)
            else:
                res = self.openlink("https://piaofang.maoyan.com/movie/%s/promotion/weibo" % id)
                tree = etree.HTML(res.text)
                # 有的话就请求weibo
                if tree.xpath("//div[@class='item']"):
                    weibo_subject = tree.xpath("//div[@class='item']")[1].xpath("./div[@class='data']//text()")
                    weibo_yesterday = tree.xpath("//div[@class='item']")[0].xpath("./div[@class='data']//text()")
                    totalData['weibo_subject'] = ''.join(weibo_subject)
                    totalData['weibo_yesterday'] = ''.join(weibo_yesterday)
                    yield Request(self.weibo_url % id,
                                  meta={'id': id, 'totalData': totalData, 'info': "下载 %s weibo" % id},
                                  callback=self.parse_weibo, errback=self.errback)
                # 没有就不清求上面这个
                else:
                    res = self.openlink("https://piaofang.maoyan.com/movie/%s/promotion/wechat" % id)
                    tree = etree.HTML(res.text)
                    # 如果有这个，就请求wechat
                    if tree.xpath("//div[@class='summary-cotnent']"):
                        wechat_titleNum = tree.xpath("//div[@class='summary-cotnent']")[0].xpath("./span/text()")
                        wechat_totalReadNum = tree.xpath("//div[@class='summary-cotnent']")[1].xpath(
                            "./span/text()")
                        totalData['wechat_titleNum'] = ';'.join(wechat_titleNum)
                        totalData['wechat_totalReadNum'] = ';'.join(wechat_totalReadNum)
                        yield Request(self.wechat_url % id,
                                      meta={'id': id, 'totalData': totalData, 'info': "下载 %s wechat" % id},
                                      callback=self.parse_wechat, errback=self.errback)
                    else:
                        # 没有就接着请求下一个
                        yield Request(self.baidu_url % id,
                                      meta={'id': id, 'totalData': totalData, 'info': '下载 %s baidu' % id},
                                      callback=self.parse_baidu, errback=self.errback)
        except Exception as e:
            print('honor', e)
            self.write_error('honor' + id)

    def parse_trailers(self, response):
        id = response.meta['id']
        try:
            totalData = response.meta['totalData']
            data = json.loads(response.text)
            everdayTenxun = []
            everydayAiqiyi = []
            everydayYouku = []
            everydaySouhu = []
            everydayMaoyan = []
            for a in data['data']:
                list = a['list']
                date = str(a['showDate'])
                if len(list) != 0:
                    everdayTenxun.append(date + ":" + str(list[0]['playCount']))
                    everydayAiqiyi.append(date + ":" + str(list[1]['playCount']))
                    everydayYouku.append(date + ":" + str(list[2]['playCount']))
                    everydaySouhu.append(date + ":" + str(list[3]['playCount']))
                if len(list) >= 5:
                    everydayMaoyan.append(date + ":" + str(list[4]['playCount']))
                else:
                    everydayMaoyan.append(date + ":" + " ")
            totalData['tenxunList'] = ';'.join((everdayTenxun))
            totalData['aiqiyiList'] = ';'.join((everydayAiqiyi))
            totalData['youkuList'] = ';'.join((everydayYouku))
            totalData['souhuList'] = ';'.join((everydaySouhu))
            totalData['maoyanList'] = ';'.join((everydayMaoyan))

            yield Request(self.weibo_url % id, meta={'id': id, 'totalData': totalData, 'info': '下载%s weibo' % id},
                          callback=self.parse_weibo, errback=self.errback)
        except Exception as e:
            print('trailers', e)
            self.write_error('trailers' + id)

    def parse_weibo(self, response):
        id = response.meta['id']
        try:
            totalData = response.meta['totalData']
            data = json.loads(response.text)
            everydayCommentNum = []
            everydayCount = []
            everydaForwardNum = []
            likeNum = []
            for a in data['data']:
                if len(a) != 0:
                    date = a['date']
                    everydayCommentNum.append(date + ":" + str(a['commentNum']))
                    everydayCount.append(date + ":" + str(a['count']))
                    everydaForwardNum.append(date + ":" + str(a['forwardNum']))
                    likeNum.append(date + ":" + str(a['likeNum']))
            totalData['everydayCommentNum'] = ';'.join(everydayCommentNum)
            totalData['everydayCount'] = ';'.join(everydayCount)
            totalData['everydaForwardNum'] = ';'.join(everydaForwardNum)
            totalData['likeNum'] = ';'.join(likeNum)
            yield Request(self.wechat_url % id, meta={'id': id, 'totalData': totalData, 'info': "下载 %s wechat" % id},
                          callback=self.parse_wechat, errback=self.errback)
        except Exception as e:
            print('weibo', e)
            self.write_error('weibo' + id)

    def parse_wechat(self, response):
        id = response.meta['id']
        try:
            data = json.loads(response.text)
            totalData = response.meta['totalData']
            everydayArticleNum = []
            everydayReadNum = []
            for a in data['data']:
                if len(a) != 0:
                    date = a['date']
                    everydayArticleNum.append(date + ":" + str(a['articleNum']))
                    everydayReadNum.append(date + ":" + str(a['readNum']))
            totalData['everydayArticleNum'] = ';'.join(everydayArticleNum)
            totalData['everydayReadNum'] = ';'.join(everydayReadNum)
            yield Request(self.baidu_url % id, meta={'id': id, 'totalData': totalData, 'info': '下载 %s baidu' % id},
                          callback=self.parse_baidu, errback=self.errback)
        except Exception as e:
            print('wechat', e)
            self.write_error('wechat' + id)

    def parse_baidu(self, response):
        id = response.meta['id']
        try:
            data = json.loads(response.text)
            totalData = response.meta['totalData']
            everyTotalIndex = []
            for a in data['data']:
                if len(a) != 0:
                    date = a['date']
                    everyTotalIndex.append(date + ":" + a['totalIndex'])
            totalData['everyTotalIndex'] = ';'.join(everyTotalIndex)
            yield Request(self.actor_url % id, meta={'id': id, 'totalData': totalData, 'info': '下载 %s actor' % id},
                          callback=self.parse_actor, errback=self.errback)
        except Exception as e:
            print('baidu', e)
            self.write_error('baidu' + id)

    def parse_actor(self, response):
        id = response.meta['id']
        try:
            totalData = response.meta['totalData']
            category = response.xpath(
                "//dl[@class='panel-main category']")
            category_data = {}
            for c in category:
                name = c.xpath(".//span[@class='title-name']/text()").extract_first()
                category_data[name] = []
                category_data[name + 'id'] = []
                p_item = c.xpath(".//div[@class='p-item']")
                for i in p_item:
                    category_data[name + 'id'].append(
                        ''.join(re.findall("\d+\.?\d*", i.xpath('./a/@href').extract_first())))
                    p_list = []
                    for p in i.xpath(".//div[@class='p-desc']/p/text()").extract():
                        p_list.append(p)
                    category_data[name].append(''.join(p_list))
                category_data[name] = ';'.join(category_data[name])
                category_data[name + 'id'] = ';'.join(category_data[name + 'id'])
            totalData.update(category_data)
            item = MaoyanItem()
            item['item'] = totalData
            self.document1.update({'id': id}, {'$set': {'status': '3'}}, True)
            yield item
        except Exception as e:
            print('actor', e)
            self.write_error('actor' + id)

    def errback(self, response):
        id = response.meta['id']
        self.write_error('download' + id)

    def write_error(self, info):
        with open('eroor', 'a') as w:
            w.write(info + '\n')

    def openlink(self, url):
        """
        urlopen error 10060错误
        :param url:  请求的网址
        :param headers: 报文头部信息
        :return: 服务器响应
        """
        maxTryNum = 15
        for tries in range(maxTryNum):
            try:
                logging.info("请求%s" % (url))
                req = requests.get(url, timeout=13, headers=self.headers)
                logging.info('请求成功%s' % url)
                return req
            except:
                if tries < (maxTryNum - 1):
                    continue
                else:
                    logger.info("尝试%d 次连接网址%s失败!" % (maxTryNum, url))
