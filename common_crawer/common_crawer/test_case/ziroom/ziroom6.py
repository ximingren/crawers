import os

import PIL.ImageOps
import requests
from PIL import Image, ImageEnhance
from lxml import etree
from pytesseract import pytesseract


def parse_main(text):
    tree = etree.HTML(text)
    houseList = tree.xpath(".//li[@class='clearfix']")
    for house in houseList:
        title = house.xpath('/div[@class="txt"]/h3/text()')
        location = house.xpath('/div[@class="txt"]/h4/text()')
        detail = house.xpath('/div[@class="txt"]/div[@class="detail"]/p[1]/text()')
        location_detail = house.xpath('/div[@class="txt"]/div[@class="detail"]/p[2]/text()')
        empty_detail = house.xpath('/div[@class="txt"]/div[@class="detail"]/p[3]/text()')
        print(title)


def crawer_main():
    res = requests.get("http://sh.ziroom.com/z/nl/z3.html?qwd", headers=headers)
    parse_main(res.text)


def read_num(img=None):
    file = "fdd00a4ec7f121b39ff49c5c234e09bes.jpg"
    im = Image.open(file)
    # im = im.convert('1')
    # im = PIL.ImageOps.invert(im)
    # im.show()
    # im = ImageEnhance.Contrast(im)
    # im = im.enhance(5)
    # enhancer = ImageEnhance.Color(im)
    # enhancer = enhancer.enhance(0)
    # enhancer = ImageEnhance.Brightness(enhancer)
    # enhancer = enhancer.enhance(2)
    # enhancer = ImageEnhance.Contrast(enhancer)
    # enhancer = enhancer.enhance(8)
    # enhancer = ImageEnhance.Sharpness(enhancer)
    # im = enhancer.enhance(20)
    im.show()
    print(pytesseract.image_to_string(im,config="-psm 8 -c tessedit_char_whitelist=1234567890"))
    print(im)


def InverseWhite(img):
    w, h = img.size
    data = list(img.getdata())
    for x in range(w):
        for y in range(h):
            if data[y * w + x] != 255:  # 255是白色 0是黑色
                img.putpixel((x, y), 0)
            else:
                img.putpixel((x, y), 255)
    return img


if __name__ == '__main__':
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Host': 'sh.ziroom.com',
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    # crawer_main()
    read_num()
    list_title = item.xpath('./div[@class="txt"]/h3/a/text()')
    title = ''.join(list_title)
    # print(title)
    house_type = re.search(r"^..", title).group()
    list_area = item.xpath('./div[@class="txt"]/div/p[1]/span/text()')
    area = ''.join(list_area)
    # print(area)
    list_metro = item.xpath('./div[@class="txt"]/div/p[2]/span/text()')
    metro = ''.join(list_metro)
    condition = item.xpath('./div[@class="txt"]/div/p[@class="leave"]/text()')
    condition = ''.join(condition)
    tag = item.xpath('./div[@class="txt"]/p[@class="room_tags clearfix"]/span/text()')
    tag = ''.join(tag)
