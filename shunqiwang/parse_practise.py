import datetime
import re

import requests
from lxml import etree

def del_rn(need_del_list):
    for e in list(need_del_list):
        if '\r\n' in e and len(e)<10:
            del need_del_list[need_del_list.index(e)]
        # if ' , ' in need_del_list:
        #     del need_del_list[need_del_list.index(' , ')]
        # if ' ' in need_del_list:
        #     del need_del_list[need_del_list.index(' ')]
def parse():

    tree=etree.parse('2.html',etree.HTMLParser())
    info = tree.xpath('.//table[@class="codl"]//td/text()')
    print(info)
    company_name = tree.xpath('.//div[@id="nav"]//text()')
    del_rn(company_name)
    del_rn(info)
    data={}
    data['company_name']=company_name[-2]
    for e in info:
        if '主要经营产品' in e:
            products = info[info.index(e) + 1:info.index('经营范围：')]
            products=''.join(products)
            data['products']=products
        if '经营范围' in e:
            business_scope = info[info.index(e) + 1]
            data['business_scope']=business_scope
        if '营业执照号码' in e:
            license_number = info[info.index(e) + 1]
            data['license_number']=license_number
        if '经营模式' in e:
            business_model = info[info.index(e) + 1]
            data['business_model']=business_model
        if '成立时间' in e:
            established_time = info[info.index(e) + 1]
            if '-' not in established_time:
                year=established_time[:4]
                month=established_time[5:7]
                day=established_time[8:10]
                established_time=year+'-'+month+'-'+day
            data['established_time']=established_time
        if '职员人数' in e:
            person_number = info[info.index(e) + 1][:-1]
            data['person_number']=person_number
        if '注册资本' in e:
            registered_capital = info[info.index(e) + 1]
            data['registered_capital']=registered_capital
    print(data)

def prox_request():
    data = requests.get('http://www.ip111.cn/', proxies={'http': 'http://106.56.102.200:8070'})
    print(data.content.decode('utf-8'))
if __name__ == '__main__':
    parse()
