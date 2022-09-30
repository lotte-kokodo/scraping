import datetime

from selenium import webdriver
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import bs4

import random
import time

import var

url = 'https://www.rankingdak.com/'
date_format = "%Y-%m-%d %H:%M:%S"


def scrap():
    # 브라우저 열기
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(3)

    action = ActionChains(driver)

    # 카테고리
    category_product = {}
    for c in var.product_categories:
        # '카테고리' mouse hover
        header_category = driver.find_element(By.XPATH, "//*[@id='header']/div[2]/div/div/a")
        header_category.click()
        time.sleep(1)

        # '카테고리' > '신상품' click
        new_product_btn = driver.find_element(By.LINK_TEXT, c)
        new_product_btn.click()
        time.sleep(1)

        bs = bs4.BeautifulSoup(driver.page_source, features="html.parser")

        # 카테고리 생품
        # 상품 li 리스트 가져오기
        product_divs = bs.find_all("div", "prd-item")

        product_strs = []
        product_detail_strs = []
        for pd in product_divs:
            price = pd.select_one(".num").getText().replace(",", "")
            display_name = pd.select_one(".text-elps2").getText()
            name = display_name
            stock = random.randint(0, 100)

            # 현재시간+10일 (start), 현재 시간+60일 (end)
            current_time = datetime.datetime.now()
            start = (current_time + datetime.timedelta(days=10)).strftime(date_format)
            end = (current_time + datetime.timedelta(days=60)).strftime(date_format)
            deadline = random_date(start, end, random.random())

            thumbnail = pd.select_one(".lozad")["data-src"]
            seller_id = 1
            delivery_fee = 3000

            product_strs.append(
                f"{price}, '{name}', '{display_name}', {stock}, '{deadline}', '{thumbnail}', {seller_id}, {delivery_fee}"
            )

            # 상품디테일
            # 상품디테일을 보기 위한 썸네일 클릭
            thumbnail_img = driver.find_element(By.XPATH, f"//img[@alt='{name}']")

            # 상품이 화면에서 보이지 않는 경우 스크롤
            try:
                thumbnail_img.click()
            except ElementNotInteractableException:
                action.move_to_element(thumbnail_img).perform()
                time.sleep(2)
                thumbnail_img.click()


            # 상품디테일 문서정보
            bs = bs4.BeautifulSoup(driver.page_source, features="html.parser")

            product_detail_div = bs.find("div", "productCont")
            product_detail_img_tags = product_detail_div.select("img")
            print(product_detail_img_tags)

            for order, img in enumerate(product_detail_img_tags):
                product_detail_strs.append(
                    f"{order}, '{img['src']}'"
                )

            driver.back()
            time.sleep(3)

            # # 상품 디테일 보기
            # product_thumbnails = driver.find_elements(By.TAG_NAME, "figure")
            # for pi in product_thumbnails:
            #     # 메인화면 문서정보
            #     bs = bs4.BeautifulSoup(driver.page_source, features="html.parser")
            #
            #     pi.click()
            #     time.sleep(5)
            #
            #     # 상품디테일 문서정보
            #     bs = bs4.BeautifulSoup(driver.page_source, features="html.parser")
            #
            #     product_detail_imgs = bs.find('img', {'alt': '상세'})
            #     print(product_detail_imgs)
            #
            #     driver.back()
            #     time.sleep(3)

        category_product[c] = product_strs

    driver.quit()
    return category_product


def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, date_format, prop)
