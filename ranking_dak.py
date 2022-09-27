import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import const


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

    # 상품 리스트 가져오기
    products = driver.find_elements(By.CLASS_NAME, "ext-li")
    print(products)