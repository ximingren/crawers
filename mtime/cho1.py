# coding:UTF-8
import csv
import datetime
import json
import os
import pandas as pd
import queue
import requests


def crawl_cinema(args):
    city = args[0]
    cinema = args[1]
    cinemaFile = args[2]
    cityList = json.load(open('city.json','r',encoding='utf-8'))
    cityId = None
    for i in cityList['locations']['List']:
        if i['NameCn'] == city:
            cityId = i['Id']
    if cityId == None:
        print('找不到该城市')
        exit(1)
    date = '20181106'
    res = requests.get(
        'http://m.mtime.cn/Service/callback.mi/Showtime/SearchVoice.api?keyword=%s&searchType=3&locationId=%s' % (
            cinema, cityId))
    cinemaList = []
    if res.json()['locationCinemasCount'] == 0:
        print('无搜索结果')
    else:
        for x in res.json()['locationCinemas']:
            url = 'http://m.mtime.cn/#!/theater/%s/%s/date/%s/' % (cityId, x['id'], date)
            cinemaList.append(x['name'] + "," + url + '\n')
        f=open(cinemaFile, 'a',encoding='utf-8')
        for c in cinemaList:
            f.write(c + '\n')
        f.close()
        print('保存cinema数据成功')

def crawl_showTimes():
    args = input('输入需要抓取的url和xls文件名')
    args = args.split()
    if len(args)<2:
        args = input('输入的参数不够，请再次输入')
        args = args.split()
    url = args[0]
    resultFile = args[1]
    print('抓取%s的数据' % url)
    index = url.split('/').index('date') - 1
    cinemaId = (url.split('/')[index])
    url = "https://ticket-api-m.mtime.cn/cinema/showtime.api?cinemaId=%s" % cinemaId
    res = requests.get(url)
    data = res.json()
    showTimesList = []
    moviesName = {}
    moviesType = {}
    if data['msg'] != '成功':
        print("抓取失败请稍候再试")
    else:
        cinema = data['data']['cinema']['name']
        movies = data['data']['movies']
        for m in movies:
            moviesName[m['movieId']] = m['title']
            moviesType[m['movieId']] = m['type']
    showtimes = data['data']['showtimes']
    for s in showtimes:
        movieId = s['movieId']
        for i in s['list']:
            timeStamp = i['showDay']
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            showTimesList.append(
                {'播出日期': dateArray.date(), '播出时间': dateArray.time(), '影片名称': moviesName[movieId], '影厅名称': i['hall'],
                 '影片类型': moviesType[movieId]})
    save_data(showTimesList, resultFile)
    csv_to_excel(resultFile)

def save_data(data_list, fileName):
    try:
        conditon = False
        if not os.path.exists(fileName + '.csv'):
            conditon = True
        with open(fileName + '.csv', 'a', newline='',encoding='utf-8') as f:
            fieldnames = field
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if conditon:
                writer.writeheader()  # 写入头部，即设置列名
            for data in data_list:
                writer.writerow(data)
    except Exception as e:
        print('保存数据错误', e)
    else:
        print("保存数据成功,文件名为%s" % fileName)


def csv_to_excel(fileName):
    data = pd.read_csv(fileName + '.csv',encoding='utf-8')
    data.to_excel(fileName + '.xlsx', index=False,encoding='utf-8')


if __name__ == '__main__':
    field = ['播出日期', '播出时间', '影片名称', '影厅名称', '影片类型']
    args = input('输入城市名、影院名、txt文件名')
    args = args.split()
    if len(args)<3:
        args=input('输入的参数不够，请再次输入')
        args=args.split()
    crawl_cinema(args)
    crawl_showTimes()
