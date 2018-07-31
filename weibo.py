# !/usr/bin/python
# -*- coding=utf-8 -*-
import socket
import urllib.parse
from multiprocessing.pool import Pool
from urllib.request import urlopen, Request
import pandas as pd
import re
import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
from numpy import long
import json

"""
    # 使用说明：基于python3.5
    # 执行参数分别为登陆帐号，登陆密码，是否用游览器引擎获取cookie（是的时候确保电脑有游览器引擎,并配置好相关信息）
    # 否的时候请自行登陆微博，手动获取cookie并存入文件.
    !!!由于微博的限制，现在爬虫只能爬前5页的粉丝列表以及关注列表，除非用其它方法!!!
"""

"""
    urlopen error 10060错误
"""
def openlink(url,headers):
    maxTryNum = 15
    for tries in range(maxTryNum):
        try:
            req = Request(url, headers=headers)
            response = urlopen(req)
            return response
        except:
            if tries < (maxTryNum - 1):
                continue
            else:
                print("尝试%d 次连接网址%s失败!"%( maxTryNum, url))

"""
    获取当前系统时间戳
"""


def get_timestamp():  # 获取当前系统时间戳
    try:
        tamp = time.time()
        timestamp = str(int(tamp)) + "000"
        return timestamp
    except Exception as e:
        print(e)
    finally:
        pass


"""
    登陆操作
"""


def login(username, password, driver_path):
    try:
        print("--------------------微博账号：" + username)
        print("--------------------微博密码：" + password)

        result = is_valid_cookie()  # 验证cookie是否失效了
        print("-------------------cookie是否有效：" + str(result))
        # 如果失效,或者第一次打开,则打开游览器进行实地登陆以记录cookie
        if result == False:
            print("-------------------------打开游览器")
            driver = webdriver.Chrome(driver_path)  # 打开Chrome
            driver.maximize_window()  # 将浏览器最大化显示
            driver.get(weibo_url)  # 打开微博登陆页面
            time.sleep(10)  # 加载页面需要时间，延时10s来确保页面已加载完毕
            print("-----------------------------登陆微博")
            cookie = login_weibo_get_cookies(driver)
            print("---------------------------保存cookie")
            save_cookie(cookie)  # 保存cookie到文件
            save_cookie_update_timestamp(get_timestamp())  # 同时保存当前时间戳,用于第二次访问验证所用
        else:
            cookie = get_cookie_from_txt()  # 如果没有失效,则从文本中读取cookie
        return cookie
    except Exception as e:
        print(e)


"""
    登陆获取cookie
"""


def login_weibo_get_cookies(driver):  # 登录获取cookies
    try:
        time.sleep(2)
        driver.find_element_by_name("username").send_keys(username)  ##输入用户名
        driver.find_element_by_name("password").send_keys(password)  ##输入密码
        driver.find_element_by_xpath("//a[@node-type='submitBtn']").click()  ##点击登录按钮
        cookies = driver.get_cookies()  ##获取cookies
        cookie = ""
        # 将返回的Cookies数组转成微博需要的cookie格式
        for x in range(len(cookies)):
            value = cookies[x]['name'] + "=" + cookies[x]['value'] + ";"
            cookie = cookie + value
        return cookie
    except Exception as e:
        print(e)


"""
    直接转化为cookie
"""


def direct_get_cookies(cookie_save_file):
    try:
        if os.path.exists(cookie_save_file):
            with open(cookie_save_file) as f:
                cookies = f.read()
                if cookies == " ":
                    print("-----------请将cookie正确输入到文件并保存")
                else:
                    save_cookie_update_timestamp(get_timestamp())  # 同时保存当前时间戳,用于第二次访问验证所用
                    return cookies
        else:
            print("----------请确保文件存在")
            return False
    except Exception as  e:
        print(e)
    finally:
        pass


"""
    把cookie存到本地
"""


def save_cookie(cookie):  # 把cookie存到本地
    try:
        with open(cookie_save_file, 'w') as f:
            f.write(cookie)
    except Exception as  e:
        print(e)
    finally:
        pass


"""
    从本地文件中读取cookie
"""


def get_cookie_from_txt():  # 从本地文件里读取cookie
    try:
        with open(cookie_save_file) as f:
            cookie = f.read()
            print("--------------------用户的cookie:\n" + cookie)
            return cookie
    except Exception as e:
        print(e)
    finally:
        pass


"""
    把cookie存储的时间戳存到本地
"""


def save_cookie_update_timestamp(timestamp):  # 把cookie存到本地
    try:
        with open(cookie_update_time_file, 'w') as f:
            f.write(timestamp)
            f.write('\n')
    except Exception as e:
        print(e)
    finally:
        pass


"""
    获取上一次cookie更新时间
"""


def get_cookie_update_time_from_txt():  # 获取上一次cookie更新时间
    try:
        with open(cookie_update_time_file) as f:
            lines = f.readlines()
            cookie_update_time = lines[0]
            print("----------------------获取上一次cookie更新时间:    " + str(cookie_update_time))
            return cookie_update_time
    except Exception as e:
        print(e)
    finally:
        pass

"""
    创建新目录(若不存在)
"""


def mkdir(path):
    try:
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
    except Exception as e:
        print(e)
    finally:
        pass


"""
    判断cookie是否有效
"""


def is_valid_cookie():  # 判断cookie是否有效
    try:
        # 如果连文件都不存在的话,那肯定时第一次访问,定为False使其进行第一次记录cookie
        if os.path.isfile(cookie_update_time_file) == False:
            return False
        else:
            with open(cookie_update_time_file) as f:

                lines = f.readlines()
                if len(lines) == 0:
                    return False  # 如果是空的,要重新记录cookie
                else:
                    last_time_stamp = get_cookie_update_time_from_txt()
                    # 如果时间大于六个小时,则要重新记录cookie了
                    if long(get_timestamp()) - long(last_time_stamp) > 6 * 60 * 60 * 1000:
                        return False
                    else:
                        return True
    except Exception as e:
        print(e)
    finally:
        pass


"""
    某些内容是藏在script里面的,解析script得到需要的html内容
    若不懂可以打印出最开始的html文本来看一下
"""


def analyse_html(soup, name):
    try:
        script_list = soup.find_all("script")  # 要抓取的内容在scirpt里面,首先先解析出script
        script_size = len(script_list)
        tag = 0
        for x in range(script_size):
            if name in str(script_list[x]):
                tag = x
        html_start = str(script_list[tag]).find("<div")  # 找到最前面的div标签
        html_end = str(script_list[tag]).rfind("div>")  # 找到最后面的div标签
        parser_html = str(str(script_list[tag])[html_start:html_end + 4])  # 找出需要的html文本
        result_html = parser_html.replace("\\", "")  # 处理成合适的规格
        result_soup = BeautifulSoup(result_html, "html.parser")  # 对处理后的html进二次解析
        return result_soup
    except Exception as e:
        print(e)


"""
    获取个人信息
"""


def get_info(name, headers):
    try:
        info_response = requests.get("https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D" + name+"&page_type=searchall")  # 微博搜索的页面url
        data = json.loads(info_response.text)
        condition=[]
        if  data['data']['cards']:
            search_size=len(data['data']['cards'][1]['card_group'])
            for k in range(search_size):
                if  data['data']['cards'] and data['data']['cards'][1]['card_group'][k]['user']['screen_name'] == name:
                        profile_url = data['data']['cards'][1]['card_group'][k]['user']['profile_url']
                        id = int(re.findall(r"/u/(\d.+)\?", profile_url)[0])
                        subs_size = data['data']['cards'][1]['card_group'][k]['user']['follow_count']
                        fans_size = data['data']['cards'][1]['card_group'][k]['user']['followers_count']
                        print("----------------%s的关注者数：%d   粉丝数%d"%(name,subs_size,fans_size))
                        if fans_size>20:
                            fans_page = int(round(fans_size / 20))  # 计算出粉丝列表的具体页数
                        elif fans_size!=0:
                            fans_page=1
                        else:
                            fans_page=0
                        if subs_size>20:
                            subs_page = int(round(subs_size / 20))  # 计算出关注列表的具体页数
                        elif subs_size!=0:
                            subs_page=1
                        else:
                            subs_page=0
                        condition=[subs_page,fans_size,id]
        if not condition:
            print("----------------------将失效昵称写入文件中,失效昵称:%s" % name)
            with open('failure.txt', 'a') as f:
                    f.write(name + "\n")
        return condition
    except Exception as e:
        print("------------发生异常", e)
    finally:
        pass


"""
    获取顶部微博文本
"""
def get_top_contents(weibo_id, name, headers,  page):
    try:
        headers['Referer'] = "https://weibo.com/p/100505" + weibo_id
        cont_url = "https://weibo.com/p/100505" + weibo_id + "?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page="+str(page)  # 拼凑成关注者列表的页面url
        weibo_div_size = 0
        count = 0
        # 因为有时会出现连接失败，返回的页面是空的，所以反复请求连接直到有页面为止
        while (weibo_div_size == 0):
            count = count + 1
            print("---------------请求连接到微博内容页面:%s" % cont_url)
            response = openlink(cont_url, headers)
            html = response.read().decode()  # 对调用接口后传过来的内容进行解码
            print("-----------------解析微博文本内容%d次" % count)
            cont_soup=BeautifulSoup(html,'html5lib')
            cont_soup = analyse_html(cont_soup, "pl.content.homeFeed.index")
            weibo_div = cont_soup.find_all('div', class_="WB_feed_detail clearfix")  # 找到所有的div内容框，返回的是结果集
            weibo_div_size = len(weibo_div)
            for k in range(weibo_div_size):
                text = weibo_div[k].find('div', attrs={"class": "WB_text W_f14", "node-type": "feed_list_content"})
                time_phone = weibo_div[k].find_all('a', attrs={"class": "S_txt2", 'target': "_blank"})
                if time_phone and text != None:
                    mkdir("./" + name)
                    with open("./" + name + '/CONTENTS.txt', 'a', encoding='utf-8') as f:
                        f.write("[" + time_phone[0].get_text() + "    " + time_phone[1].get_text() + "]")  # 写入时间和手机型号
                        f.write(text.get_text().strip("n") + "\n")  # 写入文本
            if count >= 3 and count <=5:
                    print("------------------连续解%d次失败，休眠10秒后再爬"%count)
                    time.sleep(10)
                # 这个是为了请求6页以后，微博限制用户访问列表，不再继续爬
            if count > 5:
                    print("-----------------------------解析%s页面第%d页微博文本页面失败!!!!" % (name, page))
                    break
        print("---------------休眠两秒后继续爬")
        time.sleep(2)
    except Exception as e:
        print("----------发生异常",e)
    finally:
        pass


"""
   利用接口调用获取文本
"""


def  get_contents(weibo_id, name, headers, pagebar, page,content_page):  # 通过微博ID和cookie来调取接口
    try:
        headers['Referer'] = "https://weibo.com/p/100505" + weibo_id
        weibo_div_size = 0
        count = 0
        # 因为有时会出现连接失败，返回的页面是空的，所以反复请求连接直到有页面为止
        while (weibo_div_size == 0):
            global page_div
            count = count + 1
            params = urllib.parse.urlencode(
                {'ajwvr': 6, 'domain': 100505, "profile_ftype": 1, 'is_all': 1, 'pagebar': pagebar,
                 "pl_name": "Pl_Official_MyProfileFeed__22", "id": "100505" + weibo_id,
                 "script_uri": "/p/" + "100505" + weibo_id,
                 'feed_type': 0, 'page': page + 1, 'pre_page': page + 1, 'domain_op': 100505,
                 '__rnd': get_timestamp()}).encode()  # 调用接口时所用的参数
            cont_url = api_url + "%s" % (params).decode()
            print("---------------请求连接到微博内容页面:%s" % cont_url)
            response=openlink(cont_url,headers)
            html = response.read().decode()  # 对调用接口后传过来的内容进行解码
            cont_html = json.loads(html)['data']
            print("-----------------解析微博文本内容%d次" % count)
            cont_soup = BeautifulSoup(cont_html, 'html.parser')  # 进行解析

            # 如钩没加载完则返回True,继续加载。如果加载完了返回False，不用接着加载了
            weibo_div = cont_soup.find_all('div', class_="WB_feed_detail clearfix")  # 找到所有的div内容框，返回的是结果集
            weibo_div_size = len(weibo_div)
            empty_flat = cont_soup.find_all('div', class_='WB_empty WB_empty_narrow')  # 加载完没内容了，会出现页码
            page_div=cont_soup.find_all('div',class_='W_pages')
            # 同时出现empty标签和微博内容div为空,或者出现页码条和没到最后一次滑动
            if (empty_flat and not weibo_div )or (page_div and (pagebar+1)!=2):
                print("---------------第%d页第%d次滑动没有内容"%(page+1,pagebar+1))
                break
            for k in range(weibo_div_size):
                text = weibo_div[k].find('div', attrs={"class": "WB_text W_f14", "node-type": "feed_list_content"})
                time_phone = weibo_div[k].find_all('a', attrs={"class": "S_txt2", 'target': "_blank"})
                if time_phone and text != None:
                    mkdir("./" + name)
                    with open("./" + name + '/CONTENTS.txt', 'a', encoding='utf-8') as f:
                        f.write("[" + time_phone[0].get_text() + "    " + time_phone[1].get_text() + "]")  # 写入时间和手机型号
                        f.write(text.get_text().strip(" ") + "\n")  # 写入文本
            if page + 1 != content_page and count >= 3 and count <= 5:
                print("------------------连续解析%d次失败，休眠15秒后再爬"%count)
                time.sleep(15)
            if page + 1 != content_page and count > 5:
                print("-----------------------------解析%s页面第%d页微博列表面失败!!!!" % (name, page + 1))
                break
            if page + 1 == content_page and count >= 3 and count <= 5:
                print("------------------连续解析最后一个页面%d次失败，休眠15秒后再爬"%count)
                time.sleep(15)
            if page + 1 == content_page and count > 5:
                print("------------------解析解析%s页面第最后一页微博列表面失败！！！" % (name))
                print("------------------这是最后一页")
                break

    except Exception as e:
        print(e)
    finally:
        pass


"""
    获取关注者的信息并写入文件
"""


def get_subs(weibo_id, name, headers, subs_list_page):  # 每一页顶部微博
    try:
        if subs_list_page > 5:
            subs_list_page = 5
        for page in range(0, subs_list_page):
            subs_url = "https://weibo.com/p/100505" + weibo_id + "/follow?page=" + str(page+1) + "#Pl_Official_HisRelation__59"  # 拼凑成关注者列表的页面url
            print("----------------爬取关注者列表的网址：\n" + subs_url)
            print("----------------请求连接到关注者列表页面")
            print("----------------正在爬取第%d页" % (page+1))
            subs_size = 0
            count = 0
            # 因为有时会出现连接失败，返回的页面是空的，所以反复请求连接直到有页面为止
            while (subs_size == 0):
                count = count + 1
                subs_response=openlink(subs_url,headers)
                subs_html = subs_response.read().decode()
                print("-----------------解析关注者html页面%d次" % count)
                subs_soup = BeautifulSoup(subs_html, 'html5lib')
                subs_soup = analyse_html(subs_soup,"pl.content.followTab.index")
                mkdir("./" + name)  # 创建目录(若不存在)
                # 写入文件
                with open("./" + name + '/SUB.txt', 'a', encoding='utf-8') as f:
                    subs_list = subs_soup.find_all('a', attrs={"class": "S_txt1", "target": "_blank"})
                    subs_size = len(subs_list)
                    for x in range(subs_size):
                        if subs_list[x].string is not None:
                            f.write("[" + str(subs_list[x].string) + "]")  # 关注者的昵称
                            f.write(str(subs_list[x].get('href')) + "\n")  # 关注者连接
                        else:
                            f.write("[" + "  " + "]")  # 关注者的昵称
                            f.write(str(subs_list[x].get('href')) + "\n")  # 关注者连接
                if count >= 3 and count <=5:
                    print("------------------连续解%d次失败，休眠10秒后再爬"%count)
                    time.sleep(10)
                # 这个是为了请求6页以后，微博限制用户访问列表，不再继续爬
                if count > 5:
                    print("-----------------------------解析%s页面第%d页关注列表页面失败!!!!" % (name, page+1))
                    break
            print("---------------休眠两秒后继续爬下一页")
            time.sleep(2)
    except Exception as e:
        print("------------发生异常", e)
    finally:
        pass


"""
    获取粉丝的信息
"""


def get_fans(weibo_id, name, headers, fans_list_page):  # 每一页顶部微博
    try:
        if fans_list_page > 5:
            fans_list_page = 5
        for page in range(0, fans_list_page):
            fans_url = "https://weibo.com/p/100505" + weibo_id + "/follow?relate=fans&page=" + str(
                page+1) + "#Pl_Official_HisRelation__59"  # 拼凑粉丝列表url
            print("---------------------爬取粉丝列表的网址：\n" + fans_url)
            print("---------------------请求连接到粉丝列表页面")
            print("----------------正在爬取第%d页" % (page+1))
            fans_size = 0
            count = 0
            # 因为有时会出现连接失败，返回的页面是空的，所以反复请求连接直到有页面为止
            while (fans_size == 0):
                count = count + 1
                fans_response=openlink(fans_url,headers)
                fans_html = fans_response.read().decode()
                print("-----------------------解析粉丝列表html页面%d次" % count)
                fans_soup = BeautifulSoup(fans_html, 'html5lib')
                fans_soup = analyse_html(fans_soup, "pl.content.followTab.index")  # 获取处理过的html
                mkdir("./" + name)
                with open("./" + name + '/FANS.txt', 'a', encoding='utf-8') as f:
                    fan_list = fans_soup.find_all('a', attrs={"class": "S_txt1", "target": "_blank"})
                    fans_size = len(fan_list)
                    for x in range(fans_size):
                        if  fan_list[x].string is not None:
                            f.write("[" + fan_list[x].string + "]")
                            f.write(str(fan_list[x].get('href')) + "\n")
                        else:
                            f.write("[" + "  " + "]")
                            f.write(str(fan_list[x].get('href')) + "\n")
                if count >= 3 and count <=5:
                    print("------------------连续解%d次失败，休眠10秒后再爬"%count)
                    time.sleep(10)
                # 这个是为了请求6页以后，微博限制用户访问列表，不再继续爬
                if count > 5:
                    print("-----------------------------解析%s页面第%d页粉丝列页面失败!!!!" % (name, page+1))
                    break
            print("---------------休眠两秒后继续爬下一页")
            time.sleep(2)

    except Exception as e:
        print("------------发生异常", e)
    finally:
        pass

def get_contents_page(weibo_id, name, headers, pagebar, page):
    try:
        headers['Referer'] = "https://weibo.com/p/100505" + weibo_id
        url = "https://weibo.com/p/100505" + weibo_id + "/home?profile_ftype=1&is_all=1#_0"
        response = openlink(url, headers)
        html=response.read().decode()
        soup=analyse_html(BeautifulSoup(html,'html5lib'),"Pl_Core_T8CustomTriColumn__3")
        info=soup.find_all('strong',class_='W_f18')
        weibo_size=info[2].string
        print("----------------共有%s条微博"%weibo_size)
        if weibo_size=="0":
            return 0
        if int(weibo_size)<40:
            return 1
        else:
            weibo_div_size = 0
            count = 0
            # 因为有时会出现连接失败，返回的页面是空的，所以反复请求连接直到有页面为止
            while (weibo_div_size == 0):
                count = count + 1
                params = urllib.parse.urlencode(
                    {'ajwvr': 6, 'domain': 100505, "profile_ftype": 1, 'is_all': 1, 'pagebar': pagebar,
                     "pl_name": "Pl_Official_MyProfileFeed__22", "id": "100505" + weibo_id,
                     "script_uri": "/p/" + "100505" + weibo_id,
                     'feed_type': 0, 'page': page + 1, 'pre_page': page + 1, 'domain_op': 100505,
                     '__rnd': get_timestamp()}).encode()  # 调用接口时所用的参数
                cont_url = api_url + "%s" % (params).decode()
                print("---------------请求连接到微博内容页面:%s" % cont_url)
                response=openlink(cont_url,headers)
                html = response.read().decode()  # 对调用接口后传过来的内容进行解码
                cont_html = json.loads(html)['data']
                print("-----------------解析微博文本内容%d次" % count)
                cont_soup = BeautifulSoup(cont_html, 'html.parser')  # 进行解析
                content_page=int(re.sub("\D", "", cont_soup.find_all('a',attrs={"bpfilter":"page"})[1].get_text()))
                return content_page
    except Exception as e:
        print("----------发生异常",e)

def claw_main(name):

        print("----------------------爬取%s的关注者数,粉丝数以及微博数" % name)
        info = get_info(name, headers)  # 获取个人信息
        if info:
            weibo_id = str(info[2])  # 微博id
            print("----------------------要爬取的账号的ID：" + weibo_id)
            print("-----------------------------------------爬取关注列表,共有%d页" % (info[0]))
            get_subs(weibo_id, name, headers, info[0])
            print("-----------10秒后爬取粉丝列表")
            time.sleep(10)
            print("-----------------------------------------爬取粉丝列表,共有%d页" % (info[1]))
            get_fans(weibo_id, name, headers, info[1])
            print("-----------10秒后爬取文本列表")
            time.sleep(10)
            content_page = get_contents_page(weibo_id, name, headers, 1, 1)
            print("-----------------------------------------爬取微博文本,共有%d页" % (content_page))
            for page in range(content_page):  # info[2]是微博列表的总页码
                print("-----------------正在爬取第%d页顶部内容" % (page + 1))
                get_top_contents(weibo_id, name, headers, page + 1)  # 先加载出顶部微博内容
                time.sleep(3)
                for slide in range(0, 2):  # 两次下滑加载内容
                    print("-----------------正在爬取第%d页内容------第%d次滑动加载更多" % (page + 1, slide + 1))
                    get_contents(weibo_id, name, headers, slide, page, content_page)
                    print("---------------------休眠3秒后继续爬下一次滑动")
                    time.sleep(3)
                print("---------------------休眠3秒后继续爬下一页")
                time.sleep(3)
            print("-----------30秒后爬取下一个用户的信息")
            time.sleep(30)
# 程序的入口

if __name__ == "__main__":
    """下面是定义各种属性的地方，有一些需要根据自己实际情况来定"""
    weibo_url = "http://weibo.com/"  # 微博域名
    api_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?"  # 微博文本抓取的apt
    excel_name = '19520816_0_个人性格调查问卷_101_101.xls'
    socket.setdefaulttimeout(25)  # 定义超时时间,25秒
    cookie_save_file = "cookie.txt"  # 默认的存cookie的文件名
    cookie_update_time_file = "cookie_timestamp.txt"  # 默认的存cookie时间戳的文件名
    headers = {  # User-Agent需要根据每个人的电脑来修改，每个人的信息是不同的
        'Accept': '*/*',
        'Accept-Encoding': 'br',
        'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'weibo.com',
        'Referer': "https://weibo.com/",
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': ' '
    }

    username = "987327263@qq.com"
    password = "fengdou123"
    login_condition = "1"  # 1代表用游览器获取cookie,非1代表需要自己手动获取cookie并存入文件
    try:
        if login_condition == "1":
            driver_path = input("请输入游览器引擎的路径")
            cookie = login(username, password, driver_path)  # 实地登陆
        else:
            cookie_save_file = input("请输入你的cookie文件名")  # 定义cookie储存的文件名，但是不能为空
            cookie = direct_get_cookies(cookie_save_file)  # 直接读取文件以获得cookie,如果文件不存在，则返回False
        if cookie != False:  # 文件存在，cookie是有值的就执行下面的
            headers["Cookie"] = cookie  # 将cookie加入到头文件中
            data = pd.read_excel(excel_name)  # 读取excel表格
            names_list = data['微博昵称']  # 获取昵称的列值
            pool=Pool(5)
            pool.map(claw_main,names_list)
    except Exception as e:
        print(e)
