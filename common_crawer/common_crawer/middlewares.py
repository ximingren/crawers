# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random

import requests

from common_crawer.MongoQueue import MongoQueue
from scrapy import signals
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet import error


class CommonCrawerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CommonCrawerDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    ban_ips = []

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if 'info' in request.meta.keys():
            logging.info(str(request.meta['info']) + ' 下载页面 ' + request.url)
        logging.info("准备请求下载%s页面" % request.url)

        logging.info("请求参数为%s" % str(request.body.decode('utf8')))
        if request.headers.get('Host') != 'm.douban.com':
            request.headers.setdefault("Referer", request.url)
        if spider.settings['USE_PROXY']:
            proxy = self.valid_proxies()
            if 'sec.douban' in request.url:
                print('ban掉')
                request.meta['proxy'] = proxy
            logging.info('使用代理%s' % proxy)
            request.meta['proxy'] = proxy
        print(request.meta)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if response.status == 200:

            logging.info("下载页面成功%s!!!!!!!!!!!" % response.url)
            return response
        else:
            return request

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response bject: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        logging.info("发生异常%s" % request.url)
        if isinstance(exception, TunnelError) or isinstance(exception, error.TimeoutError):
            logging.error("发生异常%s" % str(exception))
            if spider.settings['USE_PROXY']:
                logging.info("添加ban掉的代理地址%s" % request.meta['proxy'])
                self.ban_ips.append(request.meta['proxy'])
                proxy = self.valid_proxies()
                # proxy='http://104.238.146.146:8118'
                # request.meta['proxy'] = proxy
                return request
        with open('error.txt', 'a') as f:
            f.write(str(request.body))
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


    def get_ip1(self):
        print('代理池1')
        response = requests.get('http://localhost:8899/api/v1/proxies?anonymous=True&https=true')
        data = json.loads(response.text)
        proxies = random.choice(data['proxies'])
        if proxies['is_https']:
            proxy = {'https': 'https://' + str(proxies['ip']) + ":" + str(proxies['port'])}
        else:
            proxy = {'http': 'http://' + str(proxies['ip']) + ":" + str(proxies['port'])}
        return proxy['https']

    def get_ip2(self):
        print('代理池2')
        r = requests.get('http://127.0.0.1:8000/?types=0&count=5&country=%E5%9B%BD%E5%86%85&protocol=1')
        ip_ports = json.loads(r.text)
        ip = random.choice(ip_ports)[0]
        port = random.choice(ip_ports)[1]
        proxies = {
            'http': 'https://%s:%s' % (ip, port),
            'https': 'http://%s:%s' % (ip, port)
        }
        return proxies['https']

    def get_ip3(self):
        # proxy-pool,用的是redis 6378
        response = requests.get('http://127.0.0.1:5010/get_all/')
        print('代理池3')
        proxy = random.choice(list(response.json()))
        return 'https://' + proxy

    def get_ip7(self):
        print('代理池7')
        # IP-POOL
        res = requests.get('http://localhost:22555/get_all/')
        result = random.choice(res.json())
        return 'https://' + result

    def get_ip9(self):
        # fpserver
        print('代理池9')
        res = requests.get('http://localhost:12345/api/proxy/?count=100&scheme=HTTPs&anonymity=anonymous')
        proxy = random.choice(res.json()['data']['detail'])['url']
        return proxy

    def get_ip10(self):
        q = MongoQueue('proxy', 'zhima')
        return q.popProxy()['http']

    def valid_proxies(self):
        proxy = self.get_ip1()
        while proxy in self.ban_ips:
            proxy = self.get_ip1()
        return proxy
