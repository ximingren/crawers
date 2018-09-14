import json
import random

import requests
import scrapy
from scrapy import Request
import logging

from scrapy_project.items import LianjiaItem


# User timeout caused connection failure.
# : Could not open CONNECT tunnel with proxy
# Internal Server Error
# 发生错误的request不会回到List中
class LianjiaPrices(scrapy.Spider):
    name = 'scrapy_project'
    need_city = {'cd': "成都",
                 'cs': "长沙",
                 'dl': "大连",
                 'hz': "杭州",
                 'jn': '济南',
                 'nj': "南京",
                 'qd': "青岛",
                 'sjz': "石家庄",
                 'sy': "沈阳",
                 'sz': "深圳",
                 'tj': "天津",
                 'wh': '武汉',
                 'xa': "西安",
                 'xm': "厦门",
                 'yt': "烟台",
                 'hf': "合肥",
                 'fs': "佛山",
                 'zs': "中山",
                 'ty': "太原",
                 'lf': "廊坊",
                 'hui': "惠州",
                 'wx': "无锡",
                 'zz': "郑州",
                 'km': "昆明"}
    url = "https://%s.fang.scrapy_project.com/loupan/pg%s"
    current_city = 0
    handle_httpstatus_list = [404, 403]
    # def process_request(self,request,spider):
    #     response = requests.get('http://localhost:8899/api/v1/proxies?anonymous=True')
    #     data = json.loads(response.text)
    #     proxies = random.choice(data['proxies'])
    #     if proxies['is_https']:
    #         proxy = 'https://' + str(proxies['ip']) + ":" + str(proxies['port'])
    #     else:
    #         proxy = 'http://' + str(proxies['ip']) + ":" + str(proxies['port'])
    #     request.meta['proxy']=proxy
    total_pages = 0

    def start_requests(self):
        current_page = 1
        # yield  Request('http://ip.filefab.com/index.php',callback=self.parse_ip)
        for city in self.need_city.keys():
            craw_url = self.url % (city, current_page)
            yield Request(craw_url, callback=self.parse_pages, meta={
                'city': city,
                'current_page': current_page})

    def parse_pages(self, response):
        pages = int(round(int(response.xpath('.//div[@class="page-box"]/@data-total-count').extract_first()) / 10.0))
        yield Request(response.url, callback=self.parse_prices,dont_filter=True,
                      meta={
                          'city': response.meta['city'], 'pages': pages, 'current_page': response.meta['current_page']
                      })

    def parse_prices(self, response):
        logging.info("下载%s页面成功" % response.url)
        resblock_divs = response.xpath('//div[@class="resblock-desc-wrapper"]')
        # current_page=int(response.xpath('.//div[@class="page-box"]/@data-current').extract_first())
        pages = response.meta['pages']
        current_page = response.meta['current_page']
        for div in resblock_divs:
            name = div.xpath('.//div[@class="resblock-name"]/a[@class="name"]//text()').extract_first()
            type = div.xpath('.//div[@class="resblock-name"]/span[@class="resblock-type"]//text()').extract_first()
            status = div.xpath('.//div[@class="resblock-name"]/span[@class="sale-status"]//text()').extract_first()
            location = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), div.xpath(
                './/div[@class="resblock-location"]//text()').extract()))))
            area = list(filter(lambda t: t != '', map(lambda x: x.strip(), div.xpath(
                './/div[@class="resblock-area"]//text()').extract_first())))
            # agent=list(filter(lambda t:t!='',map(lambda x:x.strip(),div.xpath('.//span[@class="agent"]//text()').extract())))
            tag = list(filter(lambda t: t != '',
                              map(lambda x: x.strip(), div.xpath('.//div[@class="resblock-tag"]//text()').extract())))
            price = div.xpath('.//div[@class="resblock-price"]/div/span[@class="number"]//text()').extract_first()
            item = LianjiaItem()
            item['name'] = name
            item['resblock_type'] = type
            item['sale_status'] = status
            item['location'] = location
            item['resblock_area'] = area
            # item['resblock_agent']=agent
            item['resblock_tag'] = tag
            item['resblock_price'] = price
            item['city'] = self.need_city[response.meta['city']]
            yield item
        if current_page < pages:
            for x in range(2, pages):
                current_page = current_page + 1
                if current_page < pages:
                    craw_url = self.url % (response.meta['city'], current_page)
                    yield Request(craw_url, callback=self.parse_prices, meta={
                        'city': response.meta[
                            'city'],
                        'pages': pages,
                        'current_page':
                            current_page
                    })
