import json
import random
import re
import time
from datetime import datetime, timedelta

import requests
from lxml import etree
from pymongo import MongoClient, errors

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'text/html;charset=UTF-8',
    'Cache-Control': 'no-cache',
}


class MongoQueue():
    OUTSTANDING = 1  # 初始状态
    PROCESSING = 2  # 正在下载状态
    COMPLETE = 3  # 下载完成状态
    ERROR = 4  # url错误
    ip = '123.207.42.164'

    def __init__(self, db, collection, timeout=300):
        self.client = MongoClient(self.ip)
        self.client = self.client[db]
        self.db = self.client[collection]
        self.timeout = timeout

    def __bool__(self):
        record = self.db.find_one({'status': {'$ne': self.COMPLETE}})
        return True if record else False

    def push(self, id, url, star=None):
        try:
            self.db.insert({'_id': id, 'star': star, 'url': url, 'status': self.OUTSTANDING})
            print(id, url, '插入队列成功')
        except errors.DuplicateKeyError as e:
            print(id, url, '已经存在于队列中')

    def pushId(self, id):
        try:
            self.db.insert({'_id': id, 'status': self.OUTSTANDING})
            print(id, '插入队列成功')
        except errors.DuplicateKeyError as e:
            print(id, '已经存在于队列中')

    def pushProxy(self,proxy,startTime):
        try:
            self.db.insert({'proxy': proxy, 'timestamp':startTime, 'status': self.OUTSTANDING})
            print(proxy, '插入队列成功')
        except errors.DuplicateKeyError as e:
            print(proxy, '已经存在于队列中')

    # def push_imgurl(self,title,url):
    #     try:
    #         self.db.insert({'id':title,'statue':self.OUTSTANDING,'url':url})
    #         print("图漂地址插入成功")
    #     except errors.DuplicateKeyError as e:
    #         print("地址已经存在了")

    def pop(self):
        record = self.db.find_and_modify(query={'status': self.OUTSTANDING},
                                         update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}})
        datetime.now()
        if record:
            return record['_id'], record['url'], record['star']
        else:
            self.repair()
            raise KeyError
    def popId(self):
        record = self.db.find_and_modify(query={'status': self.OUTSTANDING},
                                         update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}})
        datetime.now()
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def pop_title(self, url):
        record = self.db.find_one({'url': url})
        return record['主题']

    def peek(self):
        record = self.db.find_one({'statis': self.OUTSTANDING})
        if record:
            return record['_id']

    def popProxy(self):
        record = self.db.find_one({'status': self.OUTSTANDING})
        if record:
            return record['proxy']
        else:
            self.repairProxy()
            raise KeyError

    def complete(self, url):
        self.db.update({"url": url}, {'$set': {'status': self.COMPLETE}})

    def completeId(self, id):
        self.db.update({"_id": id}, {'$set': {'status': self.COMPLETE}})
        print('id为%s的已完成' % id)

    def errorId(self, id):
        self.db.update({"_id": id}, {'$set': {'status': self.ERROR}})
        print('url设置错误成功', id)

    def repair(self):
        record = self.db.find_and_modify(query={'timestamp': {"$lt": datetime.now() - timedelta(seconds=self.timeout)},
                                                'status': {"$ne": self.COMPLETE}, },
                                         update={'$set': {'status': self.OUTSTANDING}})
        if record:
            print("重置id", record['id'])

    def repairProxy(self):
        record = self.db.find_and_modify(query={'timestamp': {"$lt": datetime.now() - timedelta(seconds=180)},
                                                'status': {"$ne": self.ERROR}, },
                                         update={'$set': {'status': self.ERROR}})
        if record:
            print("失效proxy", record['proxy'])

    def clear(self):
        self.db.drop()


def crawl_url():
    indexqueue = MongoQueue('maoyan', 'indexurl')
    honorqueue = MongoQueue('maoyan', 'honorurl')
    trailersqueue = MongoQueue('maoyan', 'trailersurl')
    weiboqueue = MongoQueue('maoyan', 'weibourl')
    wechatqueue = MongoQueue('maoyan', 'wechaturl')
    baiduqueue = MongoQueue('maoyan', 'baiduurl')
    celebrityqueue = MongoQueue('maoyan', 'celebrityurl')
    actorqueue = MongoQueue('maoyan', 'actorurl')
    for i in range(55555, 1000000):
        index_url = "https://piaofang.maoyan.com/movie/%s"
        honor_url = 'http://m.maoyan.com/movie/%s/honor'
        trailer_url = "https://piaofang.maoyan.com/movie/%s/promption-ajax?method=change&type=trailers&typeId=0&date=2018-10-10__2018-10-24"
        weibo_url = "https://piaofang.maoyan.com/movie/%s/promption-ajax?method=change&type=weibo&startDate=2018-10-10&endDate=2018-10-24"
        wechat_url = "https://piaofang.maoyan.com/movie/%s/promption-ajax?type=wechat&method=changeAccountChart&startDate=2018-10-10&endDate=2018-10-23"
        baidu_url = "https://piaofang.maoyan.com/movie/%s/promption-ajax?method=getIndex&type=baidu&startDate=2018-10-10&endDate=2018-10-23"
        celebrity_url = "https://piaofang.maoyan.com/movie/%s/celebritylist"
        actor_url = 'http://maoyan.com/films/celebrity/%s'
        # indexqueue.push(i,index_url%str(i))
        # honorqueue.push(i,honor_url%str(i))
        # trailersqueue.push(i,trailer_url%str(i))
        # weiboqueue.push(i,weibo_url%str(i))
        # wechatqueue.push(i,wechat_url%str(i))
        # baiduqueue.push(i,baidu_url%str(i))
        # celebrityqueue.push(i,actor_url%str(i))
        actorqueue.push(i, actor_url % str(i))


def maoyan():
    maoyanqueue = MongoQueue('maoyan', 'filmUlr')
    for i in range(19,26):
        catId=i
        for x in range(2,19):
            sourceId=x
            for y in range(13,1,-1):
                yearId=y
                for j in range(40):
                    offset=j*50
                    url = 'http://maoyan.com/films?showType=3&catId=%s&sourceId=%s&yearId=%s&offset=%s' % (str(catId), str(sourceId),str(yearId),str(offset))
                    print(url)
                    headers['Host'] = 'maoyan.com'
                    headers['Referer'] = 'www.baidu.com'
                    headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
                    res = requests.get(url, headers=headers)
                    tree = etree.HTML(res.text)
                    list = tree.xpath('//*[@id="app"]/div/div[2]/div[2]/dl//dd')
                    for item in list:
                        rawUrl = item.xpath('./div/a/@href')[0]
                        id = ''.join(re.findall("\d+\.?\d*", rawUrl))
                        id = ''.join(re.findall("\d+\.?\d*", rawUrl))
                        maoyanqueue.pushId(id)

def get_ip2():
    # IPProxy
    print('代理池2')
    r = requests.get('http://127.0.0.1:8000/?types=0&count=5&country=%E5%9B%BD%E5%86%85&protocol=1')
    ip_ports = json.loads(r.text)
    ip = random.choice(ip_ports)[0]
    port = random.choice(ip_ports)[1]
    proxies = {
        'https': 'https://%s:%s' % (ip, port),
        # 'http': 'http://%s:%s' % (ip, port)
    }
    return proxies

def proxy():
    q=MongoQueue('proxy','zhima')
    res = requests.get(
        'https://proxy.horocn.com/api/proxies?order_id=OEVL1617883042576364&num=20&format=json&line_separator=win')
    for x in res.json():
        q.pushProxy({
            'http': 'http://%s:%s' % (x['host'], x['port']),
        },datetime.now())
def repair1():
    q = MongoQueue('proxy', 'zhima')
    q.repairProxy()
def pushDouban():
    doubanqueue = MongoQueue('douban', 'url3')
    genresList = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '犯罪', '同性', '音乐', '歌舞', '传记', '历史', '战争', '西部',
                  '奇幻', '冒险', '灾难', '武侠', '情色']
    tages=['电视剧','综艺','动漫','纪录片','短片']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Host': 'movie.douban.com',
        'Pragma': 'no-cache',
        'Referer': 'www.baidu.com'
    }
    years=['2018,2018','2017,2017','2010,2019','2000,2009','1990,1999','1980,1989','1970,1979','1960,1969','1,1959']
    countries=['中国大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']
    while (1):
        try:
            doubanqueue.repair()
        except:
            break
    for genres in genresList[11:]:
            for country in countries:
                for year in years:
                    for i in range(8):
                        start=i*40
                        print(genres,start)
                        url="https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=%s&genres=%s&countries=%s&year_range=%s"%(start,genres,country,year)
                        print(url)
                        time.sleep(2)
                        res=requests.get(url,headers=headers)
                        print(res)
                        dataList = res.json()
                        for x in dataList['data']:
                            id = x['id']
                            url = x['url']
                            star = x['star']
                            doubanqueue.push(id,url,star)
if __name__ == '__main__':
    pushDouban()
    # while(1):
    #     proxy()
    #     time.sleep(10)
    # maoyan()
    # cli=MongoClient('123.207.42.164')
    # db=cli['douban']
    # document=db['url3']
    # parts = int(document.count() / 20)
    # maoyan=db['maoyan11']
    # num = 20
    # againurl  9539

    # parts = int(maoyan.count() / 20)
    # for j in range(1,780):
    #     for i in document.find().limit(20).skip(j * 20):
    #         doubanqueue.push(i['id'],i['url'],i['star'])
    # print(i)
    # print(i['rating_num'],i['aiqiyiList'],i['everydayReadNum'])
    # if i['rating_num']!='':
    # self.db.insert({'id': id, 'url': url, 'status': self.OUTSTANDING})
    # try:
    #     againqueue.push(str(i['id']))
    # document1.insert({'_id':str(i['id']),'status': 1})
    # except Exception as e:
    #     print(e)
    # else:
    #     print('添加了的id: ', i['id'],i['rating_num'])
    # print("--------第%s部分,共有%s部分" % (str(j), str(parts)))
