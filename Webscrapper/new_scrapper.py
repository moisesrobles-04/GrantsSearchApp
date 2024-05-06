import csv
import datetime
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

link = "https://www.grants.gov/search-grants"

# Access grants.gov and search for grants

def grant_scrapper():
    with webdriver.Chrome() as driver:
        # data to upload to database
        grant = []

        # titles of the data
        titles_list = []
        driver.get(link)
        wait = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table")))

        dropdown_select(driver, -1)

        wait = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table")))
        time.sleep(1)

        page_length = driver.find_element(By.XPATH,
                                          "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table/thead/tr[1]/th/nav/ul/li[6]/a").text

        titles = driver.find_elements(By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table/thead/tr[2]/th")

        for i in titles:
            if i.text == '':
                att = i.get_attribute("innerHTML").split(" <")
                titles_list.append(att[0])
            else:
                titles_list.append(i.text)

        titles_list.append("Instrument Type")
        titles_list.append("Category")
        titles_list.append("Matching")
        titles_list.append("Award Ceiling")
        titles_list.append("Award Floor")
        grant.append(titles_list)

        # size = int(page_length)
        size = 1
        grant_links = get_grants_links(driver, size)
        result = soup_scraper(driver, grant_links)

        grant.extend(result)

        return grant

# Read each page and extract data
def soup_scraper(driver, grant_links):
    output = []
    for element in grant_links:
        opportunity, o_link = element['Opportunity Number'], element['link']
        driver.get(o_link)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[3]")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        data = soup.findAll('td')
        title = data[6].text
        instrument = data[12].text
        category = data[14].text
        match = data[22].text

        if soup.find('div', {'class':"eyebrow"}):
            status = 'Forecasted'
            postdate = data[30].text
            closeddate = data[32].text
            ceiling = data[44].text
            floor = data[46].text
            agency = data[52].text

        else:
            status = 'Forecasted'
            postdate = data[26].text
            closeddate = data[32].text
            ceiling = data[38].text
            floor = data[40].text
            agency = data[46].text

        post = format_date(postdate)
        close = format_date(closeddate)
        new_ceil = aux_str(ceiling)
        new_floor = aux_str(floor)

        grant_data = [opportunity, title, agency, status, post, close, instrument, category, match, new_ceil, new_floor]

        if "UTF-8" in str(grant_data) or "NHGRI" in str(grant_data) or "RADx" in str(grant_data) or "�" in str(
                grant_data) or 'Ō' in str(grant_data) or "ô" in str(grant_data):
            print("Eliminated")
            continue

        output.append(grant_data.copy())
        grant_data.clear()

    return output

# Extract grant links
def get_grants_links(driver, size):
    temporary = []
    for i in range(0, size + 1):
        dropdown_select(driver, i)
        cell = driver.find_elements(By.XPATH, "/html/body/div[1]/div[4]/div/div/div/div[2]/div[3]/table/tbody/tr/td/a")
        for g_link in cell:
            g_dict = {"Opportunity Number": g_link.text, "link": g_link.get_attribute('href')}
            temporary.append(g_dict)

    return temporary


def format_date(date):
    if date == '':
        return '01/01/2099'

    date_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    d_split = date.split(' ')
    month, day, year = d_split[0], d_split[1], d_split[2]
    day = day.replace(',', '')
    new_date = f'{date_dict.get(month)}/{day}/{year}'
    return new_date

# Change money to num
def aux_str(money):
    if not money or money == '$':
        return '0'
    result = money.replace("$", "")
    res = result.replace(",", "")
    return res


# change pages
def skip_page(driver):
    skip = driver.find_elements(By.XPATH, "//*[@class='usa-pagination__link-text']")
    for element in skip:
        if element.text.lower().__contains__('next'):
            element.click()
            break


def dropdown_select(driver, num):
    if num == -1:
        # Select last 4 weeks values
        dropdown = Select(driver.find_element(By.XPATH, "//*[@id='dateRange']"))
        dropdown.select_by_index(5)
        update_data = driver.find_element(By.XPATH,
                                          "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[2]/div[2]/div[2]/button")
        update_data.send_keys(Keys.ENTER)

    if num > 0:
        skip_page(driver)

    time.sleep(1)


if __name__ == "__main__":
    start = time.time()
    with open("Grants_data_" + str(datetime.date.today()) + ".csv", "w", newline='', encoding='utf-8') as funds:
        writer = csv.writer(funds)
        result = grant_scrapper()
        writer.writerows(result)
        end = time.time()
        print(f"Finished at: {end-start}")
        funds.close()
