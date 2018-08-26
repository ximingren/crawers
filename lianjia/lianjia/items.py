# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    resblock_type=scrapy.Field()
    sale_status=scrapy.Field()
    location=scrapy.Field()
    resblock_area=scrapy.Field()
    resblock_agent=scrapy.Field()
    resblock_tag=scrapy.Field()
    resblock_price=scrapy.Field()
