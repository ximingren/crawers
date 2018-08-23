import time
from urllib.parse import quote

import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MONGO_URL="localhost"
MONGO_DB="taobao"
MONGO_COLLECTION="electronic"
clilent=pymongo.MongoClient(MONGO_URL)
db=clilent[MONGO_DB]

def save_to_mongo(product_name,result):
    try:
        if db[MONGO_COLLECTION].insert(result):
            print("存储数据%s到MongoDB成功"%str(result))
    except Exception:
        print("存储到MongoDB失败")


def get_products(browser):
    div_list = browser.find_elements_by_xpath('.//div[@class="item J_MouserOnverReq  "]')
    for div in div_list:
        img_element = div.find_element_by_xpath('.//img[@class="J_ItemPic img"]')
        price_element = div.find_element_by_xpath('.//div[@class="price g_price g_price-highlight"]')
        saler_num_element = div.find_element_by_class_name('deal-cnt')
        link_element = div.find_element_by_xpath('.//a[@class="J_ClickStat"]')
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
        result={
            'img':img,
            'price':price,
            'saler_num':saler_num,
            'product_name':product_name,
            'product_link':product_link,
            'shop_name':shop_name,
            'shop_location':shop_location
        }
        save_to_mongo(result)
def index_page(page):
    print("正在爬取%d页" % (page))
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
        get_products(browser)
    except TimeoutException:
        index_page(page)
    finally:
        # browser.close()
        pass
if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome('../chromedriver',chrome_options=chrome_options)
    wait=WebDriverWait(browser,10)
    # for page in range(1,100):
    index_page(100)