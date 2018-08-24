import json
import requests


def get_news(news_url, comment_url):
    response = requests.get(news_url)
    news_list = json.loads(response.text)
    for new in news_list['data']:
        abstract = new['abstract']  # 摘要标题
        comment_count = new['comment_count']
        group_id = new['group_id']
        item_id = new['item_id']  # 这两个还不知道怎么弄
        keywords = new['keywords']  # 关键词
        publish_time = new['publish_time']  # 发布时间
        read_count = new['read_count']  # 阅读量
        share_count = new['share_count']  # 分享次数
        title = new['title']  # 文章标题


if __name__ == '__main__':
    news_url="https://is.snssdk.com/api/news/feed/v88/"
    comment_url="https://is.snssdk.com/article/v3/tab_comments/?group_id=%s&count=%s&offset=2%s"
    get_news(news_url,comment_url)
