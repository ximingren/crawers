import json
from pprint import pprint

import chardet
import requests
from lxml import etree


def meituan():
    pois_list_params={
    'cityId':'{cityId}',
    'offset':'{offset}',
    'limit':str(20),
    'startDay':str(20180902),
    'endDay':str(20180902),
    'areald':str(1),
    # 'q':'',
    # 'hotelStar':1,
    # 'brandid':1,
    # 'price':''
    }
    pois_list_url='https://ihotel.meituan.com/hbsearch/HotelSearch?version_name=999.99&cateId=20&attr_28=129'
    for key,val in pois_list_params.items():
        pois_list_url +="&%s=%s"%(key,val)
    # format_url=pois_list_url.format(cityId='1',offset='20')
    # response=requests.get(format_url)
    # # tree=etree.HTML(response.content.decode('utf-8'))
    # # div_list=tree.xpath('.//article[@class="poi-item"]')
    # # pages=int(''.join(tree.xpath('.//li[@class="page-link"][last()]//text()')))
    # # print(pages)
    # # for div in div_list:
    # #     title=div.xpath(".//a[@class='poi-title']//text()")
    # #     print(title)
    # pois_list = json.loads(response.text)
    # totalcount=pois_list['data']['totalcount']
    # print(totalcount)
    for x in range(20):
        for j in range(int(round(10))):
            format_url = pois_list_url.format(cityId=str(x),offset=str(j*20))
            response=requests.get(format_url)
            pois_list = json.loads(response.text)
            if pois_list['data']['count']!=str(0):
                print(x)
                break
            else:
                searchResult_list=pois_list['data']['searchresult']
                for each in searchResult_list:
                    name=each['name']
                    addr=each['addr']
                    areaName=each['areaName']
                    score=each['avgScore']
                    lowestPrice=each['lowestPrice']
                    poiid=each['poiid']
                    poiRecommendTag=each['poiRecommendTag']
                    poiAttrTagList=each['poiAttrTagList']
                    historyCouponCount=each['historyCouponCount']
                    commentsCountDesc=each['commentsCountDesc']
                    print(name,addr,areaName,score,lowestPrice,
                          poiid,poiRecommendTag,poiAttrTagList,historyCouponCount,commentsCountDesc[:-3])


def meituan_city():
    with open('../meituan_city.json','r') as f:
        city=json.loads(f.read())
        for x in city['data']:
            cityId=x['id']
            cityName=x['name']
            print(cityId,cityName)


if __name__ == '__main__':
    meituan_city()