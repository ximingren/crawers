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



def save_to_mongo(product_id, result):
    try:
        MONGO_COLLECTION = product_id
        if db[MONGO_COLLECTION].insert(result):
            print("存储数据%s到MongoDB成功" % str(result))
    except Exception as e:
        print("存储到MongoDB失败",e)


def get_reviews(browser, product_id, link, product_info, page=1):
    """
    爬取每一条商品下的全部评价
    :param browser:
    :param product_name:
    :param link:
    :param product_info:
    :param page:
    :return:
    """
    try:
        link = link + "#J_Reviews"
        print("正在爬取%s的第%d页评价" % (product_id, page))
        if page == 1:
            browser.get(link)
            time.sleep(4)
            page = 2
            reviews = browser.find_element_by_xpath('.//div[@id="J_Reviews"]')
            reviews_num = reviews.find_element_by_xpath('.//h4[@class="hd"]/em').text
            rate_score = reviews.find_element_by_xpath('.//div[@class="rate-score"]//strong').text
            save_to_mongo(product_id,
                          {'product_id': product_id, 'reviews_num': reviews_num, 'rate_score': rate_score})

        else:
            time.sleep(4)
            page = page + 1
        reviews = browser.find_element_by_xpath('.//div[@id="J_Reviews"]')
        reviews_list = reviews.find_elements_by_xpath('.//div[@class="rate-grid"]//tr')
        for review in reviews_list:
            review_text = review.find_element_by_xpath('.//div[@class="tm-rate-fulltxt"]').text
            review_date = review.find_element_by_xpath('.//div[@class="tm-rate-date"]').text
            sku = review.find_element_by_xpath('.//div[@class="rate-sku"]/p').text
            review_use = ''.join(review.find_element_by_xpath('.//div[@class="rate-user-info"]').text)
            review_data = {'review_use': review_use,
                           'review_date': review_date,
                           'sku': sku,
                           'review_text': review_text
                           }
            result = dict(product_info, **review_data)
            save_to_mongo(product_id, result)
        button = reviews.find_element_by_xpath('.//div[@class="rate-paginator"]/a[last()]')
        button.click()
        get_reviews(browser, product_id, link, product_info, page)
    except NoSuchElementException:
        print("爬取评价完毕")


def get_products(browser):
    """
    爬取当前页的每一条商品
    :param browser:
    :return:
    """
    div_list = browser.find_elements_by_xpath('.//div[@class="item J_MouserOnverReq  "]')
    # 对每一条商品进行处理
    for div in div_list:
        img_element = div.find_element_by_xpath('.//img[@class="J_ItemPic img"]')
        price_element = div.find_element_by_xpath('.//div[@class="price g_price g_price-highlight"]')
        saler_num_element = div.find_element_by_class_name('deal-cnt')
        link_element = div.find_element_by_xpath('.//a[@class="J_ClickStat"]')
        product_id=div.find_element_by_xpath('.//a[@class="pic-link J_ClickStat J_ItemPicA"]').get_attribute('trace-nid')
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
            'shop_location': shop_location
        }
        print("正在解析%s的商品信息" % str(product_name))
        get_reviews(browser, product_id, product_link, product_info)  # 爬取商品的评价数据


def index_page(page):
    """
    爬取搜索页面的每一条商品
    :param page:  第page页
    :return:
    """
    print("正在爬取%d页搜索页面" % (page))
    try:
        url = "https://s.taobao.com/search?q=" + quote('ipad')
        browser.get(url)
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
        browser.close()


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
