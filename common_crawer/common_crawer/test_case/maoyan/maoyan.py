import os
import re
import time

import requests
from fontTools.ttLib import TTFont
from lxml import etree


def get_base(text):
    tree = etree.HTML(text)
    title = tree.xpath("//div[@class='info-base']/div[@class='info-detail']/div[@class='info-detail-title']//text()")
    category = tree.xpath(
        "//div[@class='info-base']/div[@class='info-detail']/div[@class='info-detail-extra']/div[@class='detail-list']/div[@class='detail-list-content']/p[@class='info-category']//text()")
    runningTime = tree.xpath("//div[@class='info-source-duration']//text()")
    releaseTime = tree.xpath("//div[@class='info-release']//text()")
    scores = tree.xpath("//div[@class='scores']/div[@class='percentbar']//text()")
    score_count = tree.xpath("//p[@class='detail-score-count']//text()")
    rating_num = tree.xpath("//div[@class='rating-stars']//text()")
    wish_count = tree.xpath("//p[@class='detail-wish-count']//text()")
    totalBoxOffice = tree.xpath("//div[@class='info-detail-row'][1]//div[@class='info-detail-col'][1]//text()")
    FirstDayBoxOffice = tree.xpath("//div[@class='info-detail-row'][1]//div[@class='info-detail-col'][2]//text()")
    FirstWeekBoxOffice = tree.xpath("//div[@class='info-detail-row'][1]//div[@class='info-detail-col'][3]//text()")
    predictionBoxOffice = tree.xpath("//div[@class='info-detail-row'][1]//div[@class='info-detail-col'][4]//text()")
    print(','.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), title)))))
    print(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), category)))))
    print(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), runningTime)))).replace(" ", ""))
    print(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), releaseTime)))))
    print(','.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), scores)))))
    score_count = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), score_count))))
    score_count = ''.join(re.findall("\d+\.?\d*", score_count))
    print(score_count)
    print(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), rating_num)))))
    wish_count = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), wish_count))))
    wish_count = ''.join(re.findall("\d+\.?\d*", wish_count))
    print(wish_count)
    print(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), totalBoxOffice))))[4:])
    print(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), FirstDayBoxOffice))))[4:])
    print(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), FirstWeekBoxOffice))))[4:])
    print(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), predictionBoxOffice))))[4:])


def get_marketing():
    res = requests.get('https://piaofang.maoyan.com/movie/344264/promotion/trailers', headers=headers)
    tree = etree.HTML(res.text)
    traller_number = tree.xpath("//div[@class='tralier-number']/div[@class='value-style']//text()")
    play_number = tree.xpath("//div[@class='play-number']/div[@class='value-style']//text()")
    comment_number = tree.xpath("//div[@class='comment-number']/div[@class='value-style']//text()")
    # print(res.text)


def get_box_ce():
    # for url in ce_urls:
    # url=base_url+url
    # id=''.join(re.findall("\d+\.?\d*", url))
    url = 'http://maoyan.com/films/celebrity/%s' % '28625'
    res = requests.get(url, headers=headers)
    font_file = re.findall(r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', res.text)[0]
    font = create_font(font_file)
    # modify_data(font,)
    tree = etree.HTML(res.text)
    num = ''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), tree.xpath(
        "//div[@class='cele-index sumBox']/p[@class='index-num']//text()")))))
    print(num[:-1])
    data = modify_data(font, num[:-1])
    print(data)

    # print(res.text)


def create_font(font_file):
    # 列出已下载文件
    file_list = os.listdir('./fonts')
    # 判断是否已下载
    if font_file not in file_list:
        # 未下载则下载新库
        print('不在字体库中, 下载:', font_file)
        url = 'http://vfile.meituan.net/colorstone/' + font_file
        # new_file = self.get_html(url)
        new_file = requests.get(url).content
        with open('./fonts/' + font_file, 'wb') as f:
            f.write(new_file)

    # 打开字体文件，创建 self.font属性
    font = TTFont('./fonts/' + font_file)
    return font


def modify_data(font, data):
    # 获取 GlyphOrder 节点
    gly_list = font.getGlyphOrder()
    # 前两个不是需要的值，截掉
    gly_list = gly_list[2:]
    # 枚举, number是下标，正好对应真实的数字，gly是乱码
    for number, gly in enumerate(gly_list):
        # 把 gly 改成网页中的格式
        gly = gly.replace('uni', '&#x').lower() + ';'
        # 如果 gly 在字符串中，用对应数字替换
        if gly in data:
            data = data.replace(gly, str(number))
    # 返回替换后的字符串
    return data


def get_honor():
    res = requests.get('http://m.maoyan.com/movie/1170264/honor', headers=headers)
    tree = etree.HTML(res.text)
    festival = tree.xpath("//div[@class='page-content']/div[@class='festival']")
    # festival=tree.xpath("//div[@class='page-content']/div[@class='festival']//div[@class='awards']")
    actor_award = []
    director_award = []
    film_award = []
    for i in range(len(festival)):
        e = festival[i]
        header = e.xpath("//div[@class='header']/h2")[i].xpath('string(.)')
        award = e.xpath("//ul[@class='awards']")[i]
        for l in award.xpath('li'):
            text = l.xpath('string(.)')
            if '演员' in text:
                actor_award.append(header + ":" + text)
            elif '导演' in text:
                director_award.append(header + ":" + text)
            else:
                film_award.append(header + ":" + text)
    print(actor_award)
    print(director_award)
    print(film_award)

    # print(e.xpath("//ul[@class='awards']//text()"))
    # print(','.join((e.xpath('string(.)'))))
    # e=etree.HTML(e.text)
    # header=e.xpath("//div[@class='header']//text()")
    # print(header)


def get_ce():
    res = requests.get("https://piaofang.maoyan.com/movie/344264/celebritylist", headers=headers)
    tree = etree.HTML(res.text)
    actor_item = tree.xpath("//dl[@class='panel-main category'][2]//dd[@class='panel-content']//div[@class='p-item']")
    director_item = tree.xpath(
        "//dl[@class='panel-main category'][1]//dd[@class='panel-content']//div[@class='p-item']")
    other_item = tree.xpath(
        "//dl[@class='panel-main category'][position()>2]//dd[@class='panel-content']//div[@class='p-item']")
    actor = []
    actor_id = []
    director = []
    director_id = []
    other = []
    other_id = []
    for i in actor_item:
        actor_id.append(''.join(re.findall("\d+\.?\d*", ''.join(i.xpath('./a/@href')))))
        actor.append(''.join(i.xpath(".//div[@class='p-desc']/p[1]/text()")) + "(" + ''.join(
            i.xpath(".//div[@class='p-desc']/p[2]/text()")) + ")" + ''.join(
            i.xpath(".//div[@class='p-desc']/p[3]/text()")))
    for i in director_item:
        director_id.append(''.join(re.findall("\d+\.?\d*", ''.join(i.xpath('./a/@href')))))
        director.append(''.join(i.xpath(".//div[@class='p-desc']/p[1]/text()")) + "(" + ''.join(
            i.xpath(".//div[@class='p-desc']/p[2]/text()")) + ")" + ''.join(
            i.xpath(".//div[@class='p-desc']/p[3]/text()")))
    for i in other_item:
        other_id.append(''.join(re.findall("\d+\.?\d*", ''.join(i.xpath('./a/@href')))))
        other.append(''.join(i.xpath(".//div[@class='p-desc']/p[1]/text()")) + "(" + ''.join(
            i.xpath(".//div[@class='p-desc']/p[2]/text()")) + ")" + ''.join(
            i.xpath(".//div[@class='p-desc']/p[3]/text()")))
    # ce_urls=tree.xpath("//dl[@class='panel-main category'][2]//dd[@class='panel-content']//div[@class='p-item']//a/@href")
    # get_box_ce(ce_urls)
    # item=' '.join(list(filter(lambda t: t != '', map(lambda x: x.strip(), item))))
    # print(item)
    # print(item)


def crawer_main():
    res = requests.get("https://piaofang.maoyan.com/movie/344264", headers=headers)
    get_base(res.text)
    get_marketing()


def get_trailers():
    res = requests.get(
        "https://piaofang.maoyan.com/movie/344264/promption-ajax?method=change&type=trailers&typeId=0&date=2018-10-10__2018-10-24",
        headers=headers)
    data = res.json()
    tenxunList = []
    aiqiyiList = []
    youkuList = []
    souhuList = []
    maoyanList = []
    for a in data['data']:
        list = a['list']
        date = str(a['showDate'])
        tenxunList.append(date + ":" + str(list[0]['playCount']))
        aiqiyiList.append(date + ":" + str(list[1]['playCount']))
        youkuList.append(date + ":" + str(list[2]['playCount']))
        souhuList.append(date + ":" + str(list[3]['playCount']))
        if len(list) >= 5:
            maoyanList.append(date + ":" + str(list[4]['playCount']))
        else:
            maoyanList.append(date + ":" + " ")
    print(tenxunList)
    print(aiqiyiList)
    print(youkuList)
    print(souhuList)
    print(maoyanList)
    res = requests.get('https://piaofang.maoyan.com/movie/344264/promotion/trailers', headers=headers)
    tree = etree.HTML(res.text)
    traller_number = tree.xpath("//div[@class='tralier-number']/div[@class='value-style']//text()")
    play_number = tree.xpath("//div[@class='play-number']/div[@class='value-style']//text()")
    comment_number = tree.xpath("//div[@class='comment-number']/div[@class='value-style']//text()")
    print(traller_number)
    print(play_number)
    print(comment_number)


def get_weibo():
    res = requests.get(
        "https://piaofang.maoyan.com/movie/344264/promption-ajax?method=change&type=weibo&startDate=2018-10-10&endDate=2018-10-24",
        headers=headers)
    data = res.json()
    commentNum = []
    count = []
    forwardNum = []
    likeNum = []
    for a in data['data']:
        date = a['date']
        commentNum.append(date + ":" + str(a['commentNum']))
        count.append(date + ":" + str(a['count']))
        forwardNum.append(date + ":" + str(a['forwardNum']))
        likeNum.append(date + ":" + str(a['likeNum']))
    res = requests.get("https://piaofang.maoyan.com/movie/344264/promotion/weibo", headers=headers)
    tree = etree.HTML(res.text)
    subject = tree.xpath("//div[@class='item']")[1].xpath("./div[@class='data']//text()")
    yesterday = tree.xpath("//div[@class='item']")[0].xpath("./div[@class='data']//text()")
    print(yesterday)
    print(subject)
    print(commentNum)
    print(count)
    print(forwardNum)
    print(likeNum)


def get_wechat():
    res = requests.get(
        "https://piaofang.maoyan.com/movie/344264/promption-ajax?type=wechat&method=changeAccountChart&startDate=2018-10-10&endDate=2018-10-23",
        headers=headers)
    data = res.json()
    articleNum = []
    everyreadNum = []
    for a in data['data']:
        date = a['date']
        articleNum.append(date + ":" + str(a['articleNum']))
        everyreadNum.append(date + ":" + str(a['readNum']))
    res = requests.get("https://piaofang.maoyan.com/movie/344264/promotion/wechat", headers=headers)
    tree = etree.HTML(res.text)
    titleNum = tree.xpath("//div[@class='summary-cotnent']")[0].xpath("./span/text()")
    readNum = tree.xpath("//div[@class='summary-cotnent']")[1].xpath("./span/text()")
    print(titleNum)
    print(readNum)
    print(everyreadNum)
    print(articleNum)


def get_baidu():
    res = requests.get(
        "https://piaofang.maoyan.com/movie/344264/promption-ajax?method=getIndex&type=baidu&startDate=2018-10-10&endDate=2018-10-23",
        headers=headers)
    data = res.json()
    totalIndex = []
    for a in data['data']:
        date = a['date']
        totalIndex.append(date + ":" + a['totalIndex'])
    print(totalIndex)


if __name__ == '__main__':
    base_url = 'https://piaofang.maoyan.com/'
    url = "https://piaofang.maoyan.com/movie/%s"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'Cookie':"""lxsdk_cuid=16642044005c8-03222f1ac66317-3c7f0257-1fa400-16642044005c8; _lxsdk=D8F33930C84411E8B89A69778381370431AE96FFE4EA4C1FBB36B06F3B819C3C; __mta=217888681.1538705866856.1538705866856.1538705866856.1; theme=moviepro; __mta=217888681.1538705866856.1538705866856.1540346472071.2; _lx_utm=utm_term%3D5.2.3%26utm_source%3DMoviePro_aliyun; _lxsdk_s=166a3ca8f63-b2c-c8f-3dd%7C%7C84""",
        # 'Host':"piaofang.maoyan.com"
        # 'referer'
    }
    # crawer_main()
    # get_marketing()
    # get_ce()
    # get_honor()
    # get_ce()
    get_trailers()
    # get_box_ce()
    # print(os.path.('/html'))
    # get_weibo()
    # get_wechat()
    # get_baidu()
