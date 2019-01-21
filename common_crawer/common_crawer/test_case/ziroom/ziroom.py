import csv
import os
import pandas as pd

import requests
from lxml import etree
import time
from tqdm import tqdm
from retrying import retry
import random
import re
# 接入selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 接入光学识别库
import pytesseract
from PIL import Image

# -----浏览器初始化
print('正在初始化无头Chrome浏览器...')
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
# 添加代理 proxy
# chrome_options.add_argument('--proxy-server=http://' + proxy)
browser = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
print('浏览器初始化完毕')
print('-' * 20)
field = ['id', '链接', '区域', '房源地址', '名称', '房型', '面积', '月租', '房子情况', '地铁情况', '标签']
fileName = 'ziroom'


# ------------------


# ---------------获取总页面数
# 每次重试等待两秒
@retry(wait_fixed=2000)
def get_page_num(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.8.0.16453 '
    }
    response = requests.get(url, headers=header)
    data = etree.HTML(response.text)
    try:
        pages = data.xpath('//*[@id="page"]/span[2]/text()')[0]
        final_page = re.search(r"\d+", pages).group()
        return final_page
    except Exception:
        pages = data.xpath('//*[@id="page"]/span[1]/text()')[0]
        final_page = re.search(r"\d+", pages).group()
        return final_page


# -----------------------------


# -------------------获取页面
# 每次重试等待两秒
@retry(wait_fixed=2000)
def get_page(raw_url, page):
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.8.0.16453 '
    }
    """
    # 构造参数
    # 可更改
    print('正在爬取第', page, '页')
    url = raw_url + '?p=' + str(page)
    # response = requests.get(url, headers=header)
    browser.get(url)
    time.sleep(random.randint(0, 2))
    response = browser.page_source
    return response, url


# ---------------------------


# --------解析-----------------------
# 每次重试等待两秒
@retry(wait_fixed=2000)
def parse_page(html, url, page, num_list):
    data = etree.HTML(html)
    items = data.xpath('//li[@class="clearfix"]')
    datalist = []
    for item in items:
        temp_list = []
        price_list = []
        # 初始化空列表
        id = item.xpath('./div[@class="txt"]/h3/a/@href')
        id = ''.join(re.findall("\d+\.?\d*", ''.join(id)))
        list_title = item.xpath('./div[@class="txt"]/h3/a/text()')
        title = ''.join(list_title)  # 名称
        location = item.xpath('./div[@class="txt"]/h4/a/text()')
        room_location = ''.join(re.findall(' ·(.*)\d', title))  # 房源地址
        region = re.findall('\[.*\]', ''.join(location))
        region = ''.join(region).replace('[', '').replace(']', '')  # 区域
        # print(title)
        house_type = re.search(r"^..", title).group()
        room_type = item.xpath('./div[@class="txt"]/div/p[1]/span/text()')
        room_type = '|'.join(room_type)  # 房型
        area = item.xpath('./div[@class="txt"]/div/p[1]/span[1]/text()')
        area = ''.join(re.findall("\d+\.?\d*", ''.join(area)))  # 面积
        list_metro = item.xpath('./div[@class="txt"]/div/p[2]/span/text()')
        metro = ''.join(list_metro)  # 地铁距离
        condition = item.xpath('./div[@class="txt"]/div/p[@class="leave"]/text()')
        condition = ''.join(condition)  # 有没有空房
        tag = item.xpath('./div[@class="txt"]/p[@class="room_tags clearfix"]/span/text()')
        tag = ''.join(tag)  # 标签
        prices = item.xpath('./div[3]/p[1]/span[position()>1]/@style')
        for item in prices:
            temp_list.append(item.replace("background-position:-", "").replace("px", ""))
        for number in temp_list:
            price = num_list[int(int(number) / 30)]
            price_list.append(price)
        price_final = ''.join(price_list)  # 价格
        print('=' * 40)
        info = {
            # 'type': house_type,
            '名称': title,
            '面积': area,
            '地铁情况': metro,
            '月租': price_final,
            '房子情况': condition,
            '标签': tag,
            '房型': room_type,
            '区域': region,
            '房源地址': room_location,
            '链接': url,
            'id': id
        }
        print(info)
        datalist.append(info)
    save_data(datalist, str(page))
    time.sleep(random.randint(0, 2))

    # -----------------------------------------------------------


# tesseract获取图片数字列表的方法
def get_image_number(html):
    photo = re.findall('var ROOM_PRICE = {"image":"(//.*?.png)"', html)[0]
    image = requests.get('http:' + photo).content
    f = open('price.png', 'wb')
    f.write(image)
    f.close()
    num = []
    number = pytesseract.image_to_string(Image.open("price.png"), config="-psm 8 -c tessedit_char_whitelist=1234567890")
    for i in number:
        num.append(i)
    return num


def save_data(data_list, info):
    try:
        conditon = False
        if not os.path.exists(fileName + '.csv'):
            conditon = True
        with open(fileName + '.csv', 'a', newline='') as f:  # file_path 是 csv 文件存储的路径
            fieldnames = field
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if conditon:
                writer.writeheader()  # 写入头部，即设置列名
            for data in data_list:
                writer.writerow(data)
    except Exception as e:
        write_error(info)
        print('保存数据错误', e)
    else:
        print('保存第%s页数据成功' % info)


def csv_to_excel():
    data = pd.read_csv(fileName + '.csv')
    data.to_excel(fileName + '.xlsx', index=False)


def write_error(info):
    with open('error', 'a') as f:
        f.write(str(info) + '\n')


"""
# 房价映射字典
price_dict = {
    'background-position:-210px': '9',
    'background-position:-0px': '4',
    'background-position:-240px': '7',
    'background-position:-90px': '5',
    'background-position:-60px': '3',
    'background-position:-120px': '1',
    'background-position:-270px': '6',
    'background-position:-30px': '0',
    'background-position:-180px': '2',
    'background-position:-150px': '8',
}
"""

if __name__ == '__main__':
    url = 'http://sh.ziroom.com/z/nl/z2.html'
    end = get_page_num(url)
    print('共有', end, '页')
    for page in tqdm(range(1, int(end) + 1)):
        html, now_url = get_page(url, page)
        # 获取随机数字列表
        num_list = get_image_number(html)
        parse_page(html, now_url, page, num_list)
        csv_to_excel()
    print('已完成')
