import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4

import random
import time
import const

date_format = "%Y-%m-%d %H:%M:%S"


def scrap():
    const.url = 'https://www.rankingdak.com/'

    # 브라우저 열기
    driver = webdriver.Chrome('./chromedriver')
    driver.get(const.url)
    time.sleep(3)

    # # '카테고리' mouse hover
    header_category = driver.find_element(By.XPATH, "//*[@id='header']/div[2]/div/div/a")
    header_category.click()
    time.sleep(2)

    # '카테고리' > '신상품' click
    new_product_btn = driver.find_element(By.XPATH, "//*[@id='all-category']/ul/li[1]/a")
    new_product_btn.click()
    time.sleep(2)

    bs = bs4.BeautifulSoup(driver.page_source, features="html.parser")

    # 상품 div 리스트 가져오기
    product_divs = bs.select(
        "#contents > div.content-wrap.frame-sm > div.grid-list-wrap.type-sorting > div.list-type-wrap > ul > li > div")

    products = []
    for p in product_divs:

        price = p.select_one(".num").getText()
        display_name = p.select_one(".text-elps2").getText()
        stock = random.randint(0, 100)

        # 현재시간+10일 (start), 현재 시간+60일 (end)
        current_time = datetime.datetime.now()
        start = (current_time + datetime.timedelta(days=10)).strftime(date_format)
        end = (current_time + datetime.timedelta(days=60)).strftime(date_format)
        deadline = random_date(start, end, random.random())

        thumbnail = p.select_one(".lozad")["data-src"]
        seller_id = 1
        delivery_fee = 3000

        products.append({
            "price": price,
            "display_name": display_name,
            "stock": stock,
            "deadline": deadline,
            "thumbnail": thumbnail,
            "seller_id": seller_id,
            "delivery_fee": delivery_fee})

    print(products)

    driver.quit()


def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, date_format, prop)
