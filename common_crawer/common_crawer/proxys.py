import json
import random

import requests

from common_crawer.common_crawer.MongoQueue import MongoQueue


def get_ip1():
    # scylla
    print('代理池1')
    response = requests.get('http://localhost:8899/api/v1/proxies?anonymous=True&https=true')
    data = json.loads(response.text)
    proxies = random.choice(data['proxies'])
    if proxies['is_https']:
        proxy = {'https': 'https://' + str(proxies['ip']) + ":" + str(proxies['port'])}
    else:
        proxy = {'http': 'http://' + str(proxies['ip']) + ":" + str(proxies['port'])}
    return proxy


def get_ip2():
    """
    老是出现Max retries exceeded with url:的报错，可用率低
    :return:
    """
    # IPProxy
    print('代理池2,IPProxy')
    r = requests.get('http://127.0.0.1:8000/?types=0&count=100&protocol=1')
    ip_ports = json.loads(r.text)
    ip = random.choice(ip_ports)[0]
    port = random.choice(ip_ports)[1]
    proxies = {
        # 'https': 'https://%s:%s' % (ip, port),
        'http': 'http://%s:%s' % (ip, port)
    }
    return proxies


def get_ip3():
    # proxy-pool,用的是redis 6378
    response = requests.get('http://127.0.0.1:5010/get_all/')
    print('代理池3,proxy_pool')
    proxy = random.choice(list(response.json()))
    return {'https': 'https://' + proxy,
            'http': 'http://' + proxy}


def get_ip4():
    #阿步云
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9010"

    # 代理隧道验证信息
    proxyUser = "HCD2I6F04L7TCOFP"
    proxyPass = "304B0FB51A25B5E6"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


def get_ip5():
    # 芝麻代理
    print('芝麻代理')
    res = requests.get(
        "http://http.tiqu.alicdns.com/getip3?num=20&type=2&pro=&city=0&yys=0&port=11&pack=34488&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=")
    data = res.json()['data'][0]
    ip = data['ip']
    port = data['port']
    proxies = {'https': 'https://%s:%s' % (ip, port),'http': 'http://%s:%s' % (ip, port)}
    return proxies


def get_ip6():
    # proxy_list
    print('代理池6,proxy_list')
    res = requests.get("http://localhost:8111/proxy?count=100&annoymity=anonymous&protocol=https")
    result = random.choice(res.json())
    ip = result[0]
    port = result[1]
    print(ip)
    proxies = {'https': 'https://%s:%s' % (ip, port),
               'http': 'http://%s:%s' % (ip, port)}
    return proxies


def get_ip7():
    print('代理池7, IP-POOL')
    # IP-POOL
    res = requests.get('http://localhost:22555/get_all/')
    result = random.choice(res.json())
    return {'https': 'https://' + result,'http': 'http://' + result}


def get_ip8():
    print('代理池8,ProxyPool')
    # ProxyPool
    #几乎不能用
    res = requests.get('http://localhost:5555/random')
    return {'https': 'https://' + res.text,'http': 'http://' + res.text}


def get_ip9():
    #fp-server
    print('代理池9,fp-server')
    res = requests.get('http://localhost:12345/api/proxy/?count=100&scheme=HTTPs&anonymity=anonymous')
    proxy = random.choice(res.json()['data']['detail'])['url']
    return {'https': proxy,'http': proxy}


def get_ip10():
    print('蜻蜓代理')
    q = MongoQueue('proxy', 'zhima')
    return q.popProxy()
