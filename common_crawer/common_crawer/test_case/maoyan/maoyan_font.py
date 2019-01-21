import os
import re

import requests
from fontTools.ttLib import TTFont
from lxml import etree


def create_font(font_file):
    # 列出已下载文件
    file_list = os.listdir('./fonts')
    # 判断是否已下载
    print(font_file)
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
    font1 = TTFont('./fonts/aa56b793571a4be38ebf0686685a55a62080.woff')
    keys = sorted(font1['glyf'].keys())
    values = list(' 2038146957.')
    # 构建基准 {name: num}
    dict1 = dict((k, v) for k, v in zip(keys, values))
    dict2 = {}
    for key in font['glyf'].keys():
        for k, v in dict1.items():
            # 通过比较 字形定义 填充新的name和num映射关系
            if font1['glyf'][k] == font['glyf'][key]:
                key=key.replace('uni',"").lower()
                dict2[key] = v.strip()
                break
    result=[]
    for i in data[0]:
        if i=='.':
            result.append(i)
        for k,v in dict2.items():
            if k in '%r'%i:
                result.append(dict2[k])
    if len(data)==2:
        return ''.join(result)+data[1]
    else:
        return ''.join(result)
        # font_list.append(gly.replace('uni', r"\u").lower())
        #     a=data[0][5*i:5*(i+1)]
    # for i in range(len(data[0])):
    #     print('%r'%((data[0])[i]))
            # if str(data[0][5*i:5*(i+1)]) in gly:
            #         print(gly)
            # data = data[5*i:5*(i+1)].replace(gly, str(number))
    # 返回替换后的字符串
    return data
if __name__ == '__main__':
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
    res=requests.get("http://maoyan.com/films/celebrity/28625",headers=headers)
    tree=etree.HTML(res.text)
    name=tree.xpath('.//p[@class="china-name cele-name"]/text()')
    engName=tree.xpath('.//p[@class="eng-name cele-name"]/text()')
    profession=tree.xpath('.//span[@class="profession"]/text()')
    birthday=tree.xpath('.//span[@class="birthday"]/text()')
    height=tree.xpath('.//span[@class="height"]/text()')
    master_item=tree.xpath('.//li[@class="master-item"]/a/div')
    masterList=[]
    for m in master_item:
        masterList.append(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(),m.xpath('string(.)'))))))
    masterList=';'.join(masterList)
    print(masterList)
    award_detail=tree.xpath('.//div[@class="award-slider award-class slider"]/div')
    awardList=[]
    for a in range(len(award_detail)):
        i=award_detail[a]
        header=''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(),i.xpath('string(.)')))))
        award=''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(),tree.xpath(".//div[@class='award-detail']/div")[a].xpath('string(.)')))))
        awardList.append(header+":"+award)
    awardList=';'.join(awardList)
    relations=tree.xpath('.//div[@class="rel-item"]')
    relationsList=[]
    for r in relations:
        relationsList.append(''.join(list(filter(lambda t: t != '', map(lambda x: x.strip(),r.xpath('string(.)'))))))
    relationsList=';'.join(relationsList)
    print(master_item)
    # print(name)
    # print(engName)
    # print(profession)
    # print(birthday)
    # print(height)
    # print(master_item)
    # sumBox=tree.xpath(".//div[@class='cele-index sumBox']/p[@class='index-num']/span/text()")
    # ranking=tree.xpath(".//div[@class='cele-index']")[0].xpath("./p[@class='index-num']/span/text()")
    # fans=tree.xpath(".//div[@class='cele-index']")[1].xpath("./p[@class='index-num followCount']/span/text()")
    # # font_file='491b289895261bba3b9d0bd903e640ff2076.woff'
    # font_file = re.findall(r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', res.text)[0]
    # font=create_font(font_file)
    # font.saveXML('1.xml')
    # data=modify_data(font,ranking)
    # print(data)
    # data = modify_data(font, fans)
    # print(data)
    # data=modify_data(font,sumBox)
    # print(data)
    # print()