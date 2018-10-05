import gc
import json
import sys
from pprint import pprint

import execjs
from urllib.parse import quote
import requests

Cookie = {
    # 'w_uuid': 'zDzgfvpaDrj6ywDDwhFlvYM11eVH2hZxSNYgUkmFcRy6yKCxCoU1Eb3rovTrGfXJ',
    # '_lx_utm': 'utm_source%3D9',
    # 'mtcdn': 'K',
    # 'i_extend': 'H__a100001__b1',
    # '_gid': 'GA1.3.1788558612.1536505606',
    # '_ga': 'GA1.3.1515590683.1536065731',
    # '__utmz': '74597006.1536065731.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)	',
    # '__utma': '74597006.1515590683.1536065731.1536065731.1536065731.1',
    # 'iuuid': '673824EB30BBFD121F44D0519AE750F92C2947BB8F3D55A5BF3A1687653EF215',
    # '_lxsdk': '673824EB30BBFD121F44D0519AE750F92C2947BB8F3D55A5BF3A1687653EF215',
    # 'uuid': '604353dbecf5448dae04.1535855560.1.0.0',
    # 'w_visitid': '49906311-9916-4bee-b0cc-9b23a51a887c	',
    # '__mta': '42901018.1536061975909.1536072311369.1536213047673.15',
    # '__mta': '42901018.1536061975909.1536071949924.1536072311369.14',
    # 'rvct': '20%2C118',
    # 'ci': '20',
    # '_lxsdk_s': '165c352f862-42f-280-d71%7C%7C1	',
    # '_lxsdk_cuid': '16598202022c8-045e74ca8ab789-3c720356-1fa400-16598202026c8	',
    # 'webp': '1',
    # 'w_utmz': '"utm_campaign=(direct)&utm_source=(direct)&utm_medium=(none)&utm_content=(none)&utm_term=(none)"	',
    # 'w_ah': '"23.100222889333963,113.34044571965933,%E5%B9%BF%E4%B8%9C%E7%9C%81%E7%AC%AC%E4%BA%8C%E4%BA%BA%E6%B0%91%E5%8C%BB%E9%99%A2|22.998874951153994,113.46286375075579,%E9%87%91%E7%9B%9B%E4%B8%80%E8%B7%AF"	',
}


def get_list():
    try:
        addr = '白云区'
        w_geoid = get_geoid(addr)
        city_info = get_city_info(addr)
        w_cpy = city_info['pinyin']
        w_cid = city_info['city_id']
        Cookie['w_cpy'] = w_cpy
        Cookie['w_cid'] = w_cid
        addr_encode = quote(addr)
        # Cookie['JSESSIONID'] = 'cc202xj1b15t1qjdud1yxyxsa'
        # Cookie['cityname'] = '%E5%B9%BF%E5%B7%9E'
        Cookie['w_cpy_cn'] = addr_encode
        Cookie['w_geoid'] = w_geoid
        Cookie['waddrname'] = '%E4%B8%80%E8%A1%97'
        headers = {
            'Host': 'waimai.meituan.com',
            'Connection': 'keep-alive',
            'Content-Length': '329',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'http://waimai.meituan.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'X-FOR-WITH': 'VBGydN/f1zY33OWHTAQM/aVeTLd777jsKInR3LsQFp5cbXs1ta7rJdyrmE0R7o1VQAmG0u2J2tE2AofpbAuQyj3de9lNmkZxaYczmD5pwz+DXenDQmn0Lk64kb3Whb/2mXtZNLUmqE+j/lqone+MNw==',
            'Referer': 'http://waimai.meituan.com/home/%s' % w_geoid,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7,zh-CN;q=0.6',
            # 'Cookie': '_lxsdk_cuid=16598202022c8-045e74ca8ab789-3c720356-1fa400-16598202026c8; iuuid=673824EB30BBFD121F44D0519AE750F92C2947BB8F3D55A5BF3A1687653EF215; _lxsdk=673824EB30BBFD121F44D0519AE750F92C2947BB8F3D55A5BF3A1687653EF215; w_utmz="utm_campaign=(direct)&utm_source=(direct)&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_uuid=zDzgfvpaDrj6ywDDwhFlvYM11eVH2hZxSNYgUkmFcRy6yKCxCoU1Eb3rovTrGfXJ; ci=20; rvct=20%2C118; cityname=%E5%B9%BF%E5%B7%9E; i_extend=H__a100001__b1; webp=1; __utma=74597006.1515590683.1536065731.1536065731.1536065731.1; __utmz=74597006.1536065731.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __mta=42901018.1536061975909.1536071949924.1536072311369.14"; __mta=42901018.1536061975909.1536072311369.1536213047673.15; _ga=GA1.3.1515590683.1536065731; w_visitid=fa880be0-cf20-4f41-8166-2281349fa877; waddrname="%E4%B8%9C%E6%96%B9%E4%B8%80%E8%B7%AF"; w_geoid=ws0crp6qg0p1; w_cid=440306; w_cpy=baoanqu; w_cpy_cn="%E5%AE%9D%E5%AE%89%E5%8C%BA"; w_ah="22.760710883885622,113.86553272604942,%E4%B8%9C%E6%96%B9%E4%B8%80%E8%B7%AF|23.100222889333963,113.34044571965933,%E5%9C%B0%E7%8E%8B%E5%9B%BD%E9%99%85%E5%95%86%E4%BC%9A"; JSESSIONID=1w30zpg6xh4b31uvkpcvvlpjns; _lxsdk_s=165d069f5d5-16d-206-fa5%7C%7C12'
        }
        token_value, param = test_func(w_geoid)
        print(token_value)
        url = 'http://waimai.meituan.com/ajax/poilist?_token=' + 'eJxNTl1vqkAU/C/7KhEWVMCkD6CAYkEF8aOND6zA8iFUl0XA5v73u01s0slJZs6cOcl8A7KMwBQKDDIHHjEBUwCHwnACOEBrdhlLsihDRRSgMOHA5a83mkjyiAOI7Odg+gkZOEmA5x/HY8YnVEWBg4IinLmXVsfSmRNHbH5SSxYCKaW3Kc+3YVaG2bCMM9qE1fDyVfJtLcRYwektSivWBrCXcsdeGBcvDl9Mf3eH1WfZOsMVU7HduTmB6/apBR4dXLcKKm9Q04t7bOFCazXDCrrd+5oeN7pK9rUtVr2qefstFQcXybdQf3AzfbHv3E2Bg9LDGs2dW51diqC5eEW+6HXDdpJQrZY5qanrYQM22ekE78cC8bZiWtgkGcSTrz3yZXvsdah3vBATaVeJyvh6LHN8M32jW5E+1c3qZB66rYHXGnksH7ppB0ivV1t7tZ4LpC5wysd8PHiqhqvO/Eq/zq3SncUhWlrHnfb4wAcxSU41KWPq3ZW7s5GilJC4eYofOVau/kGRYBKN+QUchDO0kJvju+qKMW2jSPUDCgdo67ioMZ1kPqFJu772I/z2Bv79B1yjqLw='
        res = requests.post(
            url,
            headers=headers, data=param, cookies=Cookie,proxies={'http':'http://127.0.0.1:8082'})
        print(res.status_code)
        print(res.text)
        print(res.json())

    except Exception as e:
        print(e)


def test_func_pyv8(w_geoid):
    try:
        with open(
                '/home/ximingren/Projects/Projects/crawer_summary/common_crawer/common_crawer/test_case/meituan_waimai/rohr.min.js',
                'r') as f:
            js_content = f.read()
        with PyV8.JSContext() as ctxt:
            ctxt.eval(js_content)
            param = {
                'classify_type': 'cate_all',
                'sort_type': '0',
                'price_type': '0',
                'support_online_pay': '0',
                'support_invoice': '0',
                'support_logistic': '0',
                'page_offset': '21',
                'page_size': '20',
                'mtsi_font_css_version': 'dd53a913'
            }
            param['uuid'] = 'zDzgfvpaDrj6ywDDwhFlvYM11eVH2hZxSNYgUkmFcRy6yKCxCoU1Eb3rovTrGfXJ'
            param['platform'] = '1'
            param['partner'] = '4'
            param['originUrl'] = 'http%3A%2F%2Fwaimai.meituan.com%2Fhome%2F{w_geoid}'.format(w_geoid=w_geoid)
            print(param['originUrl'])
            vars = ctxt.locals
            vars.href = param['originUrl']
            vars.PARAM = param
            print(vars.to)
            token_value = content.call('start', param)
            return token_value, param
        # print(a)
        # ctxt.eval(f.read())
        # vars = ctxt.locals
        # param = {
        #     'classify_type': 'cate_all',
        #     'sort_type': '0',
        #     'price_type': '0',
        #     'support_online_pay': '0',
        #     'support_invoice': '0',
        #     'support_logistic': '0',
        #     'page_offset': 0,
        #     'page_size': '20',
        #     'mtsi_font_css_version': 'dd53a913'
        # }
        # param['uuid'] = 'zDzgfvpaDrj6ywDDwhFlvYM11eVH2hZxSNYgUkmFcRy6yKCxCoU1Eb3rovTrGfXJ'
        # param['platform'] = '1'
        # param['partner'] = '4'
        # param['originUrl'] = 'http%3A%2F%2Fwaimai.meituan.com%2Fhome%2F{w_geoid}'.format(w_geoid=w_geoid)
        # vars.PARAM = param
        # vars.href = 'http%3A%2F%2Fwaimai.meituan.com%2Fhome%2F{w_geoid}'.format(w_geoid=w_geoid)
        # token_value = vars.token
        # return token_value,param
    except Exception as e:
        print('异常', e)


def test_func_genToken(w_geoid):
    with open(
            '/home/ximingren/Projects/Projects/crawer_summary/common_crawer/common_crawer/test_case/meituan_waimai/get_token.js',
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
        'page_offset': '20',
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
    token_value = content.call('genToken',toCaledParams)
    return token_value,param


def test_func(w_geoid):
    try:
        with open(
                '/home/ximingren/Projects/Projects/crawer_summary/common_crawer/common_crawer/js/rohr_min.js',
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
            'page_offset': '21',
            'page_size': '20',
            'mtsi_font_css_version': 'dd53a913'
        }
        param['uuid'] = 'zDzgfvpaDrj6ywDDwhFlvYM11eVH2hZxSNYgUkmFcRy6yKCxCoU1Eb3rovTrGfXJ'
        param['platform'] = '1'
        param['partner'] = '4'
        param['originUrl'] = 'http://waimai.meituan.com/home/{w_geoid}'.format(w_geoid=w_geoid)

        toCaledParams = ''
        for key, value in param.items():
            toCaledParams = toCaledParams + str(key) + '=' + str(value) + '&'
        toCaledParams = toCaledParams[:-1]
        token_value = content.call('start', param)
        return token_value, param
    except Exception as e:
        print('异常', e)


def get_token():
    with open('get_token.js', 'r') as f:
        with PyV8.JSContext() as env:
            env.eval(f.read())
            vars = env.locals
            genToken = vars.genToken
            param = {
                'classify_type': 'cate_all',
                'sort_type': 0,
                'price_type': 0,
                'support_online_pay': 0,
                'support_invoice': 0,
                'support_logistic': 0,
                'page_offset': 21,
                'page_size': 20,
                'mtsi_font_css_version': 'mtsi_font_css_version'
            }
            param['uuid'] = 'zDzgfvpaDrj6ywDDwhFlvYM11eVH2hZxSNYgUkmFcRy6yKCxCoU1Eb3rovTrGfXJ'
            param['platform'] = 1
            param['partner'] = 4
            param['originUrl'] = 'http://waimai.meituan.com'
            totalParam = ''
            for key, value in param.items():
                totalParam = totalParam + key + '=' + str(value) + '&'
            totalParam = totalParam[:-1]
            value = genToken('100007', 'http://waimai.meituan.com/ajax/poilist?' + totalParam)
            return value
            # a=ctx.call('genToken','1','http://waimai.meituan.com/ajax/poilist?_token=eJxNksuSojAUht+FrZQkQAJxh9cGURpEdOzqBSAq2KByVbrm3Sc402ayyVf/+c8lp/LN5fqeG0BAj8JzdZRzAw72QR9zPFcWNIIkjABCKpIQ4bnwPw0DIhHAc0HujbnBBwRQ5kVJ/OwUhwofkIiAh0AFn/wPI+mTF6lN7lw6NXGnsrwOBKHx49SP+2kUl5Wf9cNLKpwuaSQ0BYiURAnuIanpSBzNS90uD4mEh4qIqIgkyFDsED9RZogYKgzJC2XIkHllZkDMgFgLxFogloYwQ1YBSwyZqrK66msyDF91MXsQZjNgBfy8GJNnXUBRgV1jqHYoPVHu8DkkhB0+Z/iLyj+VLvTcLZTePlusivix7nXB8ie4oD+DJhbxMaMUGfdlkkOrabW1U/a+bNVPfX/ond0GTrXVSLPj2DSCfBtHkmjijXJ4yC4gtrF3Swvss95st4rvQ9twsKs9dtPhCIP23Cwew+3uMVvrtRYezqNGeUuJWayyeTJuRH9W1RunSiq1bm1fc6xxpBXOUjSL7Gw6mX5SRhrZfJGZtUlbdL8cjeVKWxnB9BQuIs0Xt5P2eGm270EyzxzPPY93xTy561V73+30oSDse4fwDZulv75VyfzXzAYOuoanW7kY7VfGe2Elj0coeZVnkQla9/Ll1PWAhUAtqddRfVK3ZnCQhTqvb19CO8G9q+dh6YKC26VW7F56FQTtHVfllRxLtXybW9zvP1AJ6L8=')
            # print(a)


def execute_js():
    with PyV8.JSContext() as ctxt:
        with open('rohr.min.js', 'r') as f:
            ctxt.eval(f.read())
            vars = ctxt.locals
            token_value = vars.token
            print(a)


def get_geoid(addr):
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
    # res=requests.get('http://api.map.baidu.com/geocoder?address=%s&output=json&key=37492c0ee6f924cb5e934fa08c6b1676'%(addr))
    # lng=res.json()['result']['location']['lng']
    # lat=res.json()['result']['location']['lat']
    res = requests.get('http://waimai.meituan.com/geo/geohash?lat=23.163998&lng=113.361381&addr=1', headers=headers)
    w_geoid = res.cookies['w_geoid']
    return w_geoid


def get_city_info(addr):
    citys = json.load(open('city_list.json'))
    a = citys['citys']
    for x in a:
        if addr in str(x):
            return x


def test_html():
    res=requests.get('http://localhost:63342/crawer_summary/common_crawer/common_crawer/test_case/meituan_waimai/test_ajax.html?_ijt=ua8arkb2ekj6s3bpdnnpl0tlp2')
    print(res.text)



if __name__ == '__main__':
    get_list()
    # get_token()
    # execute_js()
    # get_geoid()
    # get_city()
    # addr='广州'
    # res=requests.get('https://restapi.amap.com/v3/geocode/geo?address=%s&output=json&key=2665bc462508156f146b06a6589d32eb'%(addr))
    # print(res.text)
    # test_func()
    # test_html()

