import time
from urllib.parse import quote

import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# TODO(ximingren) 延时等待解决
# TODO(ximingren) 6页以后的页面都是一样的
# TODO(ximingren) stale element reference: element is not attached to the page document
# TODO(ximingren) 实际上爬取的数据比显示的评价数据要多
# 爬取速度：一小时一万条
# TODO(ximingren) 来回99页和100页之间翻滚

def save_to_mongo(product_id, result, num=0):
    try:
        MONGO_COLLECTION = product_id
        if db[MONGO_COLLECTION].insert(result):
            print("存储第%d条数据%s到MongoDB成功" % (num, str(result)))
    except Exception as e:
        print("存储到MongoDB失败", e)


def get_from_mongo(product_id):
    try:
        MONGO_COLLECTION = product_id
        results = db[MONGO_COLLECTION].find()
        return results
    except Exception as e:
        print("获取数据错误", e)


def get_reviews(browser, product, num=0, page=1):
    try:
        product_link = product['product_link']
        product_id = product['product_id']
        product_name = product['product_name']
        product_link = product_link + "#J_Reviews"
        print("正在爬取id为%s 名称为%s的第%d页评价" % (product_id, product_name, page))
        if page == 1:
            browser.get(product_link)
            page = 2
            time.sleep(4)
        else:
            time.sleep(4)
            if page >= 6:
                page = int(browser.find_elements_by_xpath('//div[@class="rate-paginator"]//span')[1].text) + 1
            else:
                page = int(browser.find_elements_by_xpath('//div[@class="rate-paginator"]//span')[0].text) + 1
        reviews = browser.find_element_by_xpath('.//div[@id="J_Reviews"]')
        reviews_num = reviews.find_element_by_xpath('.//h4[@class="hd"]/em').text
        rate_score = reviews.find_element_by_xpath('.//div[@class="rate-score"]//strong').text
        save_to_mongo(product_id,
                      {'product_id': product_id, 'reviews_num': reviews_num, 'rate_score': rate_score}, num)
        reviews = browser.find_element_by_xpath('.//div[@id="J_Reviews"]')
        reviews_list = reviews.find_elements_by_xpath('.//div[@class="rate-grid"]//tr')
        for review in reviews_list:
            num += 1
            review_text = review.find_element_by_xpath('.//div[@class="tm-rate-fulltxt"]').text
            review_date = review.find_element_by_xpath('.//div[@class="tm-rate-date"]').text
            sku = review.find_element_by_xpath('.//div[@class="rate-sku"]/p').text
            review_use = ''.join(review.find_element_by_xpath('.//div[@class="rate-user-info"]').text)
            review_data = {'review_use': review_use,
                           'review_date': review_date,
                           'sku': sku,
                           'review_text': review_text
                           }
            result = dict(product, **review_data)
            save_to_mongo(product_id, result, num)
        button = browser.find_element_by_xpath('.//div[@class="rate-paginator"]//a[last()]')
        button.click()
        if num <= int(reviews_num):
            get_reviews(browser, product, num, page)
        else:
            print("爬取评价完毕")
    except Exception as e:
        with open('failure.txt', 'w') as f:
            f.write(str(product))
        print("爬取评价失败", e)


def get_products(browser):
    """
    爬取当前页的每一条商品
    :param browser:
    :return:
    """
    time.sleep(10)
    div_list = browser.find_elements_by_xpath('.//div[@class="item J_MouserOnverReq  "]')
    # 对每一条商品进行处理
    for div in div_list[5:]:
        img_element = div.find_element_by_xpath('.//img[@class="J_ItemPic img"]')
        price_element = div.find_element_by_xpath('.//div[@class="price g_price g_price-highlight"]')
        saler_num_element = div.find_element_by_class_name('deal-cnt')
        link_element = div.find_element_by_xpath('.//a[@class="J_ClickStat"]')
        product_id = div.find_element_by_xpath('.//a[@class="pic-link J_ClickStat J_ItemPicA"]').get_attribute(
            'trace-nid')
        shop_info_element = div.find_element_by_xpath(
            './/a[@class="shopname J_MouseEneterLeave J_ShopInfo" or @class="shopname"]')
        shop_location_element = div.find_element_by_xpath('.//div[@class="location"]')
        img = img_element.get_attribute('src')
        price = price_element.text
        saler_num = saler_num_element.text[:-3]
        product_name = link_element.text
        product_link = link_element.get_attribute('href')
        shop_name = shop_info_element.text
        shop_location = shop_location_element.text
        product_info = {
            'img': img,
            'price': price,
            'saler_num': saler_num,
            'product_name': product_name,
            'product_link': product_link,
            'shop_name': shop_name,
            'shop_location': shop_location,
            'product_id': product_id
        }
        print("正在解析%s的商品信息" % str(product_name))
        save_to_mongo('electronic', product_info)
    product_list = get_from_mongo('electronic')
    # 对每一种商品进行循环获取评价
    for product in product_list:
        del product['_id']
        get_reviews(browser, product)


def index_page(page):
    """
    爬取搜索页面的每一条商品
    :param page:  第page页
    :return:
    """
    try:
        url = "https://s.taobao.com/search?q=" + quote('ipad')
        print("正在爬取%d页搜索页面 %s" % (page, url))
        browser.get(url)
        browser.maximize_window()
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.wraper div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.wraper div.form >span[class="btn J_Submit"]')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.wraper li[class="item active"] >span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.wraper  .items .item')))
        get_products(browser)  # 爬取当前页的每一条商品
    except TimeoutException:
        index_page(page)
    finally:
        # browser.close()
        pass


if __name__ == '__main__':
    MONGO_URL = "localhost"
    MONGO_DB = "ipad"
    clilent = pymongo.MongoClient(MONGO_URL)
    db = clilent[MONGO_DB]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome('../chromedriver', chrome_options=chrome_options)
    wait = WebDriverWait(browser, 10)
    for page in range(1, 100):
        index_page(page)
