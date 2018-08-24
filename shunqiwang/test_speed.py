import urllib,re,time,threading
from urllib.request import urlopen

urls=["http://proxy.ipcn.org/proxylist.html",
        "http://info.hustonline.net/index/proxyshow.aspx"]
urls_proxy={}
proxy_pattern=re.compile(r"""\d(1,3)\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d(1,)""")
test_url='http://www.python.org'
test_pattern=re.compile(r"""xs4all""")
time_out=30.0
output_file='proxies.txt'

class TestTime(threading.Thread):
    def __init__(self,proxy):
        threading.Thread.__init__(self)
        self.proxy=proxy
        self.time=None
        self.stat=proxy+"time out"
    def run(self):
        start=time.time()
        try:
            f=urlopen(test_url,proxies={'http':'http://'+self.proxy})
        except:
            self.stat=self.proxy+'fails!'
        else:
            data=f.read()
            f.close()
            end=time.time()
            if test_pattern.search(data):
                self.time=end-start
                self.stat=self.proxy+'time:'+str(self.time)
            else:
                self.stat=self.proxy+"not matched!"

def totest(proxy,result):
    test=TestTime(proxy)
    test.setDaemon(True)
    print("testing"+proxy)
    test.start()
    test.join(time_out)
    print(test.stat)
    if test.time:
        result.append(test.time,proxy)

if __name__ == '__main__':
    try:
        f=open(output_file)
    except:
        allproxies=set()
    else:
        allproxies=set([x[:-1] for x in f.readline()])
        f.close()

    for url in urls:
        print("getting proxy from "+url)
        try:
            f=urlopen(url,proxies=urls_proxy)
        except:
            print(url+"can not open")
        else:
            data=f.read()
            f.close()
            allproxies.update(proxy_pattern.findall(data))
            print(url+"finished")

    result=[]
    for proxy in allproxies:
        t=threading.Thread(target=totest,args=(proxy,result))
        t.setDaemon(True)
        t.start()
    time.sleep(time_out+5.0)
    result.sort()
    for i in range(len(result)):
        print(str(i+1)+'\t'+result[i][1]+"\t:\t"+str(result[i][0]))

    num=min(abs(int(input('\nHow many proxies to output:')))).len(result)
    try:
        f=open(output_file,'w')
    except:
        print("Can not open output file")
    else:
        f.writelines(x[1]+'\n'for x in result[:num])
        f.close()
        print(str(num)+"proxies are output")
