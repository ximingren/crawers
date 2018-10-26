# -*- coding: utf-8 -*-
import logging
import time
import scrapy
from common_crawer.items import _58CrawerItem
from scrapy import Request


class A58Spider(scrapy.Spider):
    name = '58'
    url = 'http://gz.58.com/%s/ershoufang/pn%d/'
    area = {
        'tianhe': '天河', 'haizhu': '海珠', 'yuexiu': "越秀", 'hengliqz': "横沥", 'baiyun': "白云",
        'liwan': "荔湾", 'panyu': "番禺", 'huangpu': "黄浦", 'huadu': "花都", 'zengcheng': "增城"
    }
    condition = True

    def start_requests(self):
        for area in self.area.keys():
            yield Request(self.url % (area, 1), callback=self.parse_pages, meta={'area': area})

    def parse_pages(self, response):
        # if response.xpath('.//input[@id="btnSubmit"]'):
        #     if self.condition:
        #         browser=webdriver.Chrome('/home/ximingren/Projects/Projects/crawer_summary/chromedriver')
        #         self.condition=False
        #         browser.get(response.url)
        # else:
        if not response.xpath('.//input[@id="btnSubmit"]'):
            self.condition = True
            pages = int(response.xpath('.//div[@class="pager"]//a[last()-1]//text()')[0].extract())
            area = response.meta['area']
            yield Request(self.url % (area, 1), callback=self.parse_price, dont_filter=True,
                          meta={'pages': pages, 'current_page': 1, 'area': area})

    def parse_price(self, response):
        # if response.xpath('.//input[@id="btnSubmit"]'):
        #     if self.condition:
        #         browser = webdriver.Chrome('/home/ximingren/Projects/Projects/crawer_summary/chromedriver')
        #         self.condition=False
        #         browser.get(response.url)
        # else:
        if not response.xpath('.//input[@id="btnSubmit"]'):
            self.condition = True
            current_page = response.meta['current_page']
            pages = response.meta['pages']
            house_list = response.xpath('.//ul[@class="house-list-wrap"]/li')
            area = response.meta['area']
            for house in house_list:
                name = ''.join(house.xpath('./div[@class="list-info"]/h2/a/text()').extract())
                baseinfo = ''.join(
                    list(filter(lambda x: '\n' not in x,
                                house.xpath('./div[@class="list-info"]/p//span/text()').extract())))
                jjr_info = ''.join(house.xpath('.//div[@class="jjrinfo"]/span/text()').extract()) + ''.join(
                    house.xpath('.//div[@class="jjrinfo"]/a/span/text()').extract())
                sum_price = ''.join(house.xpath('./div[@class="price"]/p[@class="sum"]//text()').extract())
                unit_price = ''.join(house.xpath('./div[@class="price"]/p[@class="unit"]/text()').extract())
                house_time = ''.join(house.xpath('./div[@class="time"]/text()').extract())
                if house_time == '今天':
                    house_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                _58Item = _58CrawerItem()
                _58Item['name'] = name
                _58Item['baseinfo'] = baseinfo
                _58Item['jjr_info'] = jjr_info
                _58Item['sum_price'] = sum_price
                _58Item['unit_price'] = unit_price
                _58Item['house_time'] = house_time
                _58Item['city'] = '广州'
                _58Item['area'] = self.area[area]
                yield _58Item
            current_page = current_page + 1
            if current_page <= pages:
                yield Request(self.url % (area, current_page), callback=self.parse_price,
                              meta={'pages': pages, 'current_page': current_page, 'area': area})
