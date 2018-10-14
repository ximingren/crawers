# from pprint import pprint
# from functools import cmp_to_key
#
# import requests
#
#
# def test(a, b):
#     a = a['CompanyType']
#     b = b['CompanyType']
#     if a < b:
#         return -1
#     elif a > b:
#         return 1
#     else:
#         return 0
#
#
# if __name__ == '__main__':
#     # s=requests.Session()
#     # res=s.post('https://wap.jx.10086.cn/huih2/pub/main/appLogin/ajaxLogin',data={'jwtTicket':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2MiOiIxMzk3OTk1MTA2NiIsInN1YiI6IjUzODIyRTg1MjRENDJCRDlFMDUzMkUxNkUyMEE3NzEyIiwiYXVkIjoiaHVpaDIiLCJtb2IiOiIxMzk3OTk1MTA2NiIsIm5iZiI6MTUzOTIxOTcwOSwiaXNzIjoidW5pYXBwIiwiZXhwIjoxNTM5MjMxMTA5LCJpYXQiOjE1MzkyMjAzMTQsImp0aSI6IjU2MTIyMjQ0MzUyMTRiM2ZiYjgyMDg0Nzc2NTliMTgwIn0.1nDUL9iACGGdXEDR3N6ZsXtrPNtcvIJCqyl9yDAQMDo'})
#     # res2=s.post('https://wap.jx.10086.cn/huih2/pub/main/baseInfo/getBaseData',data={'phone':'13879992693','isQuery':'1'})
#     # print(res2.text)
#     a = [{'CompanyType': '整合营销', 'SortID': 0, 'CompanyID': 177408, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '蓝天黑马'},
#          {'CompanyType': '发行公司', 'SortID': 0, 'CompanyID': 162344, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '海宁银润影业'},
#          {'CompanyType': '发行公司', 'SortID': 0, 'CompanyID': 175763, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '猫眼微影'},
#          {'CompanyType': '发行公司', 'SortID': 0, 'CompanyID': 1201, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '上影发行'},
#          {'CompanyType': '发行公司', 'SortID': 0, 'CompanyID': 159852, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '枫海传媒（象山）'},
#          {'CompanyType': '发行公司', 'SortID': 0, 'CompanyID': 177406, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '瀚璟影业'},
#          {'CompanyType': '发行公司', 'SortID': 0, 'CompanyID': 177407, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '盛唐映画'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 159069, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '银润广告'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 175797, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '见天地电影工作室'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 6, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '中影'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 28, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '上影集团'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 143036, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '泽十东文化'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 157482, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '银润影视'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 5, 'MovieID': 637824, 'CountryName': '中国香港',
#           'CompanyName': '泽东电影'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 162344, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '海宁银润影业'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 169898, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '恒信天地'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 165797, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '广厦传媒'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 43, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '大地时代'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 168248, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '空中银河'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 162345, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '稼轩环球影业'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 163332, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '天意影视'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 157043, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '重庆电影集团'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 143268, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '保利影业'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 173619, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '霍尔果斯枫海影业'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 177405, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '紫微垣投资'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 177409, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '中影河山'},
#          {'CompanyType': '出品公司', 'SortID': 0, 'CompanyID': 177410, 'MovieID': 637824, 'CountryName': '中国',
#           'CompanyName': '大观投资'}]
#     # a.sort(key=cmp_to_key(test))
#     import execjs
#
#     content = execjs.compile("""
#     function test(_Json){
#     _Key="CompanyType";
#     _OrderFlag=true;
#      return _Json.slice(0).sort(function (a, b) {
#                     var x = a[_Key], y = b[_Key];
#                     if (!isNaN(x)) {
#                         x = Number(x);
#                         y = Number(y);
#                     }
#                     if (_OrderFlag) return ((x < y) ? -1 : ((x > y) ? 1 : 0));//正序
#                     else return ((x > y) ? -1 : ((x < y) ? 1 : 0));//倒序
#                 });}""")
#     c = content.call('test',a)
#     pprint(c)
import time

import requests
from selenium import webdriver

if __name__ == '__main__':
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome('/home/ximingren/Projects/Projects/crawer_summary/chromedriver',
                                   chrome_options=chrome_options)
        # wait = WebDriverWait(browser, 10)
        try:
            for id in range(680000,682000):
                browser.get('http://localhost:8000/Data?EnMovieID=%s' % (str(id)))
                print(id)
        except Exception as e:
            print(e)
        finally:
            browser.close()

        # requests.get('http://localhost:8000/Data?EnMovieID=%s'%(str(id)))
    except Exception as e:
        print(e)
# time.sleep(2)
