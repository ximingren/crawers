import json
import time
from io import BytesIO
import cv2
import numpy as np
import pymongo
import requests
from PIL import Image
from lxml import etree
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import ActionChains


def slide_code(response):
    ISDcode_url = response.url
    namespace = tree.xpath('./body/input[@id="namespace"]')[0]
    uuid = tree.xpath('.//input[@id="uuid"]/@value')
    url = tree.xpath('.//input[@id="url"]/@value')[0]
    ip = tree.xpath('.//input[@id="ip"]/@value')[0]
    serialId = tree.xpath('.//input[@id="serialId"]/@value')[0]
    code = tree.xpath('.//input[@id="code"]/@value')[0]
    sign = tree.xpath('.//input[@id="sign"]/@value')[0]
    callback_url = "https://callback.58.com"
    code_url = callback_url + '/firewall/codev2/getsession.do?' + str(time.time())
    data = {'serialId': serialId, 'code': code, 'sign': sign}
    response = requests.post(code_url, data)
    json_result = json.loads(response.text)
    if json_result['code'] == 0 or json_result['data'] != None:
        element = 'ISDCaptcha'
        width = json_result['data']['width']  # 宽度
        type = json_result['data']['level']  # 验证码级别
        showType = 'win'
        sessionId = json_result['data']['sessionId']
        targetElm = 'btnSubmit'
        verify_url = "https://verifycode.58.com"
        # data={'namespace':namespace,sessionId:sessionId,url:url,'uuid':uuid,'serialId':sessionId}
        # code_result=json.loads(requests.post(callback_url+'/checkcode.do',data).text)
        data = {'showType': 'win', 'sessionId': sessionId}
        msg_result = json.loads(requests.post(verify_url + '/captcha/getV3', data).text)
        if msg_result['code'] == 0:
            content = requests.get(verify_url + msg_result['data']['bgImgUrl'])
            with open('./test_case/a.jpg', 'w') as f:
                f.write(content.text)


def craw_price(tree):
    pages = int(tree.xpath('.//div[@class="pager"]//a[last()-1]//text()')[0])
    for page in range(1, pages+1):
        print("正在爬取第%d页" % page)
        response = requests.get(first_url % page)
        tree = etree.HTML(response.text)
        house_list = tree.xpath('.//ul[@class="house-list-wrap"]/li')
        for house in house_list:
            name = ''.join(house.xpath('./div[@class="list-info"]/h2/a/text()'))
            baseinfo = ''.join(
                list(filter(lambda x: '\n' not in x, house.xpath('./div[@class="list-info"]/p//span/text()'))))
            jjr_info = ''.join(house.xpath('.//div[@class="jjrinfo"]/span/text()')) + ''.join(
                house.xpath('.//div[@class="jjrinfo"]/a/span/text()'))
            sum_price = ''.join(house.xpath('./div[@class="price"]/p[@class="sum"]//text()'))
            unit_price = ''.join(house.xpath('./div[@class="price"]/p[@class="unit"]/text()'))
            house_time = ''.join(house.xpath('./div[@class="time"]/text()'))
            if house_time == '今天':
                house_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            data = {'name': name, 'baseinfo': baseinfo, 'jjr_info': jjr_info, 'sum_price': sum_price,
                    'unit_price': unit_price, 'house_time': house_time}
            insert_data(data)
        time.sleep(3)


def insert_data(data):
    try:
        collection.update({"name": data['name']}, {"$set": data}, True)
        print("插入数据成功", str(data))
    except Exception as e:
        print("插入数据失败", e)


def driver_code():
    browser=webdriver.Chrome('/home/ximingren/Projects/Projects/crawer_summary/chromedriver')
    try:
        url='http://gz.58.com/liwan/ershoufang/pn1/'
        browser.get(url)
        # button=browser.find_element_by_xpath('.//div[@class="wp-onb-tit"]/a[2]')
        # button.click()
        button=browser.find_element_by_id('btnSubmit')
        button.click()
        time.sleep(2)
        target=browser.find_element_by_class_name('dvc-captcha__bgImg').get_attribute('src')
        template=browser.find_element_by_class_name('dvc-captcha__puzzleImg').get_attribute('src')
        # browser.switch_to.frame('tcaptcha_popup')
        # target = browser.find_element_by_id('slideBkg').get_attribute('src')
        # template = browser.find_element_by_id('slideBlock').get_attribute('src')
        # big_img=Image.open(BytesIO(requests.get(img_src).content))
        # point_x,point_y=get_pixels(big_img)
        # print(point_x)
        # left=img.location['x']
        headers={
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'text/html;charset=UTF-8',
    'Cache-Control': 'no-cache',
    'User-Agent':'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
            'Cookie':"""id58=c5/nn1uFX/IxkBAOKilKAg==; 58tj_uuid=2e355558-8a80-4ccf-bd6e-78fc77225c3c; Hm_lvt_3f405f7f26b8855bc0fd96b1ae92db7e=1535467510; myfeet_tooltip=end; wmda_uuid=b79b878094b8b0cede8635c221432bd0; wmda_new_uuid=1; wmda_visited_projects=%3B2385390625025; als=0; xxzl_deviceid=ILZH0G2SLz7C8axXPTaBrCxt46eYddRUssKC%2FTzYrREuWR9EvjVzaJ%2BCY8Ww95hf; 58home=gz; __utma=253535702.2084072100.1535620513.1535620513.1535620513.1; __utmz=253535702.1535620513.1.1.utmcsr=gz.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/tianhe/ershoufang/; city=gz; new_uv=13
referer: https://callback.58.com/firewall/verifycode?serialId=c6ea44ea56161f2566628919e4846a4b_13530240eb32455b801cf786dfc55ee8&code=22&sign=6f3444477ace01584822eb385ab5976b&namespace=ershoufanglistphp&url=http%3A%2F%2Fgz.58.com%2Fershoufang%2F"""
}
        distance=match(requests.get(target,headers).content,requests.get(template,headers).content)
        # tracks=get_tracks(int(distance * 0.4 + 18))
        # # print(tracks)
        # buttonRect=browser.find_element_by_css_selector('#tcaptcha_drag_thumb > div.tcaptcha-drag-thumb-bg.t_iconfont')
        # ActionChains(browser).click_and_hold(buttonRect).perform()
        # for track in tracks['forward_tracks']:
        #     ActionChains(browser).move_by_offset(xoffset=track, yoffset=0).perform()

        time.sleep(0.5)
        # for back_tracks in tracks['back_tracks']:
        #     ActionChains(browser).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        # ActionChains(browser).move_by_offset(xoffset=-3, yoffset=0).perform()
        # ActionChains(browser).move_by_offset(xoffset=3, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(browser).release().perform()

        # buttonRect = browser.find_element_by_css_selector(
        #     '#tcaptcha_drag_thumb > div.tcaptcha-drag-thumb-bg.t_iconfont')
        # buttonRect.click()
        time.sleep(5)

        # img=browser.find_element_by_id('slideBkg').get_attribute('src')
        # with open('./test_case/big.jpg','wb') as f:
        #     f.write(requests.get(img).content)



        # img=browser.find_element_by_xpath('.//img[@class="yidun_bg-img"]/').get_attribute('src')
        # print(img)
        # with open('./test_case/bg.jpg','ab+')as f:
        #     f.write(requests.get(img).text)

        if None:
            browser.close()
    except Exception as e:
        print(e)

def get_pixels(img,point_x=0,point_y=0):
    width=img.size[0]
    height=img.size[1]
    min=256
    for x in range(width):
        for y in range(height):
            r,g,b=img.getpixel((x,y))
            pixels=r+g+b
            if min>pixels:
                min=pixels
                point_x=x
                point_y=y


def match(target,template):
    print(target)
    print(template)
    target_file="./slide_code/target1.jpg"
    template_file='./slide_code/template1.jpg'
    with open(target_file,'wb') as f:
        f.write(target)
    with open(template_file,'wb') as f:
        f.write(template)
    img_rgb = cv2.imread(target_file)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_gray=abs(255-img_gray)
    template = cv2.imread(template_file,0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(res.argmax(), res.shape)
    # cv2.rectangle(template, (y, x), (y+w, x+h), (7, 249, 151), 2)
    return y
    # 使用二分法查找阈值的精确值
    # L = 0
    # R = 1
    # while run < 20:
    #     run += 1
    #     threshold = (R + L) / 2
    #     print(threshold)
    #     if threshold < 0:
    #         print('Error')
    #         return None
    #     loc = np.where(res >= threshold)
    #     print(len(loc[1]))
    #     if len(loc[1]) > 1:
    #         L += (R - L) / 2
    #     elif len(loc[1]) == 1:
    #         print('目标区域起点x坐标为：%d' % loc[1][0])
    #         break
    #     elif len(loc[1]) < 1:
    #         R -= (R - L) / 2
    # return loc[1][0]

def get_tracks(distance):
    print(distance)
    distance += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 3 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
    return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}


def show(name):
	cv2.imshow('Show', name)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def driver_phantom():
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.resourceTimeout"] = 1000
    driver = webdriver.PhantomJS(desired_capabilities=cap)
    driver.get('https://callback.58.com/firewall/verifycode')
    button=driver.find_element_by_xpath('//*[@id="btnSubmit"]')
    button.click()
    time.sleep(5)
    img=driver.find_element_by_xpath('//*[@id="ISDCaptcha"]/div[1]/div/img[1]').get_attribute('src')
    print(img)



if __name__ == '__main__':
    # headers = {  # User-Agent需要根据每个人的电脑来修改，每个人的信息是不同的
    #     'Accept': '*/*',
    #     'Accept-Encoding': 'br',
    #     'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
    #     'Cache-Control': 'max-age=0',
    #     'Connection': 'keep-alive',
    #     # 'Content-Type': 'application/x-www-form-urlencoded',
    #     # 'Host': 'cdata.58.com',
    #     # 'Referer': "https://weibo.com/",
    #     'Pragma': 'no-cache',
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
    #     # 'X-Requested-With': 'XMLHttpRequest',
    #     # 'Cookie': ' '
    # }
    # client = MongoClient()
    # db = client['58']
    # collection = db['house_price']
    # first_url = 'http://gz.58.com/ershoufang/pn%d'
    # response = requests.get(first_url % 1)
    # content = response.text
    # tree = etree.HTML(content)
    # if tree.xpath('.//input[@id="btnSubmit"]'):
    #     # with open('./test_case/test2.html','w+') as f:
    #     #     f.write(content)
    #     print("需要输入验证码")
    #     # slide_code(response)
    #     driver_code(response.url)
    # else:
    #     craw_price(tree)

    # driver_code()

    driver_phantom()
    # get_pixels()

    # cv_readCode()

    # match('./slide_code/target.jpeg','./slide_code/template.jpeg')

    # otemp = '/home/ximingren/Projects/Projects/crawer_summary/common_crawer/common_crawer/slide_code/template1.jpg'
    # oblk = '/home/ximingren/Projects/Projects/crawer_summary/common_crawer/common_crawer/slide_code/target1.jpg'
    # otemp='./slide_code/template.jpg'
    # oblk='./slide_code/target.jpg'
    # target = cv2.imread(otemp, 0)
    # template = cv2.imread(oblk, 0)
    # w, h = target.shape[::-1]
    # print(w,h)
    # template=abs(-template)
    # temp = 'temp.jpg'
    # targ = 'targ.jpg'
    # cv2.imwrite(temp, template)
    # cv2.imwrite(targ, target)
    # target = cv2.imread(targ)
    # target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    # target = abs(256- target)
    # cv2.imwrite(targ, target)
    # target = cv2.imread(targ)
    # template = cv2.imread(temp)
    # # show(-template-250)
    # res = cv2.matchTemplate(target,-template-240, cv2.TM_CCOEFF_NORMED)
    # x, y = np.unravel_index(res.argmax(), res.shape)
    # # 展示圈出来的区域
    # cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
    #
    # L = 0
    # R = 1
    # run=1
    # while run < 20:
    #     run += 1
    #     threshold = (R + L) / 2
    #     print(threshold)
    #     if threshold < 0:
    #         print('Error')
    #     loc = np.where(res >= threshold)
    #     print(len(loc[1]))
    #     if len(loc[1]) > 1:
    #         L += (R - L) / 2
    #     elif len(loc[1]) == 1:
    #         print('目标区域起点x坐标为：%d' % loc[1][0])
    #         break
    #     elif len(loc[1]) < 1:
    #         R -= (R - L) / 2
    #
    # show(template)
