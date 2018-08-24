# encoding:utf8
import time

from lxml import etree
from selenium import webdriver


def seleium():
    pass
    #         url="https://taobao.com"
    #         browser.get(url)
    #         input=browser.find_element_by_id('q')
    #         input.send_keys('手机')
    #         input.send_keys(Keys.ENTER)
    #         js="""
    #  var i=0
    # var interval
    # interval=setInterval(function(){scrollWindow()},1000)
    # function scrollWindow(){
    # i=i+100
    #             document.body.scrollTop=i
    #         if (i>document.body.scrollHeight){
    # clearInterval(interval)
    # }
    # }
    #         """
    #         browser.execute_script(js)
    # time.sleep(5)
    # div_list=browser.find_elements_by_class_name('important-key')
    # ActionChains(browser).move_to_element(div_list).perform()

    # for div in div_list:
    #     screen_size=div.text
    # #     img_box=div.find_element_by_class_name('img-box')
    # #     screen_size=img_box.find_element_by_class_name('important-key').text
    #     print(screen_size)

    # browser.execute_script('window.open()')

    # logo=browser.find_element_by_id('zh-top-link-logo')
    # print(logo)
    # print(logo.get_attribute('class'))
    # input=browser.find_element_by_class_name('zu-top-add-question')
    # print(input.text)
    # browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    # browser.execute_script('alter("TO Bottom")')

    # browser.switch_to_frame('iframeResult')
    # source=browser.find_element_by_css_selector('#draggable')
    # target=browser.find_element_by_css_selector('#droppable')
    # actions=ActionChains(browser)
    # actions.drag_and_drop(source,target)
    # actions.perform()

    # input=browser.find_element_by_id('q')
    # input.send_keys('python')
    # time.sleep(1)
    # input.clear()
    # input.send_keys('iPad')
    # button=browser.find_element_by_class_name('btn-search')
    # button.click()
    # input.send_keys(Keys.ENTER)
    # wait=WebDriverWait(browser,10)
    # wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    # print(browser.current_url)

def parse_review():
    html="""
<div class="rate-page"><div class="rate-paginator"><a data-page="4" href="?page=4">&lt;&lt;上一页</a><a href="?page=1">1</a><a href="?page=2">2</a><a href="?page=3">3</a><a href="?page=4">4</a><span>5</span><a href="?page=6">6</a><a href="?page=7">7</a><span class="rate-page-break">...</span><a data-page="6" href="?page=6">下一页&gt;&gt;</a></div></div>    """
    tree=etree.HTML(html)
    # for x in tree.xpath('.//div[@class="rate-grid"]//tr'):
        # print(x.xpath('.//td[@class="tm-col-master"]/div[@class="tm-rate-content"]/div[@class="tm-rate-fulltxt"]/text()'))
    print(tree.xpath('//div[@class="rate-paginator"]//span')[0].text)

def selenium_html():
    url='https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.14.48676a1acw8DU0&id=574147597194&skuId=3930870074919&user_id=2098506058&cat_id=2&is_b=1&rn=45b4a517909c85b7e380540b714034a5'+"#J_Reviews"
    browser = webdriver.Chrome('../chromedriver')
    browser.get(url)
    # button=browser.find_element_by_xpath('.//a[@href="#J_Reviews"]')
    # button.click()
    # time.sleep(5)
    # print(browser.find_element_by_xpath('.//div[@class="rate-grid"]//tr'))
    time.sleep(5)
    browser.find_element_by_xpath('.//div[@class="rate-paginator"]/a[last()]').click()

    # browser.get('https://www.taobao.com')
    # input = browser.find_element_by_id('q')
    # input.send_keys('iPhone')
    # time.sleep(1)
    # input.clear()
    # input.send_keys('iPad')
    # button = browser.find_element_by_class_name('btn-search')
    # button.click()
if __name__ == '__main__':
    parse_review()
