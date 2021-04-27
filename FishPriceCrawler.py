import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time

URL = "https://www.susansijang.co.kr/nsis/miw/ko/info/miw3110"
driver_options = webdriver.ChromeOptions()
driver_options.add_argument('headless')
driver_options.add_argument('--no-sandbox')
driver_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path='./MetaInfo/chromedriver', options=driver_options)
driver.get(url=URL)

start_date = datetime(2014, 1, 1)
end_date = datetime(2020, 12, 31)
delta = timedelta(days=1)

def crawl_table(driver):
    number = 0
    price = 0

    trees = driver.find_elements_by_xpath("""//*[@id="print_area"]/form/fieldset/table/tbody/tr""")
    for tree in trees:
        leafs = tree.find_elements_by_tag_name("td")
        isBusan = "부산(기장)" in str(leafs[1].text)
        if not isBusan:
            continue

        try:
            number += int(leafs[2].text.replace("미", ""))
            price += float(leafs[-1].text.replace(",", ""))
        except Exception as e:
            # 수량 표기가 미로 되어있지 않음(?)
            print(e)
    return number, price

# 중간에 데이터가 없을 때마다 다음날 고등어를 다시 검색해야함.
# 이때, 바로 고등어를 검색할 수 없고, 날짜를 바꿔서 조회한 후 다시 고등어를 검색해야 함
# 그냥 계속 눌러주는걸로

# dataframe 준비
dates = list()
tot_prices = list()
tot_numbers = list()
avg_prices = list()

date = start_date

while date <= end_date:
    year, month, day = date.strftime("%Y-%m-%d").split("-")
    print(f"{year}-{month}-{day}")
    tot_number = 0
    tot_price = 0

    select = driver.find_element_by_class_name("ui-datepicker-trigger")
    select.click()

    year_sel = Select(driver.find_element_by_class_name("ui-datepicker-year"))
    year_sel.select_by_value(year)

    month_sel = Select(driver.find_element_by_class_name("ui-datepicker-month"))
    month_sel.select_by_index(int(month)-1)    # month = index + 1


    xpath_day= "//div[@id='ui-datepicker-div']//a[.='"+str(int(day))+"']"
    day_sel = driver.find_element_by_xpath(xpath_day)
    day_sel.click()

    click = driver.find_element_by_id("searchBtn")
    click.click()

    try:
        select = Select(driver.find_element_by_id("kdfshNm"))
        select.select_by_value("고등어")
        click = driver.find_element_by_id("searchBtn")
        click.click()

        # first page
        number, price = crawl_table(driver)
        tot_number += number
        tot_price += price

        # next page
        # assume there is no page exceed 3
        next_page = driver.find_element_by_class_name("paginate")
        n_pages = len(next_page.text.split(" "))-1
        if n_pages > 1:
            next_page.click()
            number, price = crawl_table(driver)
            tot_number += number
            tot_price += price
        else:
            pass

        avg_price = tot_price / tot_number

    except Exception as e:
        # 고등어 가격 정보가 아예 없는 경우(?)
        print(e)
        tot_price = -1
        tot_number = -1
        avg_price = -1

    dates.append(date)
    tot_prices.append(tot_price)
    tot_numbers.append(tot_number)
    avg_prices.append(avg_price)

    date += delta

data = {"date": dates,
        "tot_price": tot_prices,
        "tot_number": tot_numbers,
        "avg_price": avg_prices}
df = pd.DataFrame(data)
df.set_index("date", inplace=True)
df.to_csv("fishprice.csv")
