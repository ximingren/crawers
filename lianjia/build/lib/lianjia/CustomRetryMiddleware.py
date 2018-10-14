import json
import random

import requests
import logging
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message

from lianjia.lianjia.middlewares import LianjiaDownloaderMiddleware


class CustomRetryMIddleware(RetryMiddleware):
    ban_ips=[]
    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status == 403:
                try:
                    logging.info("添加ban掉的代理地址%s" % request.meta['proxy'])
                    self.ban_ips.append(request.meta['proxy'])
                    return request
                except Exception as e:
                    print(e)
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def get_proxy(self):
        response = requests.get('http://localhost:8899/api/v1/proxies?anonymous=True')
        data = json.loads(response.text)
        proxies = random.choice(data['proxies'])
        if proxies['is_https']:
            proxy = 'https://' + str(proxies['ip']) + ":" + str(proxies['port'])
        else:
            proxy = 'http://' + str(proxies['ip']) + ":" + str(proxies['port'])
        return proxy
