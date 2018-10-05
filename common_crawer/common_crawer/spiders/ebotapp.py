# -*- coding: utf-8 -*-
import datetime
import json
import logging

import requests
import scrapy
from scrapy import Request, FormRequest

# BoxOfficePoint：点映票房
# BoxOfficeToTal：累积票房
# BoxOfficeWeekEnd:首周末票房
# BoxOfficeFirstWeek：首周日票房
# BoxOfficeFirstDay:首映日票房
# ReleaseDate:上映时间
from common_crawer.items import Ebotapp
from scrapy.utils.log import logger


class EbotappSpider(scrapy.Spider):
    name = 'ebotapp'

    # start_urls = ['http://ebotapp/']
    def openlink(self,url,data):
        """
        urlopen error 10060错误
        :param url:  请求的网址
        :param headers: 报文头部信息
        :return: 服务器响应
        """
        maxTryNum = 15
        for tries in range(maxTryNum):
            try:
                logging.info("请求%s，%s"%(url,data))
                req = requests.post(url,data=data,timeout=13)
                return req
            except:
                if tries < (maxTryNum - 1):
                    continue
                else:
                    logger.info("尝试%d 次连接网址%s失败!" % (maxTryNum, url))

    def start_requests(self):
        """
        开始请求，以公司id为起始点.循环迭代
        :return:
        """
        for id in range(6,7):
            page = 1
            pageSize = 30
            params = {'companyid': str(id), 'pageIndex': str(page),
                      'pageSize': str(pageSize)}
            yield FormRequest('http://ebotapp.entgroup.cn/API/Information/GetCompanyWorks', method='POST',dont_filter=True,
                              formdata=params, meta=params, callback=self.get_film_index)

    def get_company_index(self, response):
        companyid = 6
        company_info = json.loads(response.text)  # 公司信息
        company_name = company_info['Data']['Table1'][0]['CompanyName']  # 公司名称
        LongCompanyName = company_info['Data']['Table1'][0]['LongCompanyName']  # 公司长名称
        CompanyType = company_info['Data']['Table1'][0]['CompanyType']  # 公司类型
        #  获取该公司下的所有电影
        yield FormRequest('http://ebotapp.entgroup.cn/API/Information/GetCompanyWorks', method='POST',dont_filter=True,
                          formdata={'companyid': str(companyid), 'pageIndex': str(pageIndex),
                                    'pageSize': str(pageSize)}, meta={'companyid': companyid},
                          callback=self.get_film_list)

    def get_film_index(self, response):
        """
        解析结果，查出该公司下有多少个电影.接着迭代请求，把该公司的所有电影数据爬取
        :param response:
        :return:
        """
        companyid = response.meta['companyid']
        pageSize = 30
        film_list = json.loads(response.text)  # 电影列表
        totalCounts = int(film_list['Data']['Table2'][0]['TotalCounts'])  # 总电影数
        if totalCounts > 0:
            totalPage = int(film_list['Data']['Table2'][0]['TotalPage'])  # 总页数
            # self.parse_main(film_list)
            for page in range(1, totalPage):
                yield FormRequest('http://ebotapp.entgroup.cn/API/Information/GetCompanyWorks', method='POST',dont_filter=True,
                                  formdata={'companyid': str(companyid), 'pageIndex': str(page),
                                            'pageSize': str(pageSize)}, meta={'totalPage': totalPage},
                                  callback=self.get_film_list)

    def get_film_list(self, response):
        """
        解析电影列表数据
        :param response:
        :return:
        """
        film_list = json.loads(response.text)  # 电影列表
        totalCounts = int(film_list['Data']['Table2'][0]['TotalCounts'])  # 总电影数
        for film in film_list['Data']['Table1']:
            self.film_data = {}
            EnMovieID = film['EnMovieID']
            movieName = film['MovieName']
            yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByBaseInfo',
                              formdata={'EnMovieID': EnMovieID},meta={'film_data':{},'EnMovieID': EnMovieID},callback=self.get_base)


    def get_base(self, response):
        try:
            film_data=response.meta['film_data']
            enMovieID=response.meta['EnMovieID']
            base_info_res = response
            base_info_1 = base_info_res.json()['Data']['Table1'][0]
            for key, value in dict(base_info_1).items():
                film_data[key] = value
            yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByDetail',
                                            formdata={'EnMovieID': enMovieID},meta={'film_data':film_data,'EnMovieID':enMovieID},callback=self.get_people)
        except Exception as e:
            self.write_txt(response.meta['EnMovieID'])
            print("解析基础信息时发生错误",e)
    def get_people(self, response):
        try:
            detail_info_res = response
            film_data = response.meta['film_data']
            try:
                detail_info = detail_info_res.json()
            except Exception as e:
                print(e)
            else:
                people_list = detail_info['Data']['Table3']
                people_dict = {}
                for people in people_list:
                    PersonType = people['PersonType']
                    if not PersonType in people_dict.keys():
                        people_dict[PersonType] = []
                    name = people['PersonnelName']
                    people_dict[PersonType].append(name)
                film_data.update(people_dict)
            yield  FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByDetail',
                                            formdata={'EnMovieID': response.meta['EnMovieID']},
                               meta={'film_data':film_data,'EnMovieID':response.meta['EnMovieID']},callback=self.get_company)
        except Exception as e:
            self.write_txt(response.meta['EnMovieID'])
            print("解析人员时发生错误",e)
    def get_company(self, response):
        try:
            relate_company_info_res =response
            film_data = response.meta['film_data']
            try:
                relate_company_info = relate_company_info_res.json()
            except Exception as e:
                print(e)
            else:
                relate_company = relate_company_info['Data']['Table2']
                relate_company_dict = {}
                for company in relate_company:
                    CompanyName = company['CompanyName']
                    CompanyType = company['CompanyType']
                    CountryName = company['CountryName']
                    if not CountryName + CompanyName in relate_company_dict.keys():
                        relate_company_dict[CompanyType] = []
                    relate_company_dict[CompanyType].append(CountryName + CompanyName)
                film_data.update(relate_company_dict)
            if self.film_data['ReleaseDate'] != '':
                if '年' in self.film_data['ReleaseDate'] and '月' in self.film_data['ReleaseDate'] and '日' in \
                        self.film_data['ReleaseDate']:
                    releaseDate = datetime.datetime.strptime(self.film_data['ReleaseDate'], "%Y年%m月%d日")
                if '年' in self.film_data['ReleaseDate'] and '月' in self.film_data['ReleaseDate']:
                    releaseDate = datetime.datetime.strptime(self.film_data['ReleaseDate'], "%Y年%m月")
                if '年' in self.film_data['ReleaseDate']:
                    releaseDate = datetime.datetime.strptime(self.film_data['ReleaseDate'], "%Y年")
                else:
                    releaseDate = datetime.datetime.strptime(self.film_data['ReleaseDate'], "%Y-%m-%d")
                if releaseDate < datetime.datetime.now():
                    sDate = releaseDate - datetime.timedelta(days=1)
                    eDate = releaseDate + datetime.timedelta(days=10)
                    yield  FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MarketingData_EffectIndex',
                                             formdata={'EnMovieID': response.meta['EnMovieID'], 'sDate': sDate, 'eDate': eDate},
                                       meta={'film_data':film_data,'EnMovieID':response.meta['EnMovieID'],'sDate':sDate,'eDate':eDate},callback=self.get_index
                                       )
                else:
                    film_data=self.clear_data(film_data)
                    item = Ebotapp()
                    item['item'] = film_data
                    yield item
        except Exception as e:
            self.write_txt(response.meta['EnMovieID'])
            print("解析相关公司时发生错误",e)
    def get_audience(self, response):
        try:
            film_data = response.meta['film_data']
            audience_info_res = response
            try:
                audience_info = audience_info_res.json()
            except Exception as e:
                print(e)
            else:
                gender_info = audience_info['Data']['Table1'][0]  # 性别分布
                ManNumTGI = gender_info['ManNumTGI']
                WoManNumTGI = gender_info['WoManNumTGI']
                distribute_dict = {}
                film_data['年龄分布'] = []
                film_data['地域分布'] = []
                film_data['性别分布'] = ['ManNumTGI' + ":" + str(ManNumTGI), "WoManNumTGI" + ":" + str(WoManNumTGI)]
                age_info = audience_info['Data']['Table2']  # 年龄分布
                for age in age_info:
                    film_data['地域分布'].append(age['AgeName'] + ":" + str(age['Num']))
                area_info = audience_info['Data']['Table3']  # 受众分布
                for area in area_info:
                    film_data['地域分布'].append(area['ProvinceName'] + ":" + str(area['Num']))
            yield  FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByRowPiece',
                                         formdata={'EnMovieID': response.meta['EnMovieID'], 'MovieID': response.meta['MovieID'], 'sDate': response.meta['sDate'], 'eDate': response.meta['eDate'],
                                               'Index': '102,201,202,203,205,221,222,251,801,604,606', 'ServicePrice': 1}, meta={'film_data': film_data, 'EnMovieID': response.meta['EnMovieID'], 'sDate':  response.meta['sDate'],
                                    'eDate':  response.meta['eDate']},callback=self.get_rowPrice)
        except Exception as e:
            self.write_txt(response.meta['EnMovieID'])
            print("解析观众分布时发生错误",e)
    def get_index(self,response):
        try:
            film_data=response.meta['film_data']
            effect_index_res =response
            try:
                effect_index = effect_index_res.json()
            except Exception as e:
                print(e)
            else:
                index = effect_index['Data']['Table1']
                buyIndex_list = []
                rapIndex_list = []
                renIndex_list = []
                for x in index:
                    buyIndex_list.append(str(x['InsertDate']) + ':' + str(x['BuyTicketIndex']))
                    rapIndex_list.append(str(x['InsertDate']) + ':' + str(x['RapIndex']))
                    renIndex_list.append(str(x['InsertDate']) + ':' + str(x['RenZhiIndex']))
                film_data['BuyTicketIndex'] = buyIndex_list  # 购票指数
                film_data['RapIndex'] = rapIndex_list  # 口碑指数
                film_data['RenZhiIndex'] = renIndex_list  # 认知指数
            yield  FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByTimeIntervalTOP',
                                           formdata={'EnMovieID': response.meta['EnMovieID'], 'sDate': response.meta['sDate'], 'eDate': response.meta['eDate'],
                                                 'MovieID': film_data['EnMovieID']}, meta={'film_data':film_data,'EnMovieID':response.meta['EnMovieID'],'sDate':response.meta['sDate'],'eDate':response.meta['eDate']},
                               callback=self.get_distribute)
        except Exception as e:
            self.write_txt(response.meta['EnMovieID'])
            print("解析指数时发生错误", e)

    def get_distribute(self, response):
        try:
            film_data = response.meta['film_data']
            distribute_res = response
            try:
                distribute = distribute_res.json()
            except Exception as e:
                print(e)
            else:
                distribute_data = distribute['Data']
                distribute_data_list = []
                if 'Table2' in distribute_data:
                    if distribute_data['Table2'] != []:
                        distribute_data_list.append(
                            distribute_data['Table2'][0]['CinemaLineName'] + ":" + str(
                                distribute_data['Table2'][0]['BoxOffice']))
                        distribute_data_list.append(
                            distribute_data['Table3'][0]['CompanyName'] + ":" + str(distribute_data['Table3'][0]['BoxOffice']))
                        distribute_data_list.append(
                            distribute_data['Table4'][0]['CityName'] + ":" + str(distribute_data['Table4'][0]['BoxOffice']))
                        distribute_data_list.append('二线城市' + ":" + str(distribute_data['Table6'][0]['BoxOffice']))
                        film_data['票房分布'] = distribute_data_list
                    else:
                        film_data['票房分布'] = None
            yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByTimeIntervalList',
                                               formdata={'EnMovieID': response.meta['EnMovieID'], 'MovieID': response.meta['MovieID'], 'sDate': response.meta['sDate'],
                                                     'eDate': response.meta['eDate'],
                                                     'Index': '102,201,202,203,205,221,222,251,801,604,606', 'ServicePrice': 1},
                              meta={'film_data': film_data, 'EnMovieID': response.meta['EnMovieID'], 'sDate':  response.meta['sDate'],
                                    'eDate':  response.meta['eDate']},callback=self.get_boxOffice)
        except Exception as e:
            self.write_txt(response.meta['EnMovieID'])
            print("解析票房分布时发生错误", e)

    def write_txt(self,id):
        with open('error.txt','a') as f:
            f.write(str(id)+'\n')
    def get_boxOffice(self, response):
        try:
            film_data = response.meta['film_data']
            boxOffice_info_res = response
            try:
                boxOffice_info = boxOffice_info_res.json()
            except Exception as e:
                print(e)
            else:
                if 'Table2' in boxOffice_info['Data']:
                    boxOffice_day_info = boxOffice_info['Data']['Table2']
                    film_data['boxOffice_total'] = []
                    film_data['boxOffice_count'] = []
                    film_data['boxOffice_audienceCount'] = []
                    film_data['OfferSeat'] = []
                    film_data['AvgBoxOffice'] = []
                    film_data['AvgShowPeople'] = []
                    film_data['Attendance'] = []
                    film_data['ServicePrice'] = []
                    for box in boxOffice_day_info:
                        film_data['boxOffice_total'].append(box['InsertDate'] + ":" + str(box['BoxOffice']))  # 总票房
                        film_data['boxOffice_count'].append(box['InsertDate'] + ":" + str(box['ShowCount']))  # 场次
                        film_data['boxOffice_audienceCount'].append(box['InsertDate'] + ":" + str(box['AudienceCount']))  # 人次
                        film_data['OfferSeat'].append(box['InsertDate'] + ":" + str(box['OfferSeat']))  # 排座
                        film_data['AvgBoxOffice'].append(box['InsertDate'] + ":" + str(box['AvgBoxOffice']))  # 平均票价
                        film_data['AvgShowPeople'].append(box['InsertDate'] + ":" + str(box['AvgShowPeople']))  # 场均人次
                        film_data['Attendance'].append(box['InsertDate'] + ":" + str(box['Attendance']))  # 上座率
                        film_data['ServicePrice'].append(box['InsertDate'] + ":" + str(box['ServicePrice']))  # 服务费
            yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByAudience',
                                              formdata={'EnMovieID': response.meta['EnMovieID']}, meta={'film_data': film_data, 'EnMovieID': response.meta['EnMovieID'], 'sDate':  response.meta['sDate'],
                                    'eDate':  response.meta['eDate']},callback=self.get_audience)
        except Exception as e:
            self.write_txt(response.meta['EnMovieID'])
            print("解析票房具体信息时发生错误",e)

    def get_rowPrice(self, response):
        try:
            film_data=response.meta['film_data']
            rowPrice_res =response
            try:
                rowPrice = rowPrice_res.json()
            except Exception as e:
                print(e)
            else:
                rowPrice_data = rowPrice['Data']['Table1']
                self.film_data['ShowCount_list'] = []  # 排片场次
                self.film_data['HjShowCount_list'] = []  # 黄金场次
                self.film_data['swShowCount_list'] = []  # 上午场次
                self.film_data['xwShowCount_list'] = []  # 上午场次
                self.film_data['JyShowCount_list'] = []  # 上午场次
                self.film_data['ShowCountPercent_list'] = []  # 排片占比
                self.film_data['OfferSeatPercent_list'] = []  # 排座占比
                for row in rowPrice_data:
                    self.film_data['ShowCount_list'].append(row['InsertDate'] + ":" + str(row['ShowCount']))
                    self.film_data['HjShowCount_list'].append(row['InsertDate'] + ":" + str(row['HjShowCount']))
                    self.film_data['HjShowCount_list'].append(row['InsertDate'] + ":" + str(row['HjShowCount']))
                    self.film_data['xwShowCount_list'].append(row['InsertDate'] + ":" + str(row['xwShowCount']))
                    self.film_data['swShowCount_list'].append(row['InsertDate'] + ":" + str(row['swShowCount']))
                    self.film_data['JyShowCount_list'].append(row['InsertDate'] + ":" + str(row['JyShowCount']))
                    self.film_data['ShowCountPercent_list'].append(row['InsertDate'] + ":" + str(row['ShowCountPercent']))
                    self.film_data['OfferSeatPercent_list'].append(row['InsertDate'] + ":" + str(row['OfferSeatPercent']))
            film_data = self.clear_data(film_data)
            item = Ebotapp()
            item['item'] = film_data
            yield item
        except Exception as e:
            self.write_txt(response.meta['EnMovieID'])
            print("解析排片时发生错误",e)
    def clear_data(self,film_data):
        for key, value in film_data.items():
            if isinstance(value, list):
                if len(value) == 0:
                    film_data[key] = None
                else:
                    film_data[key] = ','.join(self.film_data[key])
        return film_data