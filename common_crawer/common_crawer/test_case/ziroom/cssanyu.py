import random
import re

import requests

# TODO 每次都要写头部
# TODO 写一套框架
from lxml import etree

if __name__ == '__main__':
    headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7,zh-CN;q=0.6',
        'Cache-Control': 'no-cache',
        'Host':'baidupan.xn--wxtn5jlzslkal2y.cssanyu.org',
        'Pragma':'no-cache',
        'Proxy-Connection': 'keep-alive',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Origin':'http://baidupan.xn--wxtn5jlzslkal2y.cssanyu.org'
    }
    data={
        'fastloginfield':'username',
        'username':'ximingren',
        'password':'Ximingren123',
        'quickforward':'yes',
        'handlekey':'ls'
    }
    host='http://baidupan.xn--wxtn5jlzslkal2y.cssanyu.org/bbs2/'
    session=requests.session()
    res=session.post("http://baidupan.xn--wxtn5jlzslkal2y.cssanyu.org/bbs2/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1",data=data,headers=headers)
    print(res)
    print(res.text)
    url=re.findall(r'member.php.*\'',res.text)
    url=''.join(url)[:-1]
    print(host+url+'&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login')
    input_code_res=session.get(host+url+'&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login')
    print(input_code_res.text)
    tree=etree.HTML(input_code_res.content)
    seccode=''.join(tree.xpath('.//div[@class="c cl"][1]/span/@id')).replace('seccode_','')
    print(seccode)
    url1="http://baidupan.xn--wxtn5jlzslkal2y.cssanyu.org/bbs2/misc.php?mod=seccode&action=update&idhash=%s&%f&modid=member::logging"%(seccode,random.random())
    print(url1)
    code=session.get(url1)
    print(code.text)
    code_url=re.findall('misc.php.*c',code.text)[1]
    print(host+code_url[:-3])
    coderes=session.get(host+code_url[:-3])
    with open('1.png','wb')as f:
        print(coderes.content)
        f.write(coderes.content)


    # res=session.get('http://baidupan.xn--wxtn5jlzslkal2y.cssanyu.org/bbs2/forum.php?mod=viewthread&tid=273518&extra=page%3D1')
    # print(res.text)


