import csv
import datetime
import os
import pandas as pd
import time

import requests

def save_data(data_list,fileName):
    try:
        conditon = False
        if not os.path.exists(fileName+ '.csv'):
            conditon = True
        with open(fileName + '.csv', 'a', newline='') as f:  # file_path 是 csv 文件存储的路径
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
    data = pd.read_csv(fileName+'.csv')
    data.to_excel(fileName + '.xlsx', index=False)

if __name__ == '__main__':
    url='http://m.mtime.cn/#!/theater/290/1039/date/20181106/'
    index=url.split('/').index('date')-1
    print(url.split('/')[index])

    # field=['播出日期','播出时间','影片名称','影厅名称','影片类型']
    # cinemaId='1039'
    # fileName=input('输入XLX的文件名')
    # url = "https://ticket-api-m.mtime.cn/cinema/showtime.api?cinemaId=%s"%cinemaId
    # res = requests.get(url)
    # data = res.json()
    # showTimesList = []
    # moviesName = {}
    # moviesType = {}
    # if data['msg'] != '成功':
    #     print("抓取失败请稍候再试")
    # else:
    #     cinema = data['data']['cinema']['name']
    #     movies = data['data']['movies']
    #     for m in movies:
    #         moviesName[m['movieId']] = m['title']
    #         moviesType[m['movieId']] = m['type']
    # showtimes = data['data']['showtimes']
    # for s in showtimes:
    #     movieId=s['movieId']
    #     for i in s['list']:
    #         timeStamp=i['showDay']
    #         dateArray = datetime.datetime.fromtimestamp(timeStamp)
    #         showTimesList.append({'播出日期': dateArray.date(),'播出时间':dateArray.time(),'影片名称':moviesName[movieId],'影厅名称':i['hall'],'影片类型':moviesType[movieId]})
    #
    # save_data(showTimesList,fileName)
    # csv_to_excel(fileName)