import datetime

from selenium import webdriver
from selenium.common import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bs4

import random
import time

import var

url = 'https://www.rankingdak.com/'
base_date_format = "%Y-%m-%d %H:%M:%S.%f"
date_format = "%Y-%m-%d %H:%M:%S"


def scrap():
    # 브라우저 열기
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)

    # 카테고리
    category_product_strs = {}
    product_detail_strs = []
    product_id = 0
    for category_id, c in enumerate(var.product_categories):
        # '카테고리' mouse hover
        header_category = driver.find_element(By.XPATH,
                                              "//*[@id='header']/div[2]/div/div/a")
        header_category.click()
        time.sleep(1)

        # '카테고리' > '신상품' click
        new_product_btn = driver.find_element(By.LINK_TEXT, c)
        new_product_btn.click()
        time.sleep(1)

        # 노출 상품 개수 '300' click
        try:
            product_cnt_select = driver.find_element(By.XPATH,
                                                     "//*[@id='contents']/div[1]/div[5]/div[1]/div/div[2]")

            product_cnt_select.click()
            time.sleep(1)

            product_cnt_li = driver.find_element(By.XPATH,
                                                 "//*[@id='contents']/div[1]/div[5]/div[1]/div/div[2]/div/ul/li[3]/a")
            product_cnt_li.click()
            time.sleep(2)
        except NoSuchElementException:
            print("노출상품개수 필터가 없는 카테고리")

        bs = bs4.BeautifulSoup(driver.page_source, features="html.parser")

        # 카테고리 생품
        # 상품 li 리스트 가져오기
        product_divs = bs.find_all("div", "prd-item")

        product_strs = []
        for pd in product_divs:
            price = pd.select_one(".num").getText().replace(",", "")
            display_name = pd.select_one(".text-elps2").getText()
            name = display_name
            stock = random.randint(0, 100)

            # 현재시간+10일 (start), 현재 시간+60일 (end)
            current_time = datetime.datetime(2022, 11, 10, 00, 00, 0)
            start = (current_time + datetime.timedelta(days=10)).strftime(date_format)
            end = (current_time + datetime.timedelta(days=60)).strftime(date_format)
            deadline = random_date(start, end, random.random())

            thumbnail = pd.select_one(".lozad")["data-src"]
            seller_id = 1
            delivery_fee = 3000

            # 상품디테일
            # 상품디테일을 보기 위한 썸네일 클릭
            try:

                thumbnail_img = driver.find_element(By.XPATH, f"//img[@alt='{name}']")

                # 상품이 화면에서 보이지 않는 경우 스크롤
                try:
                    thumbnail_img.click()
                except ElementNotInteractableException:
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                    time.sleep(2)
                    thumbnail_img.click()
                except ElementClickInterceptedException:
                    print("오픈 예정 상품")
                    continue

            except NoSuchElementException:
                print("썸네일 이미지 엘리먼트 못찾음")
                continue

            # 상품디테일 문서정보
            bs = bs4.BeautifulSoup(driver.page_source, features="html.parser")

            product_detail_div = bs.find("div", "productCont")
            # 연령확인이 필요한 상품의 경우
            if product_detail_div is None:
                driver.execute_script("window.history.go(-1)")
                time.sleep(2)
                continue

            product_detail_img_tags = product_detail_div.select("img")

            base_date = datetime.datetime.now().strftime(base_date_format)
            # insert query value 생성
            product_strs.append(
                f"{category_id + 1}, {price}, '{name}', '{display_name}', {stock}, '{deadline}', '{thumbnail}', "
                f"{seller_id}, {delivery_fee}, {base_date}, {base_date}"
            )
            print(f"product_str: {product_strs[-1]}")

            product_id += 1
            print(f"product_detail_img_tags: {product_detail_img_tags}")
            for order, img in enumerate(product_detail_img_tags):
                base_date = datetime.datetime.now().strftime(base_date_format)
                try:
                    product_detail_strs.append(
                        f"{product_id}, {order + 1}, '{img['src']}', {base_date}, {base_date}"
                    )
                    print(f"product detail str: {product_detail_strs[-1]}")
                except KeyError:
                    print("제품상세 src 없는 <img>")
                    continue

            driver.execute_script("window.history.go(-1)")
            time.sleep(2)

        # 카테고리에 해당되는 상품 dict
        category_product_strs[c] = product_strs

    driver.quit()
    return category_product_strs, product_detail_strs


def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, date_format, prop)
