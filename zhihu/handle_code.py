import chardet
import requests
headers={
  'Accept': '*/*',
        'Accept-Encoding': 'br',
        'Accept-Language': 'zh,en-GB;q=0.9,en;q=0.8,en-US;q=0.7',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
"Referer":"https://www.zhihu.com",

}
response=requests.get('https://www.zhihu.com',headers=headers)
print(response.content)
# print(response.content.decode('utf8','ignore'))
