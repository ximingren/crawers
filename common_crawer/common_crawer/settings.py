# -*- coding: utf-8 -*-

# Scrapy settings for common_crawer project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'common_crawer'

SPIDER_MODULES = ['common_crawer.spiders']
NEWSPIDER_MODULE = 'common_crawer.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'common_crawer (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 并发的request连接数
CONCURRENT_REQUESTS = 20

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 定义下载延时
DOWNLOAD_DELAY = 3
# 定义下载超时
DOWNLOAD_TIMEOUT = 13
# 每个并发最大的ip限制数
CONCURRENT_REQUESTS_PER_IP = 20
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 禁止cookie
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'text/html;charset=UTF-8',
    'Cache-Control': 'no-cache',

}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html


# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'common_crawer.middlewares.CommonCrawerSpiderMiddleware': 543,
    'common_crawer.middlewares.CommonCrawerDownloaderMiddleware': 540,
    'common_crawer.RandomHeadersMiddleware.RandomUserAgentMiddleware': 400,
'scrapy.downloadermiddlewares.redirect.RedirectMiddleware':None,
    'common_crawer.CommonRedirectMiddleware.CommonRedirectMiddleware':31,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'common_crawer.pipelines._58CrawerPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# 定义自动限速
# AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# # The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# # Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 定义MongoDB
MONGO_URI = "mongodb://localhost"
MONGO_DATABASE = "ebotapp"

# 定义日志
LOG_LEVEL = "INFO"
# LOG_FILE="log"

# 定义重试爬取
RETRY_ENABLED = True
RETRY_TIMES = 5

RANDOMIZE_DOWNLOAD_DELAY=True

#
MAIL_HOST="smtp.163.com"
MAIL_FROM='yanlunka@163.com'
MAIL_USER='yanlunka@163.com'
MAIL_PASS="qq13516654182"

USE_PROXY=True

# 配置分布式
# DUPEFILTER_CLASS="scrapy_redis.duperfilter.RFPDuperFilter"
# SCHEDULER="scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST=True

# REDIS_HOST='172.16.14.92'
# REDIS_PORT=6379

# ITEM_PIPELINES={
#     'common_crawer.pipelines._58CrawerPipeline':300,
#     'scrapy_redis.pipelines.RedisPipeline':400
# }