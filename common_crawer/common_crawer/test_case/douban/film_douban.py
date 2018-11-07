import json
import random
import time

import pymongo
import requests
from lxml import etree
from common_crawer.common_crawer.MongoQueue import MongoQueue
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'text/html;charset=UTF-8',
    'Cache-Control': 'no-cache',
    'Host': 'movie.douban.com',
    'Pragma':'no-cache',
    'Referer': 'www.baidu.com',
    # 'Cookie': 'll="118282"; bid=ctyiEarSLfw; ps=y; __yadk_uid=0Sr85yZ9d4bEeLKhv4w3695OFOPoedzC; dbcl2="155150959:OEu4dds1G1o"; as="https://sec.douban.com/b?r=https%3A%2F%2Fbook.douban.com%2F"; ck=fTrQ; _pk_id.100001.4cf6=c86baf05e448fb8d.1506160776.3.1507290432.1507283501.; _pk_ses.100001.4cf6=*; __utma=30149280.1633528206.1506160772.1507283346.1507290433.3; __utmb=30149280.0.10.1507290433; __utmc=30149280; __utmz=30149280.1506160772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1475767059.1506160772.1507283346.1507290433.3; __utmb=223695111.0.10.1507290433; __utmc=223695111; __utmz=223695111.1506160772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); push_noty_num=0; push_doumail_num=0',

    # 'Upgrade-Insecure-Requests':'1',
    # 'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)',
]

def crawer_main():
    while True:
        try:

            id, url, star = doubanqueue.pop()
        except KeyError:
            print('队列没有数据')
        else:
            data={}
            data['url']=url
            data['id'] = id
            data['star'] = star
            crawer_detail(id, url, data)

def openlink(id,url,data):
    """
    urlopen error 10060错误}
    :param url:  请求的网址
    :param headers: 报文头部信息
    :return: 服务器响应
    """
    maxTryNum = 15
    banIp=[]
    for tries in range(maxTryNum):
        try:
            proxies=get_ip3()
            while(proxies in banIp):
                proxies=get_ip3()
            print('使用代理',proxies)
            if not 'm.douban.com' in url:
                headers['Host']='movie.douban.com'
            else:
                headers['Host']='m.douban.com'
            headers['User-Agent']=random.choice(UserAgent_List)
            headers['Referer']=data['url']
            # time.sleep(2)
            res = requests.get(url, headers=headers,proxies=proxies)
            if "https://sec.douban.com/a" in res.text:
                banIp.append(proxies)
                print('添加ban掉的',proxies)
                break
            #     res=openlink(url)
            print(res.status_code)
            if res.status_code==200:
                print("请求成功",url)
                return res
            elif res.status_code==404:
                doubanqueue.errorId(id)
                break
        except Exception  as e:
            print(e)
            if tries < (maxTryNum - 1):
                continue
            else:
                print("尝试%d 次连接网址%s失败!" % (maxTryNum, url))
def get_ip4():


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
        # "https": proxyMeta,
    }
    return proxies
def get_ip():
    response = requests.get('http://localhost:8899/api/v1/proxies?anonymous=True')
    data = json.loads(response.text)
    proxies = random.choice(data['proxies'])
    if proxies['is_https']:
        proxy = 'https://' + str(proxies['ip']) + ":" + str(proxies['port'])
    else:
        proxy = 'http://' + str(proxies['ip']) + ":" + str(proxies['port'])
    return {'http':proxy}

def get_ip2():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=5&country=国内')
    ip_ports = json.loads(r.text)
    ip = ip_ports[0][0]
    port = ip_ports[0][1]
    proxies = {
        'http': 'http://%s:%s' % (ip, port),
        'https': 'http://%s:%s' % (ip, port)
    }
    return proxies
def get_ip3():
    response = requests.get('http://127.0.0.1:5010/get/')
    return {'http':'http://'+response.text}

def crawer_detail(id, url, data):
        detailRes = openlink(id,url,data)
        try:
            tree = etree.HTML(detailRes.text)
            name = ''.join(tree.xpath("//div[@id='content']/h1/span[1]/text()"))
            year = ''.join(tree.xpath("//div[@id='content']/h1/span[2]/text()"))
            Content = tree.xpath('//div[@class="subject clearfix"]/div[@id="info"]//text()')
            parse_content(Content, data)
            rating_num = ''.join(tree.xpath("//strong[@class='ll rating_num']/text()"))
            rating_people = ''.join(tree.xpath('//a[@class="rating_people"]/span//text()'))
            rating_item = tree.xpath('//div[@class="ratings-on-weight"]/div')
            rating_betterthan = '/'.join(list(
                filter(lambda t: t != '',
                       map(lambda x: x.strip(), tree.xpath("//div[@class='rating_betterthan']//text()")))))
            rating_stars = []
            for weight in rating_item:
                rating_stars.append(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(),
                                                                               weight.xpath(
                                                                                   './span[1]/text()') + weight.xpath(
                                                                                   './span[2]/text()'))))))
            recommendations = tree.xpath("//div[@class='recommendations-bd']/dl")
            recommend = []
            for r in recommendations:
                recommend.append(''.join(r.xpath('./dd/a/text()')))
            tags = tree.xpath("//div[@class='tags']/div/a/text()")
            data['name'] = name
            data['year'] = year
            data['tags'] = ','.join(tags)
            data['recommend'] = '/'.join(recommend)
            data['rating_num'] = rating_num
            data['rating_people'] = rating_people
            data['rating_stars'] = '/'.join(rating_stars)
            data['rating_betterthan'] = rating_betterthan
            crawer_award(id, data)
            crawer_topic(id, data)
            save_database(data)
            doubanqueue.completeId(id)
        except Exception as e:
            print(e)
def save_database(data):
    cli = pymongo.MongoClient('123.207.42.164', 27017)
    db = cli['douban']
    try:
        db['douban2'].update({'_id': data['id']}, {'$set': data}, True)
    except Exception as e:
        print('保存数据错误到数据库')
    else:
        print('保存数据成功到数据库',data['id'])

def parse_content(Content, data):
    valueList = ''.join(Content).split(Content[0])
    for i in valueList:
        if i != '':
            key = i.split(': ')[0]
            value = i.split(': ')[1]
            if 'IMDb链接' in key:
                data[key] = 'https://www.imdb.com/title/' + value.replace('\n', '') + '/'
            else:
                data[key] = value


def crawer_award(id,data):
    awardUrl = 'https://movie.douban.com/subject/%s/awards/' % id
    awardRes = openlink(id,awardUrl,data)
    tree = etree.HTML(awardRes.text)
    awardsList = tree.xpath("//div[@class='article']/div")
    awards_result = {}
    for awards in awardsList:
        awardName = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(),awards.xpath("./div[@class='hd']/h2//text()")))))
        awards_result[awardName] = list()
        awardList = awards.xpath('.//ul')
        for award in awardList:
            awards_result[awardName].append(
                ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), award.xpath('string(.)'))))))
        awards_result[awardName] = ';'.join(awards_result[awardName])
    result=[]
    for key,value in awards_result.items():
        result.append(key+":"+value)
    data['awards']=','.join(result)


def crawer_topic(id,data):
    topicUrl = 'https://m.douban.com/rexxar/api/v2/gallery/subject_feed?start=0&count=4&subject_id=%s&ck=null'%id
    headers['Referer'] = 'https://movie.douban.com/subject/26752088/'
    topicRes = openlink(id,topicUrl,data)
    topicData = topicRes.json()
    topic=[]
    for i in topicData['items']:
        topic.append(i['topic']['name']+":"+i['topic']['card_subtitle'])
    data['topics']='/'.join(topic)

if __name__ == '__main__':
    doubanqueue = MongoQueue('douban', 'url3')
    crawer_main()
