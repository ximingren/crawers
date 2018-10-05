# -*- coding: utf-8 -*-
import json
import requests
import execjs
import scrapy
from scrapy import Request, FormRequest
from urllib.parse import quote


class MeituanWaiMai(scrapy.Spider):
    name = 'meituan_waimai'
    headers = {
        'Host': 'waimai.meituan.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': 'http://waimai.meituan.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'X-FOR-WITH': 'VBGydN/f1zY33OWHTAQM/aVeTLd777jsKInR3LsQFp5cbXs1ta7rJdyrmE0R7o1VQAmG0u2J2tE2AofpbAuQyj3de9lNmkZxaYczmD5pwz+DXenDQmn0Lk64kb3Whb/2mXtZNLUmqE+j/lqone+MNw==',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7,zh-CN;q=0.6',
    }
    def start_requests(self):
        addr = '天河区'
        cookie = self.get_cookie(addr)
        w_geoid=cookie['w_geoid']
        token_value,param=self.get_token(w_geoid,'0')
        url = 'http://waimai.meituan.com/ajax/poilist?_token=' + str(token_value)
        self.headers['Referer']='http://waimai.meituan.com/home/%s' % w_geoid
        print(param)
        print(cookie)
        print(type(param))
        yield Request(url=url,method='POST',headers=self.headers, cookies=cookie, body=json.dumps(param),
                              callback=self.parse, meta={'cookiejar': cookie, 'w_geoid': w_geoid,'page_offset':param['page_offset']})

    def parse(self, response):
        w_geoid=response.meta['w_geoid']
        page_offset=response.meta['page_offset']+20
        cookie=response.meta['cookiejar']
        print(response)

    def get_token(self,w_geoid,page_offset):
        with open('/home/ximingren/Projects/Projects/crawer_summary/common_crawer/common_crawer/js/rohr.min.js',
                  'r') as f:
            js_content = f.read()
        content = execjs.compile(js_content)
        param = {
            'classify_type': 'cate_all',
            'sort_type': '0',
            'price_type': '0',
            'support_online_pay': '0',
            'support_invoice': '0',
            'support_logistic': '0',
            'page_offset': page_offset,
            'page_size': '20',
            'mtsi_font_css_version': 'dd53a913'
        }
        param['uuid'] = 'zDzgfvpaDrj6ywDDwhFlvYM11eVH2hZxSNYgUkmFcRy6yKCxCoU1Eb3rovTrGfXJ'
        param['platform'] = '1'
        param['partner'] = '4'
        param['originUrl'] = 'http%3A%2F%2Fwaimai.meituan.com%2Fhome%2F{w_geoid}'.format(w_geoid=w_geoid)
        toCaledParams = ''
        for key, value in param.items():
            toCaledParams = toCaledParams + str(key) + '=' + str(value) + '&'
        toCaledParams = toCaledParams[:-1]
        token_value = content.call('start', toCaledParams)
        return token_value,param

    def get_geoid(self, addr):
        headers = {
            'Host': 'waimai.meituan.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7,zh-CN;q=0.6',
            'Cookie': '_lxsdk_cuid=16598202022c8-045e74ca8ab789-3c720356-1fa400-16598202026c8; iuuid=673824EB30BBFD121F44D0519AE750F92C2947BB8F3D55A5BF3A1687653EF215; _lxsdk=673824EB30BBFD121F44D0519AE750F92C2947BB8F3D55A5BF3A1687653EF215; w_utmz="utm_campaign=(direct)&utm_source=(direct)&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_uuid=zDzgfvpaDrj6ywDDwhFlvYM11eVH2hZxSNYgUkmFcRy6yKCxCoU1Eb3rovTrGfXJ; ci=20; rvct=20%2C118; cityname=%E5%B9%BF%E5%B7%9E; i_extend=H__a100001__b1; webp=1; __utma=74597006.1515590683.1536065731.1536065731.1536065731.1; __utmz=74597006.1536065731.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __mta=42901018.1536061975909.1536071949924.1536072311369.14"; _ga=GA1.3.1515590683.1536065731; w_visitid=511cec6d-b2b9-4768-b201-8676bac84d83; _ga=GA1.2.1515590683.1536065731; _gid=GA1.2.1624848520.1536847730; _gid=GA1.3.1624848520.1536847730; waddrname=2; w_geoid=ws0e6fzpjvuz; w_cid=440105; w_cpy=haizhuqu; w_cpy_cn="%E6%B5%B7%E7%8F%A0%E5%8C%BA"; w_ah="23.087628912180662,113.33384077996016,2|23.88762893155217,113.33384077996016,%EF%BF%BD|23.163997940719128,113.36138069629669,1"; JSESSIONID=t7ioy21zbtm65m9d03to4yvw; _lxsdk_s=165d343ad3d-3f8-606-b97%7C%7C8'
        }
        res = requests.get(
            'https://restapi.amap.com/v3/geocode/geo?address=%s&output=json&key=2665bc462508156f146b06a6589d32eb' % (
                addr))
        location = res.json()['geocodes'][0]['location'].split(',')
        lng = location[0].strip()
        lat = location[1].strip()
        res = requests.get('http://waimai.meituan.com/geo/geohash?lat=%s&lng=%s&addr=1' %
                           (lat, lng), headers=headers)
        w_geoid = res.cookies['w_geoid']
        return w_geoid

    def get_city_info(self, addr):
        citys = json.load(open(
            '/home/ximingren/Projects/Projects/crawer_summary/common_crawer/common_crawer/json/city_list.json'))
        a = citys['citys']
        for x in a:
            if addr in str(x):
                return x

    def get_cookie(self, addr):
        w_geoid = self.get_geoid(addr)
        city_info = self.get_city_info(addr)
        w_cpy = city_info['pinyin']
        w_cid = city_info['city_id']
        cookie = dict()
        cookie['w_cpy'] = w_cpy
        cookie['w_cid'] = w_cid
        addr_encode = quote(addr)
        cookie['w_cpy_cn'] = addr_encode
        cookie['w_geoid'] = w_geoid
        cookie['waddrname'] = '%E4%B8%80%E8%A1%97'
        return cookie