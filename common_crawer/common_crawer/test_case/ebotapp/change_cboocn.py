import os
from multiprocessing.pool import Pool

import pymongo
import requests


def insert_actor():
    cli = pymongo.MongoClient('localhost', 27017)
    cli2 = pymongo.MongoClient('123.207.42.164', 27017)
    db = cli['zoopla']
    db2 = cli2['maoyan']
    document1 = db['actor']
    document2 = db2['actor']
    num = 20
    parts = int(document1.count() / 20)
    for j in range(1, parts):
        for i in document1.find().limit(20).skip(j * 20):
            try:
                document2.insert(i)
            except Exception as e:
                print("错误", i)
            else:
                print('修改了的id: ', i)
        print("--------第%s部分,共有%s部分" % (str(j), str(parts)))


def insert_actorBox(i):
        print(os.getpid())
        try:
            actoridList = i['演员id'].split(';')
        except KeyError as e:
            print('没有key', e)
        else:
            actorsumBoxList = []
            for actorid in actoridList:
                data = actor.find_one({'id': actorid})
                if data:
                    try:
                        sumBox = data['sumBox']
                        if 'name' in data.keys():
                            name = data['name']
                        else:
                            name=data['engName']
                    except KeyError as e:
                        if 'name' in data.keys():
                            name = data['name']
                        else:
                            if 'engName' in data:
                                name=data['engName']
                            else:
                                name=''
                        actorsumBoxList.append(name + ":" + " ")
                    else:
                        actorsumBoxList.append(name + ":" + sumBox)
            try:
                film.update({'id': i['id']}, {'$set': {'演员票房': ';'.join(actorsumBoxList)}},True)
            except Exception as e:
                print(e, i['id'])
            else:
                print('更新成功%s' % i['id'])


def insert_directorBox(i):
        print(os.getpid())
        try:
            directoridList = i['导演id'].split(';')
        except KeyError as e:
            print('没有key', e)
        else:
            directorsumBoxList = []
            for directorid in directoridList:
                data = actor.find_one({'id': directorid})
                if data:
                    try:
                        sumBox = data['sumBox']
                        if 'name' in data.keys():
                            name = data['name']
                        else:
                            name=data['engName']
                    except KeyError as e:
                        if 'name' in data.keys():
                            name = data['name']
                        else:
                            if 'engName' in data:
                                name=data['engName']
                            else:
                                name=''
                        directorsumBoxList.append(name + ":" + "")
                    else:
                        directorsumBoxList.append(name + ":" + sumBox)
            try:
                film.update({'id': i['id']}, {'$set': {'导演票房': ';'.join(directorsumBoxList)}},True)
            except Exception as e:
                print(e, i['id'])
            else:
                print('更新成功%s' % i['id'])


if __name__ == '__main__':
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
    res=requests.get("https://archello.com/project/block-house-stoke-newington",proxies=proxies)
    print(res)

    # cli = pymongo.MongoClient('123.207.42.164', 27017)
    # actor = cli['maoyan']['actor']
    # film = cli['maoyan']['maoyan11']
    # parts = int(film.count() / 20)
    # p=Pool(16)
    # print('主进程',os.getpid())
    # for j in range(6871,parts):
    #     print("--------第%s部分,共有%s部分" % (str(j), str(parts)))
    #         # p.apply(insert_directorBox,args=(i,))
    #         # p.apply(insert_actorBox,args=(i,))
    #     p.map(insert_actorBox,film.find().limit(20).skip(j * 20))
    #     p.map(insert_directorBox,film.find().limit(20).skip(j * 20))
    #         # insert_actorBox(i)
    #         # insert_directorBox(i)
    # p.close()
    # p.join()