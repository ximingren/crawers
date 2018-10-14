# -*- coding: utf-8 -*-
import datetime
import json
import logging
import multiprocessing
from multiprocessing.pool import Pool

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


# 7-3000
# 3000-6000
# 6000-10000
# 10000-11000 over

# 1000-15000
# 15000-40000
# 10000-200000好像是没数据的
# 3,4,5,600000字段完成
# 600000 放弃
# 0-300000完成
class EbotappSpider(scrapy.Spider):
    name = 'ebotapp'

    # start_urls = ['http://ebotapp/']
    def openlink(self, url, data):
        """
        urlopen error 10060错误
        :param url:  请求的网址
        :param headers: 报文头部信息
        :return: 服务器响应
        """
        maxTryNum = 15
        for tries in range(maxTryNum):
            try:
                logging.info("请求%s，%s" % (url, data))
                req = requests.post(url, data=data, timeout=13)
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
        for id in range(300000, 682000):
            page = 1
            pageSize = 30
            params = {'EnMovieID': str(id)}
            meta = {'EnMovieID': str(id), 'film_data': {}}
            yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByBaseInfo', meta=meta,
                              formdata=params, callback=self.main_parse)

    def main_parse(self, response):
        EnMovieID = response.meta['EnMovieID']
        film_data = response.meta['film_data']
        # EnMovieID = film['EnMovieID']
        # movieName = film['MovieName']
        # time.sleep(4)
        EnMovieID = str(EnMovieID)
        self.get_base(film_data, response)  # 票房汇总信息
        try:
            condition = film_data['ReleaseDate']
        except Exception as e:
            print(EnMovieID, e)
        else:
            # self.get_people(EnMovieID)  # 剧组人员
            # self.get_company(EnMovieID)  # 相关公司

            releaseDate = ''
            try:
                if film_data['ReleaseDate'] != '':
                    try:
                        if '年' in film_data['ReleaseDate'] and '月' in film_data['ReleaseDate'] and '日' in \
                                film_data['ReleaseDate']:
                            releaseDate = datetime.datetime.strptime(film_data['ReleaseDate'], "%Y年%m月%d日")
                        if '年' in film_data['ReleaseDate'] and '月' in film_data['ReleaseDate']:
                            releaseDate = datetime.datetime.strptime(film_data['ReleaseDate'], "%Y年%m月")
                        if '年' in film_data['ReleaseDate']:
                            releaseDate = datetime.datetime.strptime(film_data['ReleaseDate'], "%Y年")
                        else:
                            releaseDate = datetime.datetime.strptime(film_data['ReleaseDate'], "%Y-%m-%d")
                    except Exception as e:
                        print(e)
                    else:
                        if releaseDate < datetime.datetime.now():
                            sDate = releaseDate - datetime.timedelta(days=1)
                            eDate = releaseDate + datetime.timedelta(days=9)
                            # self.get_index(EnMovieID, sDate, eDate)  # 影响指数
                            self.get_distribute(EnMovieID, sDate, eDate, film_data['MovieID'],
                                                            film_data)  # 票房分布
                            # self.get_boxOffice(EnMovieID, sDate, eDate, film_data['MovieID'])
                            # self.get_audience(EnMovieID)  # 观众
                            # self.get_rowPrice(EnMovieID, sDate, eDate, film_data['MovieID'])  # 排片
                self.clear_data(film_data)
                item = Ebotapp()
                item['item'] = film_data
                yield item
            except Exception as e:
                print(EnMovieID, e)

    def parse(self, response):
        pageSize = 30
        # id=response.meta['companyid']
        # film_list = json.loads(response.text)  # 电影列表
        # totalCounts = int(film_list['Data']['Table2'][0]['TotalCounts'])  # 总电影数
        # if totalCounts > 0:
        #     totalPage = int(film_list['Data']['Table2'][0]['TotalPage'])  # 总页数
        #     # self.parse_main(film_list)
        #     for page in range(1, totalPage):
        #         response = self.openlink('http://ebotapp.entgroup.cn/API/Information/GetCompanyWorks',
        #                                  data={'companyid': str(id), 'pageIndex': str(page), 'pageSize': str(pageSize)})
        #         film_list = json.loads(response.text)  # 电影列表
        #         totalCounts = int(film_list['Data']['Table2'][0]['TotalCounts'])  # 总电影数
        #         for film in film_list['Data']['Table1']:

        # p=Pool(10)
        # need_id=range(300000,682000)
        # length=int(len(need_id)/10)
        # for i in range(10):
        #     EnMovieID_list=need_id[(length)*i:(length)*(i+1)]
        #     p.apply_async(self.main_parse,args={EnMovieID_list,})
        # p.close()
        # p.join()

    def get_base(self, film_data, response):
        try:
            # base_info_res = self.openlink('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByBaseInfo',
            #                               data={'EnMovieID': EnMovieID})
            base_info_1 = json.loads(response.text)['Data']['Table1'][0]

            for key, value in dict(base_info_1).items():
                film_data[key] = value
        except Exception as e:
            # self.write_txt(EnMovieID)
            print("解析基础信息时发生错误", e)

    def get_people(self, EnMovieID):
        try:
            detail_info_res = self.openlink('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByDetail',
                                            data={'EnMovieID': EnMovieID})
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
        except Exception as e:
            self.write_txt(EnMovieID)
            print("解析人员时发生错误", e)

    def get_company(self, EnMovieID):
        try:
            relate_company_info_res = self.openlink('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByDetail',
                                                    data={'EnMovieID': EnMovieID})
            try:
                relate_company_info = relate_company_info_res.json()
            except Exception as e:
                print(e)
            else:
                relate_company = relate_company_info['Data']['Table2']
                print(relate_company)
                relate_company_dict = {}
                for company in relate_company:
                    CompanyName = company['CompanyName']
                    CompanyType = company['CompanyType']
                    CountryName = company['CountryName']
                    if not CompanyType in relate_company_dict.keys():
                        relate_company_dict[CompanyType] = []
                    relate_company_dict[CompanyType].append(CountryName + CompanyName)
                film_data.update(relate_company_dict)
        except Exception as e:
            self.write_txt(EnMovieID)
            print("解析相关公司时发生错误", e)

    def get_audience(self, EnMovieID):
        try:
            audience_info_res = self.openlink('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByAudience',
                                              data={'EnMovieID': EnMovieID})
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
        except Exception as e:
            self.write_txt(EnMovieID)
            print("解析观众分布时发生错误", e)

    def get_index(self, EnMovieID, sDate, eDate):
        try:
            effect_index_res = self.openlink('http://ebotapp.entgroup.cn/API/DataBox/Movie/MarketingData_EffectIndex',
                                             data={'EnMovieID': EnMovieID, 'sDate': sDate, 'eDate': eDate})
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
        except Exception as e:
            self.write_txt(EnMovieID)
            print("解析指数时发生错误", e)

    def get_distribute(self, EnMovieID, sDate, eDate, MovieID, film_data):
        try:
            distribute_res = self.openlink('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByTimeIntervalTOP',
                                           data={'EnMovieID': EnMovieID, 'sDate': sDate, 'eDate': eDate,
                                                 'MovieID': MovieID, 'ServicePrice': 1})
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
                            distribute_data['Table3'][0]['CompanyName'] + ":" + str(
                                distribute_data['Table3'][0]['BoxOffice']))
                        distribute_data_list.append(
                            distribute_data['Table4'][0]['CityName'] + ":" + str(
                                distribute_data['Table4'][0]['BoxOffice']))
                        distribute_data_list.append('二线城市' + ":" + str(distribute_data['Table6'][0]['BoxOffice']))
                        film_data['票房分布-包服务费'] = distribute_data_list
                    else:
                        film_data['票房分布-包服务费'] = None
        except Exception as e:
            self.write_txt(EnMovieID)
            print("解析票房分布时发生错误", e)

    def write_txt(self, id):
        with open('error.txt', 'a') as f:
            f.write(str(id) + '\n')

    def get_boxOffice(self, EnMovieID, sDate, eDate, MovieID, Index='102,201,202,203,205,221,222,251,801,604,606',
                      ServicePrice=1):
        try:
            boxOffice_info_res = self.openlink(
                'http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByTimeIntervalList',
                data={'EnMovieID': EnMovieID, 'MovieID': MovieID, 'sDate': sDate,
                      'eDate': eDate,
                      'Index': Index, 'ServicePrice': ServicePrice})
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
                        film_data['boxOffice_audienceCount'].append(
                            box['InsertDate'] + ":" + str(box['AudienceCount']))  # 人次
                        film_data['OfferSeat'].append(box['InsertDate'] + ":" + str(box['OfferSeat']))  # 排座
                        film_data['AvgBoxOffice'].append(box['InsertDate'] + ":" + str(box['AvgBoxOffice']))  # 平均票价
                        film_data['AvgShowPeople'].append(box['InsertDate'] + ":" + str(box['AvgShowPeople']))  # 场均人次
                        film_data['Attendance'].append(box['InsertDate'] + ":" + str(box['Attendance']))  # 上座率
                        film_data['ServicePrice'].append(box['InsertDate'] + ":" + str(box['ServicePrice']))  # 服务费
        except Exception as e:
            self.write_txt(EnMovieID)
            print("解析票房具体信息时发生错误", e)

    def get_rowPrice(self, EnMovieID, sDate, eDate, MovieID, Index='102,201,202,203,205,221,222,251,801,604,606',
                     ServicePrice=1):
        try:
            rowPrice_res = self.openlink('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByRowPiece',
                                         data={'EnMovieID': EnMovieID, 'MovieID': MovieID, 'sDate': sDate,
                                               'eDate': eDate,
                                               'Index': Index, 'ServicePrice': ServicePrice})
            try:
                rowPrice = rowPrice_res.json()
            except Exception as e:
                print(e)
            else:
                rowPrice_data = rowPrice['Data']['Table1']
                film_data['ShowCount_list'] = []  # 排片场次
                film_data['HjShowCount_list'] = []  # 黄金场次
                film_data['swShowCount_list'] = []  # 上午场次
                film_data['xwShowCount_list'] = []  # 上午场次
                film_data['JyShowCount_list'] = []  # 上午场次
                film_data['ShowCountPercent_list'] = []  # 排片占比
                film_data['OfferSeatPercent_list'] = []  # 排座占比
                for row in rowPrice_data:
                    film_data['ShowCount_list'].append(row['InsertDate'] + ":" + str(row['ShowCount']))
                    film_data['HjShowCount_list'].append(row['InsertDate'] + ":" + str(row['HjShowCount']))
                    film_data['HjShowCount_list'].append(row['InsertDate'] + ":" + str(row['HjShowCount']))
                    film_data['xwShowCount_list'].append(row['InsertDate'] + ":" + str(row['xwShowCount']))
                    film_data['swShowCount_list'].append(row['InsertDate'] + ":" + str(row['swShowCount']))
                    film_data['JyShowCount_list'].append(row['InsertDate'] + ":" + str(row['JyShowCount']))
                    film_data['ShowCountPercent_list'].append(row['InsertDate'] + ":" + str(row['ShowCountPercent']))
                    film_data['OfferSeatPercent_list'].append(row['InsertDate'] + ":" + str(row['OfferSeatPercent']))
        except Exception as e:
            self.write_txt(EnMovieID)
            print("解析排片时发生错误", e)

    def clear_data(self,film_data):
        for key, value in film_data.items():
            if isinstance(value, list):
                if len(value) == 0:
                    film_data[key] = None
                else:
                    film_data[key] = ','.join(film_data[key])
