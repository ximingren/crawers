import datetime

import requests


# BoxOfficePoint：点映票房
# BoxOfficeToTal：累积票房
# BoxOfficeWeekEnd:首周末票房
# BoxOfficeFirstWeek：首周日票房
# BoxOfficeFirstDay:首映日票房
# ReleaseDate:上映时间

def get_people(EnMovieID):
    detail_info_res = requests.post('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByDetail',
                                    data={'EnMovieID': EnMovieID})
    detail_info = detail_info_res.json()
    people_list = detail_info['Data']['Table3']
    people_dict = {}
    for people in people_list:
        PersonType = people['PersonType']
        if not PersonType in people_dict.keys():
            people_dict[PersonType] = []
        name = people['PersonnelName']
        people_dict[PersonType].append(name)
    data.update(people_dict)


def get_base(EnMovieID):
    base_info_res = requests.post('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByBaseInfo',
                                  data={'EnMovieID': EnMovieID})
    base_info_1 = base_info_res.json()['Data']['Table1'][0]
    for key, value in dict(base_info_1).items():
        data[key] = value


def get_company(EnMovieID):
    relate_company_info_res = requests.post('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByDetail',
                                            data={'EnMovieID': EnMovieID})
    relate_company_info = relate_company_info_res.json()
    relate_company = relate_company_info['Data']['Table2']
    relate_company_dict={}
    for company in relate_company:
        CompanyName = company['CompanyName']
        CompanyType = company['CompanyType']
        CountryName = company['CountryName']
        if not CountryName + CompanyName in relate_company_dict.keys():
            relate_company_dict[CompanyType] =[]
        relate_company_dict[CompanyType].append(CountryName + CompanyName)
    data.update(relate_company_dict)

def get_audience(EnMovieID):
    audience_info_res = requests.post('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByAudience',
                                      data={'EnMovieID': EnMovieID})
    audience_info = audience_info_res.json()
    gender_info = audience_info['Data']['Table1'][0]  # 性别分布
    ManNumTGI = gender_info['ManNumTGI']
    WoManNumTGI = gender_info['WoManNumTGI']

    distribute_dict={}
    data['年龄分布']=[]
    data['地域分布']=[]
    data['性别分布']=['ManNumTGI'+":"+str(ManNumTGI),"WoManNumTGI"+":"+str(WoManNumTGI)]
    age_info = audience_info['Data']['Table2']  # 年龄分布
    for age in age_info:
        data['地域分布'].append(age['AgeName']+":"+str(age['Num']))
    area_info = audience_info['Data']['Table3']  # 受众分布
    for area in area_info:
        data['地域分布'].append(area['ProvinceName'] + ":" + str(area['Num']))


def get_index(EnMovieID, sDate, eDate):
    effect_index_res = requests.post('http://ebotapp.entgroup.cn/API/DataBox/Movie/MarketingData_EffectIndex',
                                     data={'EnMovieID': EnMovieID, 'sDate': sDate, 'eDate': eDate})
    effect_index = effect_index_res.json()
    index = effect_index['Data']['Table1']
    buyIndex_list = []
    rapIndex_list = []
    renIndex_list = []
    for x in index:
        buyIndex_list.append(str(x['InsertDate']) + ':' +str( x['BuyTicketIndex']))
        rapIndex_list.append(str(x['InsertDate']) + ':' + str(x['RapIndex']))
        renIndex_list.append(str(x['InsertDate']) + ':' + str(x['RenZhiIndex']))
    data['BuyTicketIndex'] = buyIndex_list  # 购票指数
    data['RapIndex'] = rapIndex_list  # 口碑指数
    data['RenZhiIndex'] = renIndex_list  # 认知指数


def get_distribute(EnMovieID, sDate, eDate, MovieID):
    distribute_res = requests.post('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByTimeIntervalTOP',
                                   data={'EnMovieID': EnMovieID, 'sDate': sDate, 'eDate': eDate, 'MovieID': MovieID})
    print({'EnMovieID': EnMovieID, 'sDate': sDate, 'eDate': eDate, 'MovieID': MovieID})
    distribute = distribute_res.json()
    distribute_data = distribute['Data']
    distribute_data_list = []
    if distribute_data['Table2']!=[]:
        distribute_data_list.append(distribute_data['Table2'][0]['CinemaLineName'] + ":" + str(distribute_data['Table2'][0]['BoxOffice']))
        distribute_data_list.append(distribute_data['Table3'][0]['CompanyName'] + ":" + str(distribute_data['Table3'][0]['BoxOffice']))
        distribute_data_list.append(distribute_data['Table4'][0]['CityName'] + ":" + str(distribute_data['Table4'][0]['BoxOffice']))
        distribute_data_list.append('二线城市' + ":" + str(distribute_data['Table6'][0]['BoxOffice']))
        data['票房分布'] = distribute_data_list
    else:
        data['票房分布']=None

def get_boxOffice(EnMovieID, sDate, eDate, MovieID, Index='102,201,202,203,205,221,222,251,801,604,606',
                  ServicePrice=1):
    boxOffice_info_res = requests.post('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByTimeIntervalList',
                                       data={'EnMovieID': EnMovieID, 'MovieID': MovieID, 'sDate': sDate, 'eDate': eDate,
                                             'Index': Index, 'ServicePrice': ServicePrice})
    boxOffice_info = boxOffice_info_res.json()
    boxOffice_day_info = boxOffice_info['Data']['Table2']
    data['boxOffice_total'] = []
    data['boxOffice_count'] = []
    data['boxOffice_audienceCount'] = []
    data['OfferSeat'] = []
    data['AvgBoxOffice'] = []
    data['AvgShowPeople'] = []
    data['Attendance'] = []
    data['ServicePrice'] = []
    for box in boxOffice_day_info:
        data['boxOffice_total'].append(box['InsertDate'] + ":" + str(box['BoxOffice']))  # 总票房
        data['boxOffice_count'].append(box['InsertDate'] + ":" + str(box['ShowCount']))  # 场次
        data['boxOffice_audienceCount'].append(box['InsertDate'] + ":" + str(box['AudienceCount']))  # 人次
        data['OfferSeat'].append(box['InsertDate'] + ":" + str(box['OfferSeat']))  # 排座
        data['AvgBoxOffice'].append(box['InsertDate'] + ":" + str(box['AvgBoxOffice']))  # 平均票价
        data['AvgShowPeople'].append(box['InsertDate'] + ":" + str(box['AvgShowPeople']))  # 场均人次
        data['Attendance'].append(box['InsertDate'] + ":" + str(box['Attendance']))  # 上座率
        data['ServicePrice'].append(box['InsertDate'] + ":" + str(box['ServicePrice']))  # 服务费


def get_rowPrice(EnMovieID,sDate, eDate, MovieID, Index='102,201,202,203,205,221,222,251,801,604,606',
                  ServicePrice=1):
    rowPrice_res=requests.post('http://ebotapp.entgroup.cn/API/DataBox/Movie/MovieDataByRowPiece' ,data={'EnMovieID': EnMovieID, 'MovieID': MovieID, 'sDate': sDate, 'eDate': eDate,
                                             'Index': Index, 'ServicePrice': ServicePrice})
    rowPrice=rowPrice_res.json()
    rowPrice_data=rowPrice["Data"]['Table1']
    data['ShowCount_list']=[] #排片场次
    data['HjShowCount_list']=[] #黄金场次
    data['swShowCount_list']=[] #上午场次
    data['xwShowCount_list']=[] #上午场次
    data['JyShowCount_list']=[] #上午场次
    data['ShowCountPercent_list']=[] # 排片占比
    data['OfferSeatPercent_list']=[] # 排座占比
    for row in rowPrice_data:
        data['ShowCount_list'].append(row['InsertDate']+":"+str(row['ShowCount']))
        data['HjShowCount_list'].append(row['InsertDate']+":"+str(row['HjShowCount']))
        data['HjShowCount_list'].append(row['InsertDate']+":"+str(row['HjShowCount']))
        data['xwShowCount_list'].append(row['InsertDate']+":"+str(row['xwShowCount']))
        data['swShowCount_list'].append(row['InsertDate']+":"+str(row['swShowCount']))
        data['JyShowCount_list'].append(row['InsertDate']+":"+str(row['JyShowCount']))
        data['ShowCountPercent_list'].append(row['InsertDate']+":"+str(row['ShowCountPercent']))
        data['OfferSeatPercent_list'].append(row['InsertDate']+":"+str(row['OfferSeatPercent']))



if __name__ == '__main__':
    data = {}
    companyid = 2
    pageIndex = 1
    pageSize = 30
    company_response = requests.post('http://ebotapp.entgroup.cn/API/Information/GetCompanyDetail',
                                     data={'companyid': companyid})  # 公司信息
    company_info = company_response.json()  # 公司信息
    print(company_info)
    company_name = company_info['Data']['Table1'][0]['CompanyName']  # 公司名称
    LongCompanyName = company_info['Data']['Table1'][0]['LongCompanyName']  # 公司长名称
    CompanyType = company_info['Data']['Table1'][0]['CompanyType']  # 公司类型
    file_list_response = requests.post('http://ebotapp.entgroup.cn/API/Information/GetCompanyWorks',
                                       data={'companyid': companyid, 'pageIndex': pageIndex, 'pageSize': pageSize})
    file_list = file_list_response.json()  # 电影列表
    totalCounts = int(file_list['Data']['Table2'][0]['TotalCounts'])  # 总电影数
    totalPage = int(file_list['Data']['Table2'][0]['TotalPage'])  # 总页数
    for m in file_list['Data']['Table1']:
        EnMovieID = m['EnMovieID']
        movieName = m['MovieName']
        get_base(EnMovieID)  # 票房汇总信息
        get_people(EnMovieID)  # 剧组人员
        get_company(EnMovieID)  # 相关公司
        releaseDate=''
        if data['ReleaseDate'] != '' :
            if '年' in data['ReleaseDate'] and '月' in data['ReleaseDate'] and '日' in data['ReleaseDate']:
                releaseDate=datetime.datetime.strptime(data['ReleaseDate'], "%Y年%m月%d日")
            if '年' in data['ReleaseDate'] and '月' in data['ReleaseDate'] :
                releaseDate=datetime.datetime.strptime(data['ReleaseDate'], "%Y年%m月")
            else:
                releaseDate=datetime.datetime.strptime(data['ReleaseDate'], "%Y-%m-%d")
            if releaseDate<datetime.datetime.now():
                sDate = releaseDate - datetime.timedelta(days=1)
                eDate = releaseDate + datetime.timedelta(days=10)
                get_index(EnMovieID, sDate, eDate)  # 影响指数
                get_distribute(EnMovieID, sDate, eDate, data['MovieID'])  # 票房分布
                get_boxOffice(EnMovieID, sDate, eDate, data['MovieID'])
                get_audience(EnMovieID)  # 观众
                get_rowPrice(EnMovieID,sDate, eDate, data['MovieID'])
        print(data)
        # base_info_2=base_info_res.json()['Data']['Table1'][1]
        # BoxOfficePoint=base_info_1['BoxOfficePoint'] #点映票房
        # Genre=base_info_1['Genre'] # 类型
        # GenreMain=base_info_1['GenreMain'] #电影主类型
        # ReleaseDate=base_info_1['ReleaseDate'] #上映时间
        # MovieName=base_info_1['MovieName'] #电影名称
        # base_info_2=base_info_res.json()['Data']['Table2'][0]
        # Event=base_info_2['Event'] # 营销事件
        # MoviePhoto=base_info_2['MoviePhoto']  #剧照
        # WeiXinNews=base_info_2['WeiXinNews']  #

    # for page in range(totalPage):
