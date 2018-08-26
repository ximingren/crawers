# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ZhihuuserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class UserItem(scrapy.Item):
    id=Field()
    name=Field()
    avatar_url=Field()
    headline=Field()
    description=Field()
    url=Field()
    url_token=Field()
    gender=Field()
    cover_url=Field()
    type=Field()
    bodge=Field()

    answer_count=Field()
    articles_count=Field()
    commercial_question_count=Field()
    favorite_count=Field()
    favorited_count=Field()
    follower_count=Field()
    following_columns_count=Field()
    following_count=Field()
    pins_count=Field()
    question_count=Field()
    thank_from_count=Field()
    thank_to_count=Field()
    thanked_count=Field()
    vote_from_count=Field()
    vote_to_count=Field()
    following_favlists_count=Field()
    following_question_count=Field()
    following_topic_count=Field()
    marked_answers_count=Field()
    mutual_followees_count=Field()
    hosted_live_count=Field()
    participated_live_count=Field()

    locations=Field()
    educations=Field()
    employments=Field()