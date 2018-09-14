# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class _58CrawerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    baseinfo = scrapy.Field()
    jjr_info = scrapy.Field()
    sum_price = scrapy.Field()
    unit_price = scrapy.Field()
    house_time = scrapy.Field()
    city=scrapy.Field()
    area=scrapy.Field()

class MeituanHotelItem(scrapy.Item):
    name =scrapy.Field()
    addr = scrapy.Field()
    areaName = scrapy.Field()
    score =scrapy.Field()
    lowestPrice = scrapy.Field()
    poiid =scrapy.Field()
    poiRecommendTag = scrapy.Field()
    poiAttrTagList =scrapy.Field()
    historyCouponCount =scrapy.Field()
    commentsCountDesc = scrapy.Field()
    startDay=scrapy.Field()
    endDay=scrapy.Field()
    cityName=scrapy.Field()