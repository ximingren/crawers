# -*- coding: utf-8 -*-
import datetime
import json
import scrapy
from scrapy import FormRequest
from common_crawer.items import Ebotapp


class EbotappSpider(scrapy.Spider):
    name = 'ebotapp'

    def start_requests(self):
        """
        开始请求，以公司id为起始点.循环迭代
        :return:
        """
        for id in range(660000, 660001):
            params = {'EnMovieID': str(id)}
            meta = {'EnMovieID': str(id), 'film_data': {}}
            yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByBaseInfo', meta=meta,
                              formdata=params, callback=self.main_parse)

    def main_parse(self, response):
        """
        解析主函数
        :param response:
        :return:
        """
        EnMovieID = response.meta['EnMovieID']
        film_data = response.meta['film_data']
        self.get_base(film_data, response)  # 票房汇总信息
        meta = {'EnMovieID': EnMovieID, 'film_data': film_data}
        yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByDetail',
                              meta=meta, formdata={'EnMovieID': EnMovieID}, callback=self.get_people) #爬取演员

    def get_base(self, film_data, response):
        """
        解析电影的基础信息
        :param film_data:
        :param response:
        :return:
        """
        try:
            base_info_1 = json.loads(response.text)['Data']['Table1'][0]
            for key, value in dict(base_info_1).items():
                film_data[key] = value
        except Exception as e:
            print("解析基础信息时发生错误", e)

    def get_people(self, response):
        """
        解析得到演员
        :param EnMovieID:
        :param film_data:
        :return:
        """
        film_data = response.meta['film_data']
        EnMovieID = response.meta['EnMovieID']
        try:

            try:
                detail_info = json.loads(response.text)
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
            print("解析人员时发生错误", e)
        finally:
            meta = {'EnMovieID': EnMovieID, 'film_data': film_data}
            yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByDetail',dont_filter=True,
                              meta=meta, formdata={'EnMovieID': EnMovieID}, callback=self.get_company)  # 相关公司

    def get_company(self, response):
        try:
            film_data = response.meta['film_data']
            EnMovieID = response.meta['EnMovieID']
            try:
                relate_company_info = json.loads(response.text)
            except Exception as e:
                print(e)
            else:
                relate_company = relate_company_info['Data']['Table2']
                relate_company_dict = {}
                for company in relate_company:
                    CompanyName = company['CompanyName']
                    CompanyType = company['CompanyType']
                    CountryName = company['CountryName']
                    if not CompanyType in relate_company_dict.keys():
                        relate_company_dict[CompanyType] = []
                    relate_company_dict[CompanyType].append(CountryName + CompanyName)
                film_data.update(relate_company_dict)
            finally:
                try:
                    if film_data['ReleaseDate'] != '':
                        releaseDate = self.get_date(film_data)
                        if releaseDate < datetime.datetime.now():
                            sDate = releaseDate - datetime.timedelta(days=1)
                            eDate = releaseDate + datetime.timedelta(days=9)
                            meta = {'EnMovieID': EnMovieID, 'film_data': film_data, 'sDate': sDate, 'eDate': eDate}
                            yield FormRequest(
                                'http://ebotapp.entgroup.cn/API/DataBox/Movie/MarketingData_EffectIndex',
                                formdata={'EnMovieID': EnMovieID, 'sDate': sDate, 'eDate': eDate}, meta=meta,
                                callback=self.get_index)  # 影响指数
                except Exception as e:
                    print(EnMovieID, e)
        except Exception as e:
            print("解析相关公司时发生错误", e)

    def get_date(self, film_data):
        try:
            if '年' in film_data['ReleaseDate'] and '月' in film_data['ReleaseDate'] and '日' in \
                    film_data['ReleaseDate']:
                releaseDate = datetime.datetime.strptime(film_data['ReleaseDate'], "%Y年%m月%d日")
            elif '年' in film_data['ReleaseDate'] and '月' in film_data['ReleaseDate']:
                releaseDate = datetime.datetime.strptime(film_data['ReleaseDate'], "%Y年%m月")
            elif '年' in film_data['ReleaseDate']:
                releaseDate = datetime.datetime.strptime(film_data['ReleaseDate'], "%Y年")
            else:
                releaseDate = datetime.datetime.strptime(film_data['ReleaseDate'], "%Y-%m-%d")
            return releaseDate
        except Exception as e:
            print(e)

    def get_audience(self, response):
        film_data = response.meta['film_data']
        EnMovieID = response.meta['EnMovieID']
        sDate = response.meta['sDate']
        eDate = response.meta['eDate']
        try:
            try:
                audience_info = json.loads(response.text)
            except Exception as e:
                print(e)
            else:
                gender_info = audience_info['Data']['Table1'][0]  # 性别分布
                ManNumTGI = gender_info['ManNumTGI']
                WoManNumTGI = gender_info['WoManNumTGI']
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
            print("解析观众分布时发生错误", e)
        finally:
            meta = {'EnMovieID': EnMovieID, 'film_data': film_data, 'sDate': sDate, 'eDate': eDate}
            yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByRowPiece',
                              formdata={'EnMovieID': EnMovieID, 'MovieID': film_data['MovieID'],
                                        'sDate': sDate,
                                        'eDate': eDate,
                                        'Index': '102,201,202,203,205,221,222,251,801,604,606',
                                        'ServicePrice': 1}, meta=meta,
                              callback=self.get_rowPrice)  # 排片
            self.clear_data(film_data)

    def get_index(self, response):
        film_data = response.meta['film_data']
        EnMovieID = response.meta['EnMovieID']
        sDate = response.meta['sDate']
        eDate = response.meta['eDate']
        try:
            try:
                effect_index = json.loads(response.text)
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
            print("解析指数时发生错误", e)
        finally:
            meta = {'EnMovieID': EnMovieID, 'film_data': film_data, 'sDate': sDate, 'eDate': eDate}
            yield FormRequest(
                'http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByTimeIntervalTOP',
                formdata={'EnMovieID': EnMovieID, 'sDate': sDate, 'eDate': eDate,
                          'MovieID': film_data['MovieID'], 'ServicePrice': 1}, meta=meta,
                callback=self.get_distribute)  # 票房分布

    def get_distribute(self, response):
        film_data = response.meta['film_data']
        EnMovieID = response.meta['EnMovieID']
        sDate = response.meta['sDate']
        eDate = response.meta['eDate']
        try:
            try:
                distribute = json.loads(response.text)
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
            print("解析票房分布时发生错误", e)
        finally:
            meta = {'EnMovieID': EnMovieID, 'film_data': film_data, 'sDate': sDate, 'eDate': eDate}
            yield FormRequest(
                'http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByTimeIntervalList',
                formdata={'EnMovieID': EnMovieID, 'MovieID': film_data['MovieID'], 'sDate': sDate,
                          'eDate': eDate,
                          'Index': '102,201,202,203,205,221,222,251,801,604,606',
                          'ServicePrice': 1},
                meta=meta, callback=self.get_boxOffice)

    def get_boxOffice(self, response):
        film_data = response.meta['film_data']
        EnMovieID = response.meta['EnMovieID']
        sDate = response.meta['sDate']
        eDate = response.meta['eDate']
        try:
            try:
                boxOffice_info = json.loads(response.text)
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
            print("解析票房具体信息时发生错误", e)
        finally:
            meta = {'EnMovieID': EnMovieID, 'film_data': film_data, 'sDate': sDate, 'eDate': eDate}
            yield FormRequest('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByAudience',
                              formdata={'EnMovieID': EnMovieID}, meta=meta,
                              callback=self.get_audience)  # 观众

    def get_rowPrice(self, response):
        try:
            film_data = response.meta['film_data']
            try:
                rowPrice = json.loads(response.text)
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
            finally:
                pass
        except Exception as e:
            print("解析排片时发生错误", e)
        finally:
            item = Ebotapp()
            film_data = self.clear_data(film_data)
            item['item'] = film_data
            yield item

    def clear_data(self, film_data):
        for key, value in film_data.items():
            if isinstance(value, list):
                if len(value) == 0:
                    film_data[key] = None
                else:
                    film_data[key] = ','.join(film_data[key])
