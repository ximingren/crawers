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


class MeituanWaiMaiItem(scrapy.Item):
    pass

class Cboocn(scrapy.Item):
    name=scrapy.Field()
    enName=scrapy.Field()
    boxOffice_total=scrapy.Field()
    now_boxOffice=scrapy.Field()
    genre=scrapy.Field()
    runTime=scrapy.Field()
    releaseDate=scrapy.Field()
    standard=scrapy.Field()
    country=scrapy.Field()
    director=scrapy.Field()
    starring=scrapy.Field()
    production_co=scrapy.Field()
    distribution_co=scrapy.Field()
    inland_avg=scrapy.Field()
    inland_week=scrapy.Field()
    inland_total=scrapy.Field()
    inland_days=scrapy.Field()
    hk_rank=scrapy.Field()
    hk_week=scrapy.Field()
    hk_total=scrapy.Field()
    am_rank=scrapy.Field()
    am_week=scrapy.Field()
    am_total=scrapy.Field()
    EnMovieID=scrapy.Field()

class Ebotapp(scrapy.Item):
    item=scrapy.Field()
    # MovieName=scrapy.Field() #电影名称
    # dirctor=scrapy.Field() #导演
    # actor=scrapy.Field() #演员
    # producer=scrapy.Field() #制片人
    # screenwriter=scrapy.Field() #编剧
    # art=scrapy.Field() #美术
    # film_distrbution_corporation=scrapy.Field() #发行公司
    # ReleaseDate=scrapy.Field() #上映时间
    # BoxOfficeToTal=scrapy.Field() # 累计票房
    # BoxOfficePoint=scrapy.Field() #点映票房
    # BoxOfficeFirstDay=scrapy.Field() # 首日票房
    # BoxOfficeFirstWeek=scrapy.Field() #首周票房
    # Genre=scrapy.Field() #电影类型
    # GenreMain=scrapy.Field() #电影主类型
    # Runtime=scrapy.Field() #时长
    # BoxOfficeEveryDay=scrapy.Field() #每日总票房
    # screeningsEveryDay=scrapy.Field() #每日场次
    # boxOffice_distribution=scrapy.Field() #票房分布
    # BuyTicketIndex=scrapy.Field() #购票指数
    # RenZhiIndex=scrapy.Field() #认知指数
    # RapIndex=scrapy.Field() #口碑指数
    # age_distribution=scrapy.Field() #年龄分布
    # area_distribution=scrapy.Field() #地域分布
    # gender_distribution=scrapy.Field() # 性别分布

