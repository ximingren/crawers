# -*- coding: utf-8 -*-
import json
import re

import demjson
import scrapy
from scrapy import Request

from common_crawer.items import ZooplaItem
from scrapy.crawler import CrawlerProcess

from common_crawer import settings


class ZooplaSpider(scrapy.Spider):
    filed = ['has_modern_etc', 'latitude_min', 'country_code', 'region_name', 'market_stats', 'latitude',
             'agentAddress', 'has_house', 'incode', 'longitude_min', 'county_area_name', 'num_baths', 'furnished_state',
             'is_shared_ownership', 'has_garden', 'descrition', 'price', 'num_recepts', 'longitude_max',
             'property_type', 'bigAddress', 'has_floorplan', 'has_flat_studio', 'school_distance', 'title', 'longitude',
             'area_name', 'zindex', 'is_retirement_home', 'room_status', 'price_history_date', 'agentName', 'outcode',
             'num_beds', 'brand_name', 'id', 'branch_name', 'has_epc', 'post_town_name', 'room_condition',
             'subway_distance', 'postal_area', 'display_address', 'latitude_max', 'agentPhone', 'room_category']
    name = 'zoopla'
    page_url = 'https://www.zoopla.co.uk/search/?q=%s&geo_autocomplete_identifier=&price_min=&price_max=&property_type=&beds_min=&category=residential&price_frequency=per_month&furnished_state=&radius=&added=&results_sort=newest_listings&keywords=&new_homes=&retirement_homes=true&shared_ownership=&include_auctions=true&include_sold=&include_shared_accommodation=false&include_rented=true&search_source=to-rent&section=to-rent&view_type=list'
    address_list=settings.ADDRESS_LIST

    def start_requests(self):
        for address in self.address_list:
            addressNumber=self.address_list.index(address)
            info = 'address: %s\%s(%s)' % (addressNumber, len(self.address_list), address)
            yield Request(self.page_url % address, callback=self.parse_page, meta={'address': address,'page':'1', 'info':info,'addressNumber':addressNumber},dont_filter=True,
                          errback=self.errback)


    def errback(self, failure):
        response = failure.value.response
        meta = failure.value.meta
        print(failure)
        print(response)
        print(meta)

        # yield Request(response.url,meta=meta)

    def parse_page(self, response):
        idList = response.xpath("//*[@class='srp clearfix   ']/@data-listing-id").extract()
        pageList = response.xpath("//div[@class='paginate bg-muted']/a/text()").extract()
        pages = int(pageList[-2])
        now_page = response.meta['page']
        addressNumber=response.meta['addressNumber']
        address=response.meta['address']
        self.parse_detail(response)

        for id in idList:
                info='id: %s\%s page: %s\%s address: %s\%s'%(idList.index(id),len(idList),now_page,pages,addressNumber,len(self.address_list))
                detail_url = 'https://www.zoopla.co.uk/to-rent/details/%s' % id
                yield Request(detail_url, callback=self.parse_detail,
                              meta={'id': str(id), 'address': response.meta['address'],'info':info})
        if int(now_page) == 1:
            for page in range(2, pages):
                info='page: %s\%s  address: %s\%s(%s)'%(str(page),pages,addressNumber,len(self.address_list),address)
                yield Request(response.url+'&pn='+str(page), callback=self.parse_page,
                              meta={'page': page, 'address': response.meta['address'],'info':info,'addressNumber':addressNumber})

    def parse_detail(self, response):
        item = {}
        item['has_garden'] = 0
        item['has_modern_etc'] = 0
        item['has_flat_studio'] = 0
        item['has_house'] = 0
        address=response.meta['address']
        id=response.meta['id']
        market_stats = ''.join(response.xpath("//span[@class='dp-market-stats__price']//text()").extract())
        descrition = list(filter(lambda t: t != '', map(lambda x: x.strip(), response.xpath(
            "//section[@class='dp-features']/ul[@class='dp-features__list ui-list-bullets']//text()").extract())))
        price = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), response.xpath(
            "//div[@class='dp-sidebar-wrapper']//div[@class='ui-pricing']/p[@class='ui-pricing__main-price']//text()").extract()))))
        price = ''.join(re.findall("\d+\.?\d*", price))
        self.detect(descrition, item)
        descrition = ','.join(descrition)
        price_history_date = ''.join(response.xpath("//span[@class='dp-price-history__item-date']//text()").extract())
        distance = response.xpath(
            "//div[@class='ui-interactive-map']//ul[@class='ui-local-amenities__list ui-list-flat']//text()").extract()
        distance = list(filter(lambda t: t != '', map(lambda x: x.strip(), distance)))
        self.get_distance(distance, item)
        market_stats = ''.join(re.findall("\d+\.?\d*", market_stats))
        title = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), response.xpath(
            "//h1[@class='ui-prop-summary__title ui-title-subgroup']/text()").extract()))))
        self.get_agent(response, item)
        if 'flat' in title or 'studio' in title:
            item['has_flat_studio'] = 1
        if 'house' in title:
            item['has_house'] = 1
        self.get_mapData(response, item)

        item['price'] = price
        item['descrition'] = descrition
        item['market_stats'] = market_stats
        item['price_history_date'] = price_history_date
        item['title'] = title

        item['bigAddress'] = address
        item['id'] = id
        zooplaItem=ZooplaItem()
        zooplaItem['item']=item
        yield zooplaItem

    def detect(self,descrition, item):
        for x in descrition:
            if 'garden' in x:
                item['has_garden'] = 1
            if 'modern' in x or 'high standard' in x or 'good qualitu' in x or 'renovated' in x:
                item['has_modern_etc'] = 1

    def get_distance(self,distance, item):
        subway_distance = []
        school_distance = []
        for i in distance[0:3]:
            if 'miles' in i:
                subway_distance.append(''.join(re.findall("\d+\.?\d*", i)))
        for i in distance[3:]:
            if 'miles' in i:
                school_distance.append(''.join(re.findall("\d+\.?\d*", i)))
        subway_distance = min(subway_distance)
        school_distance = min(school_distance)
        item['subway_distance'] = subway_distance
        item['school_distance'] = school_distance

    def get_agent(self,res, item):
        agentName = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), res.xpath(
            "//h4[@class='ui-agent__name']//text()").extract()))))
        agentAddress = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), res.xpath(
            "//address[@class='ui-agent__address']//text()").extract())))[0])
        try:
            agentPhone = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), res.xpath(
                "//p[@class='ui-agent__tel ui-agent__text']/a//text()").extract()[1]))))
        except Exception as e:
            print(e)
        else:
            item['agentPhone'] = agentPhone
        item['agentName'] = agentName
        item['agentAddress'] = agentAddress

    def get_mapData(self,res, item):
        mapData = res.text[
                  res.text.find('ZPG.mapData') + len('ZPG.mapData = '):res.text.find(
                      'ZPG.poiMapData = ')].strip().strip(
            ';')
        mapData = json.loads(mapData)
        bounding_box = mapData['bounding_box']
        coordinates = mapData['coordinates']
        del coordinates['is_approximate']
        item.update(bounding_box)
        item.update(coordinates)
        address_info = res.text[
                       res.text.find('ZPG.trackData.taxonomy') + len('ZPG.trackData.taxonomy = '):res.text.find(
                           'ZPG.trackData.taxonomy.activity')].strip().strip(';')
        address_info = demjson.decode(address_info)
        item['area_name'] = address_info['area_name']
        item['country_code'] = address_info['country_code']
        item['county_area_name'] = address_info['county_area_name']
        item['room_category'] = address_info['listings_category']
        item['postal_area'] = address_info['postal_area']
        item['region_name'] = address_info['region_name']
        item['outcode'] = address_info['outcode']
        item['post_town_name'] = address_info['post_town_name']
        item['branch_name'] = address_info['branch_name']
        item['brand_name'] = address_info['brand_name']
        item['display_address'] = address_info['display_address']
        item['furnished_state'] = address_info['furnished_state']
        item['has_epc'] = address_info['has_epc']
        item['has_floorplan'] = address_info['has_floorplan']
        item['incode'] = address_info['incode']
        item['is_retirement_home'] = address_info['is_retirement_home']
        item['is_shared_ownership'] = address_info['is_shared_ownership']
        item['room_status'] = address_info['listing_status']
        item['num_baths'] = address_info['num_baths']
        item['num_beds'] = address_info['num_beds']
        item['num_recepts'] = address_info['num_recepts']
        item['property_type'] = address_info['property_type']
        item['zindex'] = address_info['zindex']
        item['room_condition'] = address_info['listing_condition']

# if __name__ == '__main__':
#
#     process = CrawlerProcess()
#     process.crawl(ZooplaSpider)
#     process.start()

# CrawlerProcess和crawlerRunner有什么不同
# runner=CrawlerRunner()
# d=runner.crawl(ZooplaSpider)
# d.addBoth(lambda _:reactor.stop())
# reactor.run()
