# !/usr/bin/python
# -*- coding=utf-8 -*-
import socket
import urllib.parse
from urllib.request import Request, urlopen
import pandas as pd
import re

import sys
from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import os
from numpy import long

"""
    使用说明：基于python3.5,命令行执行
    执行参数分别为登陆帐号，登陆密码，是否用游览器引擎获取cookie（是的时候确保电脑有游览器引擎,并配置好相关信息）
    否的时候请自行登陆微博，手动获取cookie并存入文件.
    !!!由于微博的限制，现在爬虫只能爬前5页的粉丝列表以及关注列表，除非用其它方法!!!
"""

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


def login(username, password,driver_path):
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


"""
    登陆获取cookie
"""


def login_weibo_get_cookies(driver):  # 登录获取cookies
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


"""
    直接转化为cookie
"""


def direct_get_cookies(cookie_save_file):
    try:
        if os.path.exists(cookie_save_file):
            with open(cookie_save_file) as f:
                cookies=f.read()
                if cookies==" ":
                    print("-----------请将cookie正确输入到文件并保存")
                else:
                   save_cookie_update_timestamp(get_timestamp())  # 同时保存当前时间戳,用于第二次访问验证所用
                   return cookies
        else :
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
    with open(cookie_save_file) as f:
        cookie = f.read()
        print("--------------------用户的cookie:\n" + cookie)
        return cookie


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
    判断cookie是否有效
"""


def is_valid_cookie():  # 判断cookie是否有效
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


"""
    某些内容是藏在script里面的,解析script得到需要的html内容
    若不懂可以打印出最开始的html文本来看一下
"""


def get_html(soup, name):
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


"""
    获取个人信息
"""


def get_info(x, headers):
    try:
        info_response = requests.get('http://s.weibo.com/user/' + names_list[x], headers)  # 微博搜索的页面url
        info_soup = BeautifulSoup(info_response.text, 'html5lib')  # 利用BeautifulSoup库进行解析html操作
        info_soup = get_html(info_soup, "pl_user_feedList")
        weibo_info = info_soup.find_all('a', attrs={"class": "W_linkb", "target": "_blank"})  # 找到用户信息的html
        if len(weibo_info) == 0:
            get_info(x, headers)
        else:
            id = weibo_info[0].get('href')  # 用户id
            subs_size = weibo_info[0].string  # 关注数
            fans_size = weibo_info[1].string  # 粉丝数
            contents_size = weibo_info[2].string  # 微博数
            subs_size = int(re.sub("\D", "", subs_size))  # 只取出数字,其它的不管用,下面同理
            fans_size = int(re.sub("\D", "", fans_size))
            contents_size = int(re.sub("\D", "", contents_size))
            id = int(re.findall('\d+', id)[0])
            fans_page = int(round(fans_size / 20))  # 计算出粉丝列表的具体页数
            subs_size = int(round(subs_size / 20))  # 计算出关注列表的具体页数
            contents_size = int(round(contents_size / 44))  # 计算出微博列表的具体页数
            return [subs_size, fans_page, contents_size, id]
    except Exception as e:
        print("------------发生异常", e)
    finally:
        pass


"""
    创建新目录(若不存在)
"""


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


"""
   利用接口调用获取文本
"""


def get_contents(weibo_id, name, headers, pagebar, page):  # 通过微博ID和cookie来调取接口
    try:
        print("-----------------正在爬取第%d页内容------第%d次滑动加载更多" % (page + 1, pagebar + 1))
        headers['Referer'] = "https://weibo.com/p/100505" + weibo_id
        text_size = 0
        count = 0
        # 因为有时会出现连接失败，返回的页面是空的，所以反复请求连接直到有页面为止
        while (text_size == 0):
            count = count + 1
            params = urllib.parse.urlencode(
                {'__rnd': get_timestamp(), 'page': page, 'pagebar': pagebar, "id": "100505" + weibo_id,
                 "script_uri": "/p/" + "100505" + weibo_id,
                 'ajwvr': 6, 'domain': 100505, "pl_name": "Pl_Official_MyProfileFeed__22", "profile_ftype": 1,
                 'feed_type': 0, 'domain_op': 100505}).encode()  # 调用接口时所用的参数
            request = Request(api_url + "?%s" % (params).decode(), headers=headers)
            print("---------------请求连接到微博内容页面")
            response = urlopen(request)
            html = response.read().decode('utf8')  # 对调用接口后传过来的内容进行解码
            html_start = html.find("<div")  # 获取最前面的div标签
            html_end = html.rfind("div>")  # 获取最后面的div标签
            parser_html = html[html_start:html_end + 4]
            cont_html = parser_html.replace('\\"', '"')  # 进行适当的处理
            cont_html = cont_html.replace('\\/', '/')
            print("-----------------解析微博文本内容%d次" % count)
            cont_soup = BeautifulSoup(cont_html, 'html5lib')  # 进行解析
            mkdir("./" + name)
            with open("./" + name + '/CONTENTS.txt', 'a') as f:
                text_list = cont_soup.find_all('div', attrs={"class": 'WB_text W_f14',
                                                             "node-type": "feed_list_content"})  # 文本列表
                time_list = cont_soup.find_all('a',
                                               attrs={"class": 'S_txt2', 'node-type': "feed_list_item_date"})  # 时间列表
                phone_list = cont_soup.find_all('a', attrs={"action-type": "app_source"})  # 手机型号列表
                text_size = len(text_list)
                for x in range(text_size):
                    time = str(time_list[x].get_text().encode('latin-1', 'ignore').decode('unicode_escape', 'ignore'))
                    phone = str(phone_list[x].get_text().encode('latin-1', 'ignore').decode('unicode_escape', 'ignore'))
                    text = str(text_list[x].get_text().encode('latin-1', 'ignore').decode('unicode_escape', 'ignore'))
                    f.write("[" + time + "    " + phone + "]")  # 写入时间和手机型号
                    f.write(text + "\n")  # 写入文本
    except Exception as e:
        print(e)
    finally:
        pass


"""
    获取关注者的信息并写入文件
"""


def get_subs(weibo_id, name, headers, subs_list_size):  # 每一页顶部微博
    try:
        for page in range(1, subs_list_size + 1):
            subs_url = "https://weibo.com/p/100505" + weibo_id + "/follow?page=" + str(
                page) + "#Pl_Official_HisRelation__59"  # 拼凑成关注者列表的页面url
            print("----------------爬取关注者列表的网址：\n" + subs_url)
            print("----------------请求连接到关注者列表页面")
            print("----------------正在爬取第%d页" % page)
            subs_size = 0
            count = 0
            # 因为有时会出现连接失败，返回的页面是空的，所以反复请求连接直到有页面为止
            while (subs_size == 0):
                count = count + 1
                subs_request = Request(subs_url, headers=headers)
                subs_response = urlopen(subs_request)
                subs_html = subs_response.read().decode()
                print("-----------------解析关注者html页面%d次" % count)
                subs_soup = BeautifulSoup(subs_html, 'html5lib')
                subs_soup = get_html(subs_soup, "WB_cardwrap S_bg")
                mkdir("./" + name)  # 创建目录(若不存在)
                # 写入文件
                with open("./" + name + '/SUB.txt', 'a') as f:
                    subs_list = subs_soup.find_all('a', attrs={"class": "S_txt1", "target": "_blank"})
                    subs_size = len(subs_list)
                    for x in range(subs_size):
                        f.write("[" + str(subs_list[x].string) + "]")  # 关注者的昵称
                        f.write(str(subs_list[x].get('href')) + "\n")  # 关注者连接
                # 这个是为了请求6页以后，微博限制用户访问列表，不再继续爬
                if count > 5:
                    break
    except Exception as e:
        print("------------发生异常", e)
    finally:
        pass


"""
    获取粉丝的信息
"""


def get_fans(weibo_id, name, headers, fans_list_size):  # 每一页顶部微博
    try:
        for page in range(1, fans_list_size + 1):
            fans_url = "https://weibo.com/p/100505" + weibo_id + "/follow?relate=fans&page=" + str(
                page) + "#Pl_Official_HisRelation__59"  # 拼凑粉丝列表url
            print("---------------------爬取粉丝列表的网址：\n" + fans_url)
            print("---------------------请求连接到粉丝列表页面")
            print("----------------正在爬取第%d页" % page)
            fans_size = 0
            count = 0
            # 因为有时会出现连接失败，返回的页面是空的，所以反复请求连接直到有页面为止
            while (fans_size == 0):
                count = count + 1
                fans_request = Request(fans_url, headers=headers)
                fans_response = urlopen(fans_request)
                fans_html = fans_response.read().decode()
                print("-----------------------解析粉丝列表html页面%d次" % count)
                fans_soup = BeautifulSoup(fans_html, 'html5lib')
                fans_soup = get_html(fans_soup, "WB_cardwrap S_bg2")  # 获取处理过的html
                mkdir("./" + name)
                with open("./" + name + '/FANS.txt', 'a') as f:
                    fan_list = fans_soup.find_all('a', attrs={"class": "S_txt1", "target": "_blank"})
                    fans_size = len(fan_list)
                    for x in range(fans_size):
                        f.write("[" + fan_list[x].string + "]")
                        f.write(str(fan_list[x].get('href')) + "\n")
                # 这个是为了请求6页以后，微博限制用户访问列表，不再继续爬
                if count > 5:
                    break
    except Exception as e:
        print("------------发生异常", e)
    finally:
        pass


# 程序的入口
if __name__ == "__main__":
    """下面是定义各种属性的地方，有一些需要根据自己实际情况来定"""
    weibo_url = "http://weibo.com/" #微博域名
    api_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?" #微博文本抓取的apt
    socket.setdefaulttimeout(60 * 3)  # 定义超时时间
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
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': ' '
    }

    
    username = sys.argv[1]  # 定义你微博的帐号以及密码,因为爬虫需要用到cookie模拟登陆
    password = sys.argv[2]  # 定义密码
    login_condition=sys.argv[3] #是否用游览器引擎来实地登陆以获得cookie，否的话需要自己上微薄登陆，然后查看coookie并写入到相关的文件中
    if login_condition=="1":
        driver_path=input("请输入游览器引擎的路径")
        cookie = login(username, password,driver_path) #实地登陆
    else:
        cookie_save_file=input("请输入你的cookie文件名") #定义cookie储存的文件名，但是不能为空
        cookie=direct_get_cookies(cookie_save_file) #直接读取文件以获得cookie,如果文件不存在，则返回False
    if cookie!=False: #文件存在，cookie是有值的就执行下面的
        headers["Cookie"] = cookie  # 将cookie加入到头文件中
        data = pd.read_excel('19520816_0_个人性格调查问卷_101_101.xls')  # 读取excel表格
        names_list = data['微博昵称']  # 获取昵称的列值
        for x in range(len(names_list)):
            name = names_list[x]
            print("----------------------爬取%s的关注者数,粉丝数以及微博数" % name)
            info = get_info(x, headers)  # 获取个人信息
            weibo_id = str(info[3])  # 微博id
            print("----------------------要爬取的账号的ID：" + weibo_id)
            print("-----------------------------------------爬取关注列表")
            get_subs(weibo_id, name, headers, info[0])
            print("-----------------------------------------爬取粉丝列表")
            get_fans(weibo_id, name, headers, info[1])
            print("-----------------------------------------爬取微博文本")
            for page in range(info[2]):  # info[2]是微博列表的总页码
                for slide in range(0, 2):  # 两次下滑加载内容
                    html = get_contents(weibo_id, name, headers, slide, page)
            os.remove(cookie_save_file)  # 删除文件
            os.remove(cookie_update_time_file)  # 删除文件
