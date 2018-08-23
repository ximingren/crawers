from multiprocessing.pool import Pool
import chardet
import os
import pandas as pd
import pymysql
import requests
from lxml import etree
from multiprocessing import Manager, Value
from requests import ConnectTimeout
from requests.exceptions import ProxyError


# TODO(ximingren) 优化代码
# TODO(ximingren) 代理地址速度很慢,改善代理地址
# TODO(ximingren) 怎么把warning去掉
# TODO(ximingren) 要爬取的数据不用文件读取，而是直接读取
# TODO(ximingren) 'utf-8' codec can't decode byte 0xed in position 1567: invalid continuation byte
# TODO(ximingren) ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))
# TODO(ximingren)Invalid URL '': No schema supplied. Perhaps you meant http://?

i=0
def insert_info(mysql_db, mysql_table, data):
    """
    插入数据
    :param mysql_db:
    :param mysql_table:
    :param data:
    :return:
    """
    keys = ','.join(data.keys())
    values = ','.join(['%s'] * len(data))
    cursor = mysql_db.cursor()
    sql = 'INSERT INTO {table} ({keys}) values ({values})'.format(table=mysql_table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(data.values())):
            print("插入%s表数据成功" % (mysql_table), str(data))
            mysql_db.commit()
    except Exception as e:
        print("插入%s数据发生异常 " % (mysql_table), e, data)
        mysql_db.rollback()


def del_rn(need_del_list):
    """
    删除列表中含有\r\n中的元素
    :param need_del_list:
    :return:
    """
    try:
        for e in list(need_del_list):
            if '\r\n' in e:
                del need_del_list[need_del_list.index(e)]
    except Exception as e:
        print("删除\r\n的元素失败", e)


def get_proxy():
    """
    得到代理地址
    :return:
    """
    try:
        count = 1
        response = requests.get("http://127.0.0.1:12345/api/proxy/?scheme=HTTP&count=" + str(count))
        content = response.json()
        if content['msg'] == 'success':
            for x in range(count):
                proxy_dict = {}
                scheme = content['data']['detail'][x]['scheme']
                proxy_dict[scheme] = content['data']['detail'][x]['url']
                # print("进程%d获取到的代理库为%s"%(os.getpid(),str(proxy_dict)))
                return proxy_dict
    except Exception as e:
        print("获得代理地址失败", e)


def change_proxy():
    """
    改变代理地址
    :return:
    """
    global i
    proxies = 0
    get_proxy_condition=True
    while get_proxy_condition:
        try:
            proxies = get_proxy()
            r = requests.get(url="http://www.ip111.cn/", proxies=proxies, timeout=15)
            if r.ok:
                status = etree.HTML(r.content.decode('utf8')).xpath(
                    '//table[@class= "table table-bordered"]//tr[position()=2]//text()')
                if not status:
                    raise ConnectionError
                print("进程%d  第%d条代理地址%s进行测试成功!" % (os.getpid(), i, str(proxies)))
                get_proxy_condition=False
                return proxies
        except ConnectTimeout:
            print("进程%d 测试第%d条代理地址%s时连接超时" % (os.getpid(), i, proxies))
            i += 1
        except ProxyError:
            print("进程%d 测试第%d条代理地址%s时代理错误" % (os.getpid(), i, proxies))
            i += 1


def craw_text(url):
    """
    爬取文本的主程序
    :param url: 爬取的url
    :return:
    """
    global i
    while True:
        try:
            proxies = change_proxy()  # 获取代理地址
            print("进程%d正在使用第%d个代理,代理地址为%s  爬取页面为 %s" % (os.getpid(), i, proxies, url))
            re = requests.get(url, headers=headers, proxies=proxies)  # 使用代理爬取
            re.encoding = chardet.detect(re.content)['encoding']  # 设置编码
            print("进程%d是否访问页面成功  %s" % (os.getpid(), str(re.ok)))
            if (not re.ok) or len(re.content) < 500:
                raise ConnectionError
            else:
                return re.content
        except Exception as e:
            print("进程%d爬取页面时发生异常" % (os.getpid()), e)


def get_contact_way(content, style,link):
    """
    解析网页得到公司的联系方式
    :param content:
    :param style:
    :return:
    """
    try:
        tree = etree.HTML(content.decode('utf8'))
        data = {}
        if style == 2:
            info = tree.xpath('.//ul[@class="codl"]//text()')
            company_name = tree.xpath('.//div[@id="nav"]//text()')
            del_rn(company_name)
            del_rn(info)
            data['company_name'] = company_name[-2]
            for e in info:
                if '地址' in e:
                    address = e[3:]
                    data['address'] = address
                if '固定电话' in e:
                    fixed_phone = e[3:]
                    data['fixed_phone'] = fixed_phone
                if '经理' in e:
                    manager = e[3:]
                    data['manager'] = manager
                if '手机' in e:
                    manager_phone = e[3:]
                    data['manager_phone'] = manager_phone
                if "mail" in e:
                    email = e[5:]
                    data['email'] = email
                if '邮编' in e:
                    postal_code = e[3:]
                    data['postal_code'] = postal_code
                if '传真' in e:
                    fax_number = e[3:]
                    data['fax_number'] = fax_number
        if style == 1:
            info = tree.xpath('.//dl[@class="codl"]//text()')
            company_name = tree.xpath('.//div[@id="nav"]//text()')
            del_rn(company_name)
            del_rn(info)
            data['company_name'] = company_name[-2]
            for e in info:
                if '地址' in e:
                    address = info[info.index(e) + 1]
                    data['address'] = address
                if '固定电话' in e:
                    fixed_phone = info[info.index(e) + 1]
                    data['fixed_phone'] = fixed_phone
                if '经理' in e:
                    manager = info[info.index(e) + 1]
                    data['manager'] = manager
                if '手机' in e:
                    manager_phone = info[info.index(e) + 1]
                    data['manager_phone'] = manager_phone
                if "mail" in e:
                    email = info[info.index(e) + 1]
                    data['email'] = email
                if '邮编' in e:
                    postal_code = info[info.index(e) + 1]
                    data['postal_code'] = postal_code
                if '传真' in e:
                    fax_number = info[info.index(e) + 1]
                    data['fax_number'] = fax_number
        data['url']=link
        insert_info(mysql_db, 'shunqiwang_contact_way', data)
    except Exception as e:
        print("解析%d式内容联系方式时发生异常" % (style), e)


def get_business_info(content, style,link):
    """
    解析网页得到公司的联系方式
    :param content:
    :param style:
    :return:
    """
    try:
        tree = etree.HTML(content.decode('utf8'))
        data = {}
        info = company_name = None
        if style == 1:
            info = tree.xpath('.//table[@class="codl"]//td/text()')
            company_name = tree.xpath('.//div[@id="nav"]//text()')
            del_rn(company_name)
            del_rn(info)
            company_name = company_name[-2]
        if style == 2:
            info = tree.xpath('.//dl[@class="codl"]//text()')
            company_name = tree.xpath('.//div[@id="nav"]//text()')
            del_rn(company_name)
            del_rn(info)
            company_name = company_name[-2]
        del_rn(company_name)
        del_rn(info)
        data['company_name'] = company_name
        for e in info:
            if '主要经营产品' in e:
                if '经营范围：' in info:
                    products = info[info.index(e) + 1:info.index('经营范围：')]
                else:
                    products=info[info.index(e)+1:info.index(e)+5] # 这个还没办法解决
                products = ''.join(products)
                data['products'] = products
            if '经营范围' in e:
                business_scope = info[info.index(e) + 1]
                data['business_scope'] = business_scope
            if '营业执照号码' in e:
                license_number = info[info.index(e) + 1]
                data['license_number'] = license_number
            if '经营模式' in e:
                business_model = info[info.index(e) + 1]
                data['business_model'] = business_model
            if '成立时间' in e:
                established_time = info[info.index(e) + 1]
                if '-' not in established_time:
                    year = established_time[:4]
                    month = established_time[5:7]
                    day = established_time[8:10]
                    established_time = year + '-' + month + '-' + day
                data['established_time'] = established_time
            if '职员人数' in e:
                person_number = info[info.index(e) + 1][:-1]
                data['person_number'] = person_number
            if '注册资本' in e:
                registered_capital = info[info.index(e) + 1]
                data['registered_capital'] = registered_capital
            data['url']=link
        insert_info(mysql_db, 'shunqiwang_business_info', data)
    except Exception as e:
        print("解析%d式内容公司信息时发生异常" % (style), e)


def craw_main(link):
    """
    爬取页面的主程序
    :param x:
    :return:
    """
    style = 0  # 辨别不同的页面，采取的解析方式也是不同的。
    if "http:" in link:
        headers['Host'] = link[6:]
        link = "http://" + link[6:] + "/"
        style = 2
    if "htm" in link:
        link = "http://" + link.strip(" ")
        style = 1
        headers['Host'] = "www.11467.com"
    content = craw_text(link)  # 获取文本，以代理的模式
    # 接下来对文本进行解析处理,函数返回的结果是每一个页面解析后的结果
    if content:
        print("进程%d正在进行解析页面得到联系方式" % os.getpid())
        get_contact_way(content, style,link)
        print("进程%d正在进行解析页面得到公司内容" % os.getpid())
        get_business_info(content, style,link)


if __name__ == '__main__':
    pd.set_option('display.width', 200)
    citys = ['dongcheng', 'xicheng', 'chongwen', 'chaoyang', 'fengtai', 'haiding', 'tongzhou']
    headers = {  # User-Agent需要根据每个人的电脑来修改，每个人的信息是不同的
        'Accept': '*/*',
        'Accept-Encoding': 'br',
        'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.shunqiwang.com',
        'Referer': "",
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
        'Cookie': "Hm_lvt_819e30d55b0d1cf6f2c4563aa3c36208=1533379740; Hm_lpvt_819e30d55b0d1cf6f2c4563aa3c36208=1533380882"
    }
    # 获取需要爬取的链接
    with open('a.txt', 'r') as f:
        links = f.read()
    links = links.split(',')
    need_links = []
    for x in range(len(links)):
        need_links.append(links[x].replace("\'", "").replace("//", ""))
    # need_links = need_links[]  # 获取要爬取的链接
    mysql_db = pymysql.connect(user='ximingren', password='923162', db='spiders',
                               unix_socket="/var/run/mysqld/mysqld.sock")  # 创建数据库连接
    need_links=need_links[581:]
    pool = Pool()
    pool.map(craw_main, need_links)  # 用进程池的形式实现多进程
    mysql_db.close() # 关闭数据库连接
