import time
from multiprocessing.pool import Pool
import chardet
import os
import pandas as pd
import pymysql
import requests
from lxml import etree
from multiprocessing import Value, Manager, Lock

from pyquery import PyQuery
from requests import ConnectTimeout
from requests.exceptions import ProxyError

#1222 06:00
# TODO(ximingren) 优化代码
# TODO(ximingren) 代理地址速度很慢,改善代理地址
# TODO(ximingren) 怎么把warning去掉
# TODO(ximingren) 要爬取的数据不用文件读取，而是直接读取
# TODO(ximingren) 'utf-8' codec can't decode byte 0xed in position 1567: invalid continuation byte
# TODO(ximingren) ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))
# TODO(ximingren)Invalid URL '': No schema supplied. Perhaps you meant http://?
# b''
# list index out of range
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
    sql = 'INSERT INTO {table} ({keys}) values ({values})'.format(table=mysql_table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(data.values())):
            print("插入%s表数据成功" % (mysql_table), str(data))
            mysql_db.commit()
    except Exception as e:
        print("插入%s数据发生异常 " % (mysql_table), e, data)
        mysql_db.rollback()


def get_one_link(mysql_table, id, cursor):
    try:
        sql = 'SELECT company_url FROM {table} WHERE city ="{city}" and id={id}'. \
            format(table=mysql_table, city='guangzhou', id=id)
        cursor.execute(sql)
        row = cursor.fetchone()[0]
        return row
    except Exception as e:
        print("获取链接时发生异常", e)


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
    get_proxy_condition = True
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
                get_proxy_condition = False
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
    while True:
        try:
            # proxies = change_proxy()  # 获取代理地址
            print("进程%s爬取页面为 %s" % (os.getpid(),url))
            re = requests.get(url, headers=headers, proxies={'http': 'http://127.0.0.1:8082'})  # 使用代理爬取
            re.encoding = chardet.detect(re.content)['encoding']  # 设置编码
            print("进程%s是否访问页面成功  %s" % (os.getpid(),str(re.ok)))
            if (not re.ok) or len(re.content) < 800:
                raise ConnectionError
            else:
                return re.content
        except ConnectionError:
            print('进程%s连接失败'%os.getpid())
        except Exception as e:
            print("进程%s爬取页面时发生异常" %(os.getpid()),e)


def get_contact_way(content, link):
    """
    解析网页得到公司的联系方式
    :param content:
    :param style:
    :return:
    """
    try:
        tree = etree.HTML(content.decode('utf8'))
        data = {}
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
        data['url'] = link
        insert_info(mysql_db, 'shunqiwang_contact_way', data)
    except Exception as e:
        print("进程%s解析内容联系方式时发生异常"%os.getpid(), e)


def get_business_info(content, link):
    """
    解析网页得到公司的联系方式
    :param content:
    :param style:
    :return:
    """
    try:
        tree = etree.HTML(content.decode('utf8'))
        data = {}
        info = tree.xpath('.//table[@class="codl"]//td/text()')
        company_name = tree.xpath('.//div[@id="nav"]//text()')
        del_rn(company_name)
        del_rn(info)
        company_name = company_name[-2]
        data['company_name'] = company_name
        for e in info:
            if '主要经营产品' in e:
                if '经营范围：' in info:
                    products = info[info.index(e) + 1:info.index('经营范围：')]
                else:
                    products = info[info.index(e) + 1:info.index(e) + 5]  # 这个还没办法解决
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
            data['url'] = link
        insert_info(mysql_db, 'shunqiwang_business_info', data)
    except Exception as e:
        print("进程%s解析式内容公司信息时发生异常"%(os.getpid()), e)


def craw_main(share_dict,rowcount):
    """
    爬取页面的主程序
    :param x:
    :return:
    """
    try:
        for x in range(rowcount):
            link = get_one_link('shunqiwang', share_dict['common_id'], cursor)
            headers['Host'] = "www.11467.com"
            content = craw_text(link)  # 获取文本，以代理的模式
            # 接下来对文本进行解析处理,函数返回的结果是每一个页面解析后的结果
            if content:
                if share_dict['common_id']!=id:
                    print("进程%s正在进行解析页面得到联系方式" % os.getpid())
                    get_contact_way(content, link)
                    print("进程%s正在进行解析页面得到公司内容" % os.getpid())
                    get_business_info(content, link)
            lock.acquire()
            share_dict['common_id'] = share_dict['common_id'] + 1
            lock.release()
    except Exception as e:
        print(e)

def get_shunqiwang_list(url, city, area, headers, page=1, link_num=0):
    link = url % (city, area) + str(page)
    try:
        response = requests.get(link, headers, proxies={'http': "http://127.0.0.1:8082"})
        doc = PyQuery(response.text)
        print("正在爬取页面 %s" % link)
        if page == 1:
            global total_page
            total_page = doc('.pages a:last-child').attr('href')
            total_page = total_page[total_page.index('pn') + 2:]
        if page <= int(total_page):
            company_element = doc('.companylist .f_l h4 a')
            for company in company_element.items():
                link_num += 1
                company_name = company.text()
                company_url = "http://" + company.attr('href')[2:]
                result = {'city': city,
                          'area': area,
                          'company_name': company_name,
                          'company_url': company_url}
                insert_info(mysql_db, 'shunqiwang', result)
        else:
            return [link_num]
    except Exception as e:
        print("正在爬取页面 %s 发生异常" % link)
    else:
        page = page + 1
        get_shunqiwang_list(url, city, area, headers, page, link_num)

def init(l):
    global lock
    lock=l
if __name__ == '__main__':
    pd.set_option('display.width', 200)
    citys = ['dongcheng', 'xicheng', 'chongwen', 'chaoyang', 'fengtai', 'haiding', 'tongzhou']
    headers = {  # User-Agent需要根据每个人的电脑来修改，每个人的信息是不同的
        'Accept': '*/*',
        'Accept-Encoding': 'br',
        'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'beijing.11467.com',
        'Referer': "",
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
        'Cookie': "Hm_lvt_819e30d55b0d1cf6f2c4563aa3c36208=1534830939,1535094885,1535107534; Hm_lpvt_819e30d55b0d1cf6f2c4563aa3c36208=1535128502"
    }
    # 获取需要爬取的链接
    url = 'http://%s.11467.com/%s/pn'
    city = 'guangzhou'
    area = 'liwan'
    mysql_db = pymysql.connect(host='172.17.0.5', port=3306, user='root', passwd='923162', db='spiders')  # 创建数据库连接
    # get_shunqiwang_list(url,city,area,headers)
    cursor = mysql_db.cursor()
    sql = 'SELECT id  FROM {table} WHERE city ="{city}"'.format(table='shunqiwang', city='guangzhou')
    cursor.execute(sql)
    rowcount = cursor.rowcount
    print("总共有%d个链接" % rowcount)
    id = cursor.fetchone()[0]
    # common_id=Value('i',id)
    lock=Lock()
    share_dict=Manager().dict()
    share_dict['common_id'] = id
    pool = Pool(initializer=init,initargs=(lock,))
    try:
        for x in range(4):
            if x<3:
                pool.apply_async(craw_main,args=(share_dict,int(rowcount/4.0)))  # 用进程池的形式实现多进程
            if x==3:
                pool.apply_async(craw_main, args=(share_dict,rowcount-(int(rowcount/4.0))*3-1))  # 用进程池的形式实现多进程
        pool.close()
        pool.join()
        mysql_db.close()  # 关闭数据库连接
    except Exception as e:
        print(e)