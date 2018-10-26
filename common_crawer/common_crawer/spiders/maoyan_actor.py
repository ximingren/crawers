import os
import re

import requests
import scrapy
from fontTools.ttLib import TTFont
from scrapy import Request

from common_crawer.items import MaoyanActorItem


class MaoyanActorSpider(scrapy.Spider):
    name = 'actor'
    url = 'http://maoyan.com/films/celebrity/%s'
    fonts_dir = '/home/ximingren/Projects/Projects/crawer_summary/common_crawer/common_crawer/test_case/maoyan/fonts/'

    def start_requests(self):
        for id in range(20257,100000):
            yield Request(self.url % str(id),meta={'id':str(id),'info':'%s'%str(id)})

    def parse(self, response):
        id=response.meta['id']
        actor={}
        name = response.xpath('.//p[@class="china-name cele-name"]/text()').extract_first()
        if name!='' or name:

            font_file = re.findall(r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', response.text)[0]
            font = self.create_font(font_file)
            sumBox = response.xpath(".//div[@class='cele-index sumBox']/p[@class='index-num']/span/text()").extract()
            ranking = response.xpath(".//div[@class='cele-index']")[0].xpath(
                "./p[@class='index-num']/span/text()").extract()
            fans = response.xpath(".//div[@class='cele-index']")[1].xpath(
                "./p[@class='index-num followCount']/span/text()").extract()
            if len(sumBox)!=0:
                sumBox = self.modify_data(font, sumBox)
                actor['sumBox'] = sumBox
            if len(ranking)!=0:
                ranking = self.modify_data(font, ranking)
                actor['ranking'] = ranking
            if len(fans)!=0:
                fans = self.modify_data(font, fans)
                actor['fans'] = fans
            engName = response.xpath('.//p[@class="eng-name cele-name"]/text()').extract_first()
            profession = response.xpath('.//span[@class="profession"]/text()').extract_first()
            birthday = response.xpath('.//span[@class="birthday"]/text()').extract_first()
            height = response.xpath('.//span[@class="height"]/text()').extract_first()
            master_item = response.xpath('.//li[@class="master-item"]/a/div')
            masterList = []
            for m in master_item:
                masterList.append(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), m.xpath('string(.)').extract())))))
            masterList = ';'.join(masterList)
            award_detail = response.xpath('.//div[@class="award-slider award-class slider"]/div')
            awardList = []
            for a in range(len(award_detail)):
                i = award_detail[a]
                header = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), i.xpath('.//text()').extract()))))
                award = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(),
                                                                   response.xpath(".//div[@class='award-detail']/div")[a].xpath(
                                                                       './/text()').extract())))).replace('\n','').replace(' ','').replace('/\xa0','')
                awardList.append(header + ":" + award)
            awardList = ';'.join(awardList)
            relations = response.xpath('.//div[@class="rel-item"]')
            relationsList = []
            for r in relations:
                relationsList.append(
                    ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), r.xpath('.//text()').extract())))))
            relationsList = ';'.join(relationsList)
            actor['id']=id
            actor['name']=name
            actor['engName']=engName
            actor['profession']=profession
            actor['birthday']=birthday
            actor['birthday']=birthday
            actor['height']=height
            actor['masterList']=masterList
            actor['awardList']=awardList
            actor['relationsList']=relationsList
            item=MaoyanActorItem()
            item['item']=actor
            yield item

    def create_font(self, font_file):
        # 列出已下载文件
        file_list = os.listdir(self.fonts_dir)
        # 判断是否已下载
        if font_file not in file_list:
            # 未下载则下载新库
            print('不在字体库中, 下载:', font_file)
            url = 'http://vfile.meituan.net/colorstone/' + font_file
            # new_file = self.get_html(url)
            new_file = requests.get(url).content
            with open(self.fonts_dir + font_file, 'wb') as f:
                f.write(new_file)

        # 打开字体文件，创建 self.font属性
        font = TTFont(self.fonts_dir+ font_file)
        return font

    def modify_data(self, font, data):
        # 获取 GlyphOrder 节点
        font1 = TTFont(self.fonts_dir + 'aa56b793571a4be38ebf0686685a55a62080.woff')
        keys = sorted(font1['glyf'].keys())
        values = list(' 2038146957.')
        # 构建基准 {name: num}
        dict1 = dict((k, v) for k, v in zip(keys, values))
        dict2 = {}
        for key in font['glyf'].keys():
            for k, v in dict1.items():
                # 通过比较 字形定义 填充新的name和num映射关系
                if font1['glyf'][k] == font['glyf'][key]:
                    key = key.replace('uni', "").lower()
                    dict2[key] = v.strip()
                    break
        result = []
        for i in data[0]:
            if i == '.':
                result.append(i)
            for k, v in dict2.items():
                if k in '%r' % i:
                    result.append(dict2[k])
        if len(data) == 2:
            return ''.join(result) + data[1]
        else:
            return ''.join(result)
