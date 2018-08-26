import json
import random

import requests
import scrapy
from scrapy import Request

from lianjia.items import LianjiaItem


class LianjiaPrices(scrapy.Spider):
    name='lianjia'
    need_city=['bj','sh','gz']
    url="https://%s.fang.lianjia.com/loupan"
    # def process_request(self,request,spider):
    #     response = requests.get('http://localhost:8899/api/v1/proxies?anonymous=True')
    #     data = json.loads(response.text)
    #     proxies = random.choice(data['proxies'])
    #     if proxies['is_https']:
    #         proxy = 'https://' + str(proxies['ip']) + ":" + str(proxies['port'])
    #     else:
    #         proxy = 'http://' + str(proxies['ip']) + ":" + str(proxies['port'])
    #     request.meta['proxy']=proxy

    def start_requests(self):
        # yield  Request('http://ip.filefab.com/index.php',callback=self.parse_ip)
        yield Request(self.url%self.need_city[0],callback=self.parse_prices)

    def parse_prices(self,response):
        name=response.xpath('.//div[@class="resblock-name"]/a[@class="name"]//text()').extract()
        type=response.xpath('.//div[@class="resblock-name"]/span[@class="resblock-type"]//text()').extract()
        status=response.xpath('.//div[@class="resblock-name"]/span[@class="sale-status"]//text()').extract()
        location=response.xpath('.//div[@class="resblock-location"]//text()').extract()
        area=response.xpath('.//div[@class="resblock-area"]//text()').extract()
        agent=response.xpath('.//div[@class="resblock-agent"]//text()').extract()
        tag=response.xpath('.//div[@class="resblock-tag"]//text()').extract()
        price=response.xpath('.//div[@class="resblock-price"]/div/span[@class="number"]//text()').extract()
        item=LianjiaItem()
        item['name']=name
        item['resblock_type']=type
        item['sale_status']=status
        item['location']=location
        item['resblock_area']=area
        item['resblock_agent']=agent
        item['resblock_tag']=tag
        item['resblock_price']=price
        yield item

