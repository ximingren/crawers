from http.cookies import SimpleCookie
from pprint import pprint

# _utm开头的是google analyse用于分析访客信息的
# _pk_id是你的id
# _pk_ref 相当于referer
#
def analyse():
    cookie = 'bid=lIu3h3JHU8M; ll="108169"; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=D92E42ED83B9D3D469075A00519B6B8A4|62af73017681c772484022afcd94f375; __utmz=223695111.1541655047.3.2.utmcsr=iaas.cloud.tencent.com|utmccn=(referral)|utmcmd=referral|utmcct=/webshell; ps=y; push_noty_num=0; push_doumail_num=0; gr_user_id=1b34b294-fc4a-4cc1-a473-b8d0ad8178de; __utma=223695111.1497463613.1541598313.1541764269.1543036448.8; douban-profile-remind=1; __utmv=30149280.18703; __utma=30149280.460722265.1541598313.1543036448.1543036885.9; __utmz=30149280.1543036885.9.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1543110769%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; as="https://movie.douban.com/subject/27015848/"; dbcl2="187800715:DA1Oe6nPBl8"; ck=9uuX; _pk_id.100001.4cf6=21d9ea0b8d8a8647.1541598312.21.1543110887.1543037453.'
    s = SimpleCookie(cookie)
    pprint({v.key: v.value for k, v in s.items()})


if __name__ == '__main__':
    analyse()
