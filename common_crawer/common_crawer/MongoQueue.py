from datetime import datetime, timedelta

import requests
from pymongo import MongoClient, errors


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

    def pop_title(self, url):
        record = self.db.find_one({'url': url})
        return record['主题']

    def peek(self):
        record = self.db.find_one({'statis': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        self.db.update({"url": url}, {'$set': {'status': self.COMPLETE}})

    def completeId(self, id):
        self.db.update({"_id": id}, {'$set': {'status': self.COMPLETE}})
        print('id为%s的已完成'%id)

    def errorId(self, id):
        self.db.update({"_id": id}, {'$set': {'status': self.ERROR}})
        print('url设置错误成功',id)

    def repair(self):
        record = self.db.find_and_modify(query={'timestamp': {"$lt": datetime.now() - timedelta(seconds=self.timeout)},
                                                'status': {"$ne": self.COMPLETE}, },
                                         update={'$set': {'status': self.OUTSTANDING}})
        if record:
            print("重置id", record['id'])

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


if __name__ == '__main__':
    # cli=MongoClient('123.207.42.164')
    # db=cli['douban']
    # document=db['url']
    # parts = int(document.count() / 20)
    # maoyan=db['maoyan11']
    # num = 20
    # againurl  9539
    doubanqueue = MongoQueue('douban', 'url3')
    genresList = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '犯罪', '同性', '音乐', '歌舞', '传记', '历史', '战争', '西部',
                  '奇幻', '冒险', '灾难', '武侠', '情色']
    # while (1):
    #     try:
    #         doubanqueue.repair()
    #     except:
    #         break
    for genres in genresList:
        for i in range(500):
            start=i*20
            print(genres,start)
            url="https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=%s&genres=%s"%(start,genres)
            res=requests.get(url)
            dataList = res.json()
            for x in dataList['data']:
                data = {}
                id = x['id']
                url = x['url']
                star = x['star']
                doubanqueue.push(id,url,star)
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
