import json

import scrapy
from common_crawer.items import MaoyanItem

from common_crawer.MongoQueue import MongoQueue
from scrapy import Request


class DoubanSpider(scrapy.Spider):
    name = 'doubanFilm'
    awardUrl = 'https://movie.douban.com/subject/%s/awards/'
    topicUrl = 'https://m.douban.com/rexxar/api/v2/gallery/subject_feed?start=%s&count=4&subject_id=%s&ck=null'
    doubanqueue = MongoQueue('douban', 'url')

    def start_requests(self):
        while True:
            try:
                id,url,star = self.doubanqueue.pop()
            except KeyError:
                print('队列没有数据')
                break
            else:
                data={}
                data['id']=id
                data['url']=url
                data['star']=star
                yield Request(url, meta={'id': id, 'data': data}, callback=self.parse_detail, errback=self.errback)

    def parse_detail(self, response):
        id = response.meta['id']
        data = response.meta['data']
        name = response.xpath("//div[@id='content']/h1/span[1]/text()").extract_first()
        year = response.xpath("//div[@id='content']/h1/span[2]/text()").extract_first()
        content = response.xpath('//div[@class="subject clearfix"]/div[@id="info"]//text()').extract()
        self.parse_content(content, data)
        rating_num = response.xpath("//strong[@class='ll rating_num']/text()").extract_first()
        rating_people = response.xpath('//a[@class="rating_people"]/span//text()').extract_first()
        rating_item = response.xpath('//div[@class="ratings-on-weight"]/div')
        rating_betterthan = ' '.join(list(
            filter(lambda t: t != '',
                   map(lambda x: x.strip(), response.xpath("//div[@class='rating_betterthan']//text()").extract()))))
        rating_stars = []
        for weight in rating_item:
            rating_stars.append(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(),
                                                                           weight.xpath(
                                                                               './span[1]/text()').extract_first() + weight.xpath(
                                                                               './span[2]/text()').extract_first())))))
        recommendations = response.xpath("//div[@class='recommendations-bd']/dl")
        recommend = []
        for r in recommendations:
            recommend.append(r.xpath('./dd/a/text()').extract_first())
        tags = response.xpath("//div[@class='tags']/div/a/text()").extract()
        data['name'] = name
        data['year'] = year
        data['tags'] = '/'.join(tags)
        data['recommend'] = '/'.join(recommend)
        data['rating_num'] = rating_num
        data['rating_people'] = rating_people
        data['rating_stars'] = '/'.join(rating_stars)
        data['rating_betterthan'] = rating_betterthan
        yield Request(self.awardUrl % id, callback=self.parse_award, errback=self.errback,
                      meta={'id': id, 'data': data})

    def parse_award(self, response):
        id=response.meta['id']
        data = response.meta['data']
        awardsList = response.xpath("//div[@class='article']/div")
        awards_result = {}
        for awards in awardsList:
            awardName = ''.join(list(
                filter(lambda t: t != '',
                       map(lambda x: x.strip(), awards.xpath("./div[@class='hd']/h2//text()").extract()))))
            awards_result[awardName] = list()
            awardList = awards.xpath('.//ul')
            for award in awardList:
                awards_result[awardName].append(
                    ''.join(
                        list(filter(lambda t: t != '', map(lambda x: x.strip(), award.xpath('.//text()').extract())))))
            awards_result[awardName] = ';'.join(awards_result[awardName])
        result = []
        for key, value in awards_result.items():
            result.append(key + ":" + value)
        data['awards'] = ','.join(result)
        yield Request(self.topicUrl % ('0',id), meta={'id': id, 'data': data}, callback=self.parse_topic,headers={'Host':'m.douban.com','Referer':'https://movie.douban.com/subject/%s/'%id},
                      errback=self.errback)

    def parse_topic(self, response):
        id = response.meta['id']
        data = response.meta['data']
        topicData = json.loads(response.text)
        topic = []
        for i in topicData['items']:
            topic.append(i['topic']['name'] + ":" + i['topic']['card_subtitle'])
        data['topics'] = '/'.join(topic)
        item=MaoyanItem()
        item['item']=data
        self.doubanqueue.completeId(id)
        yield  item

    def parse_content(self, Content, data):
        valueList = ''.join(Content).split(Content[0])
        for i in valueList:
            if i != '':
                try:
                    key = i.split(':')[0]
                    value = i.split(':')[1]
                except:
                    pass
                else:
                    if key == 'IMDb链接':
                        data[key] = 'https://www.imdb.com/title/' + value.replace('\n', '') + '/'
                    else:
                        data[key] = value

    def errback(self, response):
        id = response.meta['id']
        self.write_error('download' + id)

    def write_error(self, info):
        with open('douban', 'a') as w:
            w.write(info + '\n')
