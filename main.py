import csv
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

link = "https://www.grants.gov/search-grants"


# Limit search to 1-6 months
# length of 6

def lista1():
    with webdriver.Chrome() as driver:
        grant = []
        titles_list = []
        driver.get(link)
        wait = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table")))
        time.sleep(2)
        page_length = driver.find_element(By.XPATH,
                                          "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/thead/tr[1]/th/nav/ul/li[6]/a").text
        titles = driver.find_elements(By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/thead/tr[2]/th")
        cell = driver.find_elements(By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tbody/tr/td")
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
        # size = 1

        for i in range(0, size):
            #skip pages
            # if i<93:
            #     if i == 0:
            #         next = driver.find_element(By.XPATH,
            #                                "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tfoot/tr/td/nav/ul/li[2]/a")
            #     elif i == 1:
            #         next = driver.find_element(By.XPATH,
            #                                "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tfoot/tr/td/nav/ul/li[4]/a")
            #     elif i == 2:
            #         next = driver.find_element(By.XPATH,
            #                                "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tfoot/tr/td/nav/ul/li[5]/a")
            #     else:
            #         next = driver.find_element(By.XPATH,
            #                                "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tfoot/tr/td/nav/ul/li[6]/a")
            #
            #     next.send_keys(Keys.ENTER)
            #     time.sleep(0.5)
            #     continue

            index = 1
            count = 1
            temporary = []
            for element in cell:
                try:
                    if count < 6:
                        temporary.append(element.text)

                    else:
                        att = element.get_attribute("innerHTML").split("<")
                        att = att[1].split(">")
                        if att[1] == "no data":
                            temporary.append("2099-01-01")
                        else:
                          temporary.append(att[1])

                        send = driver.find_element(By.XPATH,
                                                   "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tbody/tr["
                                                   + str(index) + "]/td[1]/a")
                        send.send_keys(Keys.ENTER)

                        wait = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[3]")))
                        time.sleep(1)

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

                        index += 1
                        count = 0
                        if "UTF-8" in str(temporary) or "NHGRI" in str(temporary) or "RADx" in str(temporary):
                            print("Eliminated")
                        else:
                            grant.append(temporary.copy())
                        temporary.clear()


                except:
                    print("Failed in page: " + str(i + 1))
                    print("Failed element number: " + str(index))
                    return grant

                finally:
                    count += 1

            if i == 0:
                next = driver.find_element(By.XPATH,
                                           "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tfoot/tr/td/nav/ul/li[2]/a")
            elif i == 1:
                next = driver.find_element(By.XPATH,
                                           "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tfoot/tr/td/nav/ul/li[4]/a")
            elif i == 2:
                next = driver.find_element(By.XPATH,
                                           "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tfoot/tr/td/nav/ul/li[5]/a")
            else:
                next = driver.find_element(By.XPATH,
                                           "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tfoot/tr/td/nav/ul/li[6]/a")

            next.send_keys(Keys.ENTER)
            time.sleep(2)

        return grant


def aux_str(money):
    result = money.replace("$", "")
    res = result.replace(",", "")
    return res


if __name__ == "__main__":
    with open("./data/test.csv", "w") as funds:
        writer = csv.writer(funds)
        result = lista1()
        writer.writerows(result)
        print("Finished")
        funds.close()
