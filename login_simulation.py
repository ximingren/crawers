# encoding=utf8
import base64
import binascii
import json
import re
import time
from urllib import parse

import requests
import rsa
"""
    这个模拟登录程序是参考他人的，而不是自己的
"""
class WeiBoLogin(object):
    def __init__(self):
        """
        预处理函数
        """
        self.user_name=None
        self.pass_word=None
        self.user_uniqueid=None
        self.user_nick=None

        self.session=requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"})
        self.session.get('http://weibo.com/login.php')
        return

    def login(self,user_name,pass_word):
        """
        登录的主程序
        :param user_name:
        :param pass_word:
        :return:
        """
        self.user_name=user_name
        self.pass_word=pass_word
        self.user_uniqueid=None
        self.user_nick=None
        s_user_name=self.get_username() # 获取编码加密后的用户名
        json_data=self.get_json_data(su_value=s_user_name) # 获取服务器的相关信息
        if not json_data:
            return False
        s_pass_word=self.get_password(json_data['servertime'],json_data['nonce'],json_data['pubkey']) # 加密后的密码
        post_data={
            'entry':'weibo',
            'gateway':'1',
            'from':'',
            'savestate':'7',
            'userticket':'1',
            'vsnf':'1',
            'service':'miniblog',
            'encoding':'UTF-8',
            'pwencode':'rsa2',
            'sr':'1920*1080',
            'prelt':'529',
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            'rsakv':json_data['rsakv'],
            'servertime':json_data['servertime'],
            'nonce':json_data['nonce'],
            'su':s_user_name,
            'sp':s_pass_word,
            'returntype':'META'
        }
        # 如果有验证码的话，就获取验证码图片并输入验证码
        if json_data['showpin']==1:
            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), json_data["pcid"])
            with open('captcha.jpeg','wb') as file_out:
                file_out.write(self.session.get(url).content)
            code=input('请输入验证码')
            post_data['pcid']=json_data['pcid']
            post_data['door']=code

        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_=%d" % int(time.time())
        json_data_1=self.session.post(login_url_1,data=post_data)
        # 找到重定向的url
        json_data_1=re.search(r'location.replace\((?P<result>.*)\)',json_data_1.content.decode('GBK')).group('result')
        # 重定向后得到的数据
        json_data_2=self.session.get(json_data_1[:-3].strip('\'')).content.decode('utf-8')
        # if json_data_1['retcode']== 0:
        #     params={
        #          "callback": "sinaSSOController.callbackLoginStatus",
        #         "client": "ssologin.js(v1.4.18)",
        #         "ticket": json_data_1["ticket"],
        #         "ssosavestate": int(time.time()),
        #         "_": int(time.time()*1000),
        #     }
        #     response = self.session.get("https://passport.weibo.com/wbsso/login", params=params)
        json_data_2=json.loads(re.search(r'\((?P<result>.*)\)',json_data_2).group('result'))
        # 如果模拟登录成功
        if json_data_2['result'] is True:
            self.user_uniqueid=json_data_2['userinfo']['uniqueid'] # 用户id
            self.user_nick=json_data_2['userinfo']['displayname'] # 用户名称
            self.userdomain=json_data_2['userinfo']['userdomain'] # 用户的个人域名
            self.person_url="http://weibo.com/u/"+self.user_uniqueid+"/home/"+self.userdomain # 用户个人url
            person_response=self.session.get(self.person_url) # 访问个人url
            person_content=person_response.content.decode('utf-8') # 个人页面的内容
            return person_response.headers
        else:
            print('failed',json_data_2)
        # else:
        #     print('failed',json_data_1)
        # return True if self.user_uniqueid and self.user_nick else False


    def get_username(self):
        """
        获取用户名
        :return: 加密后的用户名
        """
        username_quote=parse.quote_plus(self.user_name) # url编码
        username_base64=base64.b64encode(username_quote.encode('utf-8')) # 加密
        return username_base64.decode('utf-8') # 解码

    def get_json_data(self,su_value):
        """
        获取预处理的服务器数据
        :param su_value: 加密后的用户名
        :return:
        """
        params={
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.19)",
            "su": su_value,
            "_": int(time.time()*1000)
        }
        try:
            response=self.session.get('http://login.sina.com.cn/sso/prelogin.php',params=params)
            json_data=json.loads(re.search(r'\((?P<data>.*)\)',response.text).group('data'))
        except Exception as e:
            json_data={}
            print(e)
        return json_data

    def get_password(self,servertime,nonce,pubkey):
        """
        获取加密后的密码
        :param servertime: 服务器时间
        :param nonce:
        :param pubkey:
        :return:
        """
        string=(str(servertime)+'\t'+str(nonce)+'\n'+str(self.pass_word)).encode('utf-8')
        public_key=rsa.PublicKey(int(pubkey,16),int('10001',16))
        password=rsa.encrypt(string,public_key)
        password=binascii.b2a_hex(password)
        return password.decode()

if __name__ =="__main__":
    weibo=WeiBoLogin()
    cookies=weibo.login('987327263@qq.com','fengdou123')
    print(cookies)
    for item,value in cookies:
        print(item)
        print(value)
