import json
import random

import chardet
import requests
headers={
  'Accept': '*/*',
        'Accept-Encoding': 'br',
        'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
"Referer":"https://www.zhihu.com",

}
response=requests.get('http://localhost:8899/api/v1/proxies?anonymous=True')
data=json.loads(response.text)
proxies=random.choice(data['proxies'])
if proxies['is_https']:
    proxy='https://'+str(proxies['ip'])+":"+str(proxies['port'])
print(proxy)
# print(response.content.decode('utf8','ignore'))
