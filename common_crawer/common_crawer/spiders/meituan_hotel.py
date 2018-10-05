# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from common_crawer.items import MeituanHotelItem


class MeituanHotelSpider(scrapy.Spider):
    name = 'meituan_hotel'
    pois_list_params = {
        'cityId': '{cityId}',
        'offset': '{offset}',
        'limit': str(20),
        'startDay':'{startDay}',
        'endDay': '{endDay}',
        'areald': str(1),
        # 'q':'',
        # 'hotelStar':1,
        # 'brandid':1,
        # 'price':''
    }
    # allowed_domains = ['meituan.com']
    # start_urls = ['http://meituan.com/']
    pois_list_url='https://ihotel.meituan.com/hbsearch/HotelSearch?version_name=999.99&cateId=20&attr_28=129'
    startDay='20180904'
    endDay='20180905'

    def start_requests(self):
        for key, val in self.pois_list_params.items():
            self.pois_list_url += "&%s=%s" % (key, val)
        with open('/home/ximingren/Projects/Projects/crawer_summary/common_crawer/common_crawer/meituan_city.json', 'r') as f:
            city_list = json.loads(f.read())
            for x in city_list['data']:
                cityId = x['id']
                cityName = x['name']
                yield Request(self.pois_list_url.format(cityId=str(cityId), offset=str(0),
                            startDay=self.startDay,endDay=self.endDay),callback=self.parse_count,
                              meta={'cityId':str(cityId),'cityName':cityName})

    def parse_count(self,response):
        pois_list=json.loads(response.text)
        totalCount=pois_list['data']['totalcount']
        cityId = response.meta['cityId']
        cityName=response.meta['cityName']
        if not (totalCount==0):
            for count in range(int(round(totalCount/20.0))):
                yield Request(self.pois_list_url.format(cityId=cityId, offset=str(count * 20),startDay=self.startDay,endDay=self.endDay),dont_filter=True,
                              callback=self.parse_pois, meta={'cityId': str(cityId),'cityName':cityName})
    def parse_pois(self,response):
        pois_list = json.loads(response.text)
        searchResult_list = pois_list['data']['searchresult']
        cityName=response.meta['cityName']
        for each in searchResult_list:
            hotelItem = MeituanHotelItem()
            hotelItem['name'] = each['name']
            hotelItem['addr'] = each['addr']
            hotelItem['areaName'] = each['areaName']
            hotelItem['score'] = each['avgScore']
            hotelItem['lowestPrice'] = each['lowestPrice']
            hotelItem['poiid'] = each['poiid']
            hotelItem['poiRecommendTag'] = each['poiRecommendTag']
            hotelItem['poiAttrTagList'] = each['poiAttrTagList']
            hotelItem['historyCouponCount'] = each['historyCouponCount']
            hotelItem['commentsCountDesc'] = each['commentsCountDesc'][:-3]
            hotelItem['startDay'] = self.startDay
            hotelItem['endDay']=self.endDay
            hotelItem['cityName']=cityName
            yield hotelItem
