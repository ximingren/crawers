# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from scrapy import Request

from common_crawer.items import Cboocn


class CboocnSpider(scrapy.Spider):
    name = 'cboocn'

    # allowed_domains = ['cboocn.cn']
    # start_urls = ['http://cboocn.cn/']

    def start_requests(self):
        for id in range(650000, 670000):
            yield Request('http://www.cbooo.cn/m/%s' % str(id), meta={'EnMovieID': str(id)})

    def get_block_office(self,tree):
        boxOffice_block = tree.xpath(
            '//div[@class="ziliaofr"]/div[@class="cont"]/p/span/text()')
        if len(boxOffice_block)>=2:
            if boxOffice_block[0] == '累计票房':
                boxOffice_total = boxOffice_block[1][:-1]
                return boxOffice_total, None
            else:
                boxOffice_total = boxOffice_block[3][:-1]
                now_boxOffice = boxOffice_block[1][:-1]
                return boxOffice_total, now_boxOffice
        else:
            return None,None
    def get_office(self, data, style):
        if style == 1:
            hk_am_rank = []
            hk_am_boxOffice_total = []
            hk_am_oneWeekOffice = []
            hk_am_parts = int(len(data) / 5)
            for i in range(hk_am_parts):
                week_boxOffice = data[5 * i:5 * (i + 1)]
                hk_am_rank.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[2])
                hk_am_oneWeekOffice.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[3])
                hk_am_boxOffice_total.append(
                    week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[4])
            return hk_am_rank[::-1], hk_am_oneWeekOffice[::-1], hk_am_boxOffice_total[::-1]
        else:
            inland_days = []
            inland_boxOffice_total = []
            inland_oneWeekOffice = []
            inland_avePeople = []
            parts = int(len(data) / 6)
            for i in range(parts):
                week_boxOffice = data[6 * i:6 * (i + 1)]
                inland_avePeople.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[2])
                inland_oneWeekOffice.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[3])
                inland_boxOffice_total.append(
                    week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[4])
                inland_days.append(week_boxOffice[0] + "(" + week_boxOffice[1] + ")" + ":" + week_boxOffice[5])
            return inland_avePeople[::-1], inland_oneWeekOffice[::-1], inland_boxOffice_total[::-1], inland_days[::-1]

    def get_inland(self, tree):
        if '内地票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[1]//text()')):
            inland_boxOffice = list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
                '//*[@id="tabcont2"]/table[1]//tr[position()>1]//text()'))))
            return inland_boxOffice
        elif '内地票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[2]//text()')):
            inland_boxOffice = list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
                '//*[@id="tabcont2"]/table[2]//tr[position()>1]//text()'))))
            return inland_boxOffice
        elif '内地票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[3]//text()')):
            inland_boxOffice = list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
                '//*[@id="tabcont2"]/table[3]//tr[position()>1]//text()'))))
            return inland_boxOffice
        else:
            return []

    def get_hk(self, tree):
        if '香港票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[1]//text()')):
            hk_boxOffice = list(filter(lambda t: t != '',
                                       map(lambda x: x.strip(),
                                           tree.xpath('//*[@id="tabcont2"]/table[1]/tbody//tr//text()'))))
            return hk_boxOffice
        elif '香港票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[2]//text()')):
            hk_boxOffice = list(filter(lambda t: t != '',
                                       map(lambda x: x.strip(),
                                           tree.xpath('//*[@id="tabcont2"]/table[2]/tbody//tr//text()'))))
            return hk_boxOffice
        elif '香港票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[3]//text()')):
            hk_boxOffice = list(filter(lambda t: t != '',
                                       map(lambda x: x.strip(),
                                           tree.xpath('//*[@id="tabcont2"]/table[3]/tbody//tr//text()'))))
            return hk_boxOffice
        else:
            return []

    def get_am(self, tree):
        if '北美票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[1]//text()')):
            am_boxOffice = list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
                '//*[@id="tabcont2"]/table[1]//tr[position()>1]//text()'))))
            return am_boxOffice
        elif '北美票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[2]//text()')):
            am_boxOffice = list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
                '//*[@id="tabcont2"]/table[2]//tr[position()>1]//text()'))))
            return am_boxOffice
        elif '北美票房' in ''.join(tree.xpath('//*[@id="tabcont2"]/h4[3]//text()')):
            am_boxOffice = list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
                '//*[@id="tabcont2"]/table[3]//tr[position()>1]//text()'))))
            return am_boxOffice
        else:
            return []

    def parse(self, response):
        EnMovieID = response.meta['EnMovieID']
        tree = etree.HTML(response.text)
        name = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
            '//div[@class="ziliaofr"]/div[@class="cont"]/h2//text()')))))
        enName = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
            '//div[@class="ziliaofr"]/div[@class="cont"]/p[1]//text()')))))
        boxOffice_total,now_boxOffice=self.get_block_office(tree)
        genre = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
            '//div[@class="ziliaofr"]/div[@class="cont"]/p[3]//text()')))))
        genre = genre[genre.find("：") + 1:].strip('')
        runTime = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
            '//div[@class="ziliaofr"]/div[@class="cont"]/p[4]//text()')))))
        runTime = runTime[runTime.find("：") + 1:].strip('')
        releaseDate = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
            '//div[@class="ziliaofr"]/div[@class="cont"]/p[5]//text()')))))
        releaseDate = releaseDate[releaseDate.find("：") + 1:].strip('')
        standard = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
            '//div[@class="ziliaofr"]/div[@class="cont"]/p[6]//text()')))))
        standard = standard[standard.find("：") + 1:].strip('')
        country = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
            '//div[@class="ziliaofr"]/div[@class="cont"]/p[7]//text()')))))
        country = country[country.find("：") + 1:].strip('')
        director = ','.join(
            list(
                filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath('//dl[@class="dltext"]/dd[1]//text()')))))
        starring = ','.join(
            list(
                filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath('//dl[@class="dltext"]/dd[2]//text()')))))
        production_co = ','.join(
            list(
                filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath('//dl[@class="dltext"]/dd[3]//text()')))))
        distribution_co = ','.join(
            list(
                filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath('//dl[@class="dltext"]/dd[4]//text()')))))
        inland_boxOffice = self.get_inland(tree)
        hk_boxOffice = self.get_hk(tree)
        am_boxOffice = self.get_am(tree)
        item = Cboocn()
        if len(inland_boxOffice) != 0:
            inland_avg, inland_week, inland_total, inland_days = self.get_office(inland_boxOffice, 0)
            item['inland_avg'] = ','.join(inland_avg)
            item['inland_week'] = ','.join(inland_week)
            item['inland_total'] = ','.join(inland_total)
            item['inland_days'] = ','.join(inland_days)
        if len(hk_boxOffice) != 0:
            hk_rank, hk_week, hk_total = self.get_office(hk_boxOffice, 1)
            item['hk_rank'] = ','.join(hk_rank)
            item['hk_week'] = ','.join(hk_week)
            item['hk_total'] = ','.join(hk_total)
        if len(am_boxOffice) != 0:
            am_rank, am_week, am_total = self.get_office(am_boxOffice, 1)
            item['am_rank'] = ','.join(am_rank)
            item['am_week'] = ','.join(am_week)
            item['am_total'] = ','.join(am_total)
        item['EnMovieID'] = EnMovieID
        item['name'] = name
        item['enName'] = enName
        item['boxOffice_total'] = boxOffice_total
        item['now_boxOffice'] = now_boxOffice
        item['genre'] = genre
        item['runTime'] = runTime
        item['releaseDate'] = releaseDate
        item['standard'] = standard
        item['country'] = country
        item['director'] = director
        item['starring'] = starring
        item['production_co'] = production_co
        item['distribution_co'] = distribution_co
        yield item
