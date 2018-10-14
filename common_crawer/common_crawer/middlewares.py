# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random

import requests
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
        logging.info("准备请求下载%s页面" % request.url)
        logging.info("请求参数为%s"%str(request.body.decode('utf8')))
        request.headers.setdefault("Referer", request.url)
        if spider.settings['USE_PROXY']:
            proxy = self.valid_proxies()
            # proxy="https://185.93.3.70:8080"
            logging.info('使用代理%s' % proxy)
            request.meta['proxy'] = proxy
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if response.status == 200:
            logging.error("下载页面成功%s!!!!!!!!!!!"%response.url)
            return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response bject: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        logging.info("发生异常%s"%request.url)
        if isinstance(exception, TunnelError) or isinstance(exception, error.TimeoutError):
            logging.error("发生异常%s" % str(exception))
            if spider.settings['USE_PROXY']:
                logging.info("添加ban掉的代理地址%s" % request.meta['proxy'])
                self.ban_ips.append(request.meta['proxy'])
                proxy = self.valid_proxies()
                # proxy='http://104.238.146.146:8118'
                # request.meta['proxy'] = proxy
                return request
        with open('error.txt','a') as f:
            f.write(str(request.body))
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def get_proxy(self):
        # response = requests.get('http://localhost:8899/api/v1/proxies?anonymous=True')
        # data = json.loads(response.text)
        # proxies = random.choice(data['proxies'])
        # if proxies['is_https']:
        #     proxy = 'https://' + str(proxies['ip']) + ":" + str(proxies['port'])
        # else:
        #     proxy = 'http://' + str(proxies['ip']) + ":" + str(proxies['port'])
        # return proxy

        # response=requests.get('http://localhost:12345/api/proxy/')
        # data=response.json()
        # return data['data']['detail'][0]['url']
        response=requests.get('http://127.0.0.1:5010/get/')
        return 'http://'+response.text

    def valid_proxies(self):
        proxy = self.get_proxy()
        while proxy in self.ban_ips:
            proxy = self.get_proxy()
        return proxy