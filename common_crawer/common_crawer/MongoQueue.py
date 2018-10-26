from datetime import datetime, timedelta

from pymongo import MongoClient, errors


class MongoQueue():
    OUTSTANDING=1 # 初始状态
    PROCESSING=2 # 正在下载状态
    COMPLETE=3 # 下载完成状态
    ip='123.207.42.164'
    def __init__(self,db,collection,timeout=300):
        self.client=MongoClient(self.ip)
        self.client=self.client[db]
        self.db=self.client[collection]
        self.timeout=timeout

    def __bool__(self):
        record=self.db.find_one({'status':{'$ne':self.COMPLETE}})
        return True if record else False

    def push(self,id,url):
        try:
            self.db.insert({'id':id,'url':url,'status':self.OUTSTANDING})
            print(url,'插入队列成功')
        except errors.DuplicateKeyError as e:
            print(url,'已经存在于队列中')

    # def push_imgurl(self,title,url):
    #     try:
    #         self.db.insert({'id':title,'statue':self.OUTSTANDING,'url':url})
    #         print("图漂地址插入成功")
    #     except errors.DuplicateKeyError as e:
    #         print("地址已经存在了")

    def pop(self):
        record=self.db.find_and_modify(query={'status':self.OUTSTANDING},
                                       update={'$set':{'status':self.PROCESSING,'timestamp':datetime.now()}})
        datetime.now()
        if record:
            return [record['id'],record['url']]
        else:
            self.repair()
            raise KeyError

    def pop_title(self,url):
        record=self.db.find_one({'url':url})
        return record['主题']

    def peek(self):
        record=self.db.find_one({'statis':self.OUTSTANDING})
        if record:
            return record['id']

    def complete(self,url):
        self.db.update({"url":url},{'$set':{'status':self.COMPLETE}})

    def repair(self):
        record=self.db.find_and_modify(query={'timestamp':{"$lt":datetime.now()-timedelta(seconds=self.timeout)},'status':{"$ne":self.COMPLETE},},update={'$set':{'status':self.OUTSTANDING}})
        if record:
            print("重置url",record['url'])
    def clear(self):
        self.db.drop()

if __name__ == '__main__':
    queue=MongoQueue('maoyan','actorurl')
    for i in range(55591,1000000):
        url='http://maoyan.com/films/celebrity/%s'
        queue.push(i,url%str(i))




