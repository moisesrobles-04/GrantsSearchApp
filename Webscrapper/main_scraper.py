import csv
import datetime
import json

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

        size = int(page_length)

        for i in range(0, size):
            # Number of pages to skip
            # if i<13:
            #     skip_page(driver, i)
            #     time.sleep(2)
            #     continue

            count = 1
            cell = driver.find_elements(By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table/tbody/tr/td")
            cell_tostring = []
            for elem in cell:
                # check if element is closed date, if it is select by innerHTML
                if count < 6:
                    cell_tostring.append(elem.text)

                else:
                    att = elem.get_attribute("innerHTML").split("<")
                    att = att[1].split(">")
                    if att[1] == "no data":
                        cell_tostring.append("2099-01-01")
                    else:
                        cell_tostring.append(att[1])
                        count = 0
                count += 1
            count = 1
            index = 1
            temporary = []
            for element in cell_tostring:
                try:
                    temporary.append(element)
                    if count < 6:
                        continue

                    else:
                        send = driver.find_element(By.XPATH,
                                                   "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table/tbody/tr["
                                                   + str(index) + "]/td[1]/a")
                        send.send_keys(Keys.ENTER)

                        wait = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[3]")))

                        if temporary.count("Forecasted") == 1:
                            instrument = driver.find_element(By.XPATH,
                                                             "//*[@id='opportunity-container']/div/div[2]/div/div[1]/table/tbody/tr[6]/td[1]")
                            cat = driver.find_element(By.XPATH,
                                                      "//*[@id='opportunity-container']/div/div[2]/div/div[1]/table/tbody/tr[7]/td[1]")
                            match = driver.find_element(By.XPATH,
                                                        "//*[@id='opportunity-container']/div/div[2]/div/div[1]/table/tbody/tr[11]/td[1]")
                            ceiling = driver.find_element(By.XPATH,
                                                          "//*[@id='opportunity-container']/div/div[2]/div/div[2]/table/tbody/tr[11]/td[2]").text
                            floor = driver.find_element(By.XPATH,
                                                        "//*[@id='opportunity-container']/div/div[2]/div/div[2]/table/tbody/tr[12]/td[2]").text

                        else:
                            instrument = driver.find_element(By.XPATH,
                                                             "//*[@id='opportunity-container']/div/div[1]/div/div[1]/table/tbody/tr[6]/td[2]")
                            cat = driver.find_element(By.XPATH,
                                                      "//*[@id='opportunity-container']/div/div[1]/div/div[1]/table/tbody/tr[7]/td[2]")
                            match = driver.find_element(By.XPATH,
                                                        "//*[@id='opportunity-container']/div/div[1]/div/div[1]/table/tbody/tr[11]/td[2]")
                            ceiling = driver.find_element(By.XPATH,
                                                          "//*[@id='opportunity-container']/div/div[1]/div/div[2]/table/tbody/tr[8]/td[2]").text
                            floor = driver.find_element(By.XPATH,
                                                        "//*[@id='opportunity-container']/div/div[1]/div/div[2]/table/tbody/tr[9]/td[2]").text

                        if re.search(r'\d', ceiling):
                            ceiling = aux_str(ceiling)
                        else:
                            ceiling = 0
                        if re.search(r'\d', floor):
                            floor = aux_str(floor)
                        else:
                            floor = 0

                        temporary.append(instrument.text)
                        temporary.append(cat.text)
                        temporary.append(match.text)
                        temporary.append(ceiling)
                        temporary.append(floor)

                        driver.back()
                        time.sleep(1)
                        wait = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table")))
                        dropdown_select(driver, i)

                        index += 1
                        count = 0
                        if "UTF-8" in str(temporary) or "NHGRI" in str(temporary) or "RADx" in str(temporary) or "�" in str(temporary):
                            print("Eliminated")
                        else:
                            grant.append(temporary.copy())
                        temporary.clear()


                except:
                    print("Failed in page: " + str(i + 1))
                    print("Failed element number: " + str(index))
                    print("Failed element: " + str(element))
                    return grant

                finally:
                    count += 1

            skip_page(driver, i)
            time.sleep(1)

        return grant


# Change money to num
def aux_str(money):
    result = money.replace("$", "")
    res = result.replace(",", "")
    return res


# change pages
def skip_page(driver, num):
    if num == 0:
        skip = driver.find_element(By.XPATH,
                                   "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table/tfoot/tr/td/nav/ul/li[2]/a")
    elif num == 1:
        skip = driver.find_element(By.XPATH,
                                   "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table/tfoot/tr/td/nav/ul/li[4]/a")
    elif num == 2:
        skip = driver.find_element(By.XPATH,
                                   "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table/tfoot/tr/td/nav/ul/li[5]/a")
    else:
        skip = driver.find_element(By.XPATH,
                                   "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[3]/table/tfoot/tr/td/nav/ul/li[6]/a")

    skip.send_keys(Keys.ENTER)
    time.sleep(0.5)

def dropdown_select(driver, num):
    # Select last 4 weeks values
    dropdown = Select(driver.find_element(By.XPATH, "//*[@id='dateRange']"))
    dropdown.select_by_index(5)
    update_data = driver.find_element(By.XPATH,
                                      "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/div[2]/div[2]/div[2]/button")
    update_data.send_keys(Keys.ENTER)
    for i in range(num):
        if i >= 0:
            skip_page(driver, i)
            time.sleep(1)

if __name__ == "__main__":
    with open("Grants_data_" + str(datetime.date.today()) + ".csv", "w") as funds:
        writer = csv.writer(funds)
        result = grant_scrapper()
        writer.writerows(result)
        print("Finished")
        funds.close()
