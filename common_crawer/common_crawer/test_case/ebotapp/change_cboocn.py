import pymongo

if __name__ == '__main__':
    cli=pymongo.MongoClient('localhost',27017)
    db=cli['ebotapp']
    document=db['cboocn2']
    num=20
    parts=int(document.count()/20)
    for j in range(12919,parts):
        for i in document.find().limit(20).skip(j*20):
           if '\n' in i['runTime']:
               i['runTime']=i['runTime'].replace('\n','')
               EnMovieID=i['EnMovieID']
               try:
                document.update({'EnMovieID': EnMovieID}, {'$set': dict(i)}, True)
               except Exception as e:
                   print("错误",EnMovieID)
               else:
                print('修改了的id: ',EnMovieID)
        print("--------第%s部分,共有%s部分"%(str(j),str(parts)))
