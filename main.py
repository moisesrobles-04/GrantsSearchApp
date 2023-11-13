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
    with webdriver.Safari() as driver:
        grant = []
        driver.get(link)
        wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table")))
        page_length = driver.find_element(By.XPATH,
                                          "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/thead/tr[1]/th/nav/ul/li[6]/a").text
        titles = driver.find_elements(By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/thead/tr[2]/th")
        cell = driver.find_elements(By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tbody/tr/td")
        for i in titles:
            grant.append(i.text)

        grant.append("Instrument Type")
        grant.append("Category")
        grant.append("Matching")
        grant.append("Award Ceiling")
        grant.append("Award Floor")

        for i in range(0, int(page_length)):
            index = 1
            count = 1
            temp = []
            for element in cell:
                try:

                    if count == 6 and element.text == "":
                        grant.append("2099-01-01")
                        temp.append("2099-01-01")
                    else:
                        grant.append(element.text)
                        temp.append(element.text)

                    if count == 6:
                        send = driver.find_element(By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[2]/table/tbody/tr["
                                               + str(index) + "]/td[1]/a")
                        send.send_keys(Keys.ENTER)

                        wait = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='__nuxt']/div[4]/div/div/div/div[3]")))

                        if temp.count("Forecasted") == 1:
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

                        grant.append(instrument.text)
                        grant.append(cat.text)
                        grant.append(match.text)
                        grant.append(ceiling)
                        grant.append(floor)

                        driver.back()
                        time.sleep(1)

                        index += 1
                        count = 0
                        temp.clear()


                except:
                    print("Failed in page: " + str(i+1))
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
    with open("grants.csv", "w") as funds:
        writer = csv.writer(funds)
        result = lista1()
        for i in range(0, len(result) - 10, 11):
            temp = [result[i], result[i + 1], result[i + 2], result[i + 3], result[i + 4], result[i + 5], result[i + 6],
                    result[i + 7], result[i + 8], result[i + 9], result[i + 10]]
            writer.writerow(temp)
        funds.close()

# with open("locations.csv", "r") as locations:
#     reader = csv.reader(locations)
#     header = next(reader)
#     for i in reader:
#         temp.append(i)
#
#     wb = Workbook("json.xlsx")
#     ws = wb.add_worksheet("New Sheet")
#     first_row= 0
#     result = lista1(temp)
#     order_list = ["id","type","name","name_en","area","phone","fax","hours_weekly_range","hours","event","address","city","lat","lng","distance","features"]
#     for header in order_list:
#         col = order_list .index(header)
#         ws.write(first_row, col, header)
#
#     row = 1
#
#     for jsonfiles in result:
#         for _key, _values in jsonfiles.items():
#             if(_key=='hours' or _key=='event' or _key=='features'):
#                 col = order_list.index(_key)
#                 ws.write(row, col, str(_values))
#             else:
#                 col=order_list.index(_key)
#                 ws.write(row, col, _values)
#         row+=1
#     print(len(result))
#     wb.close()
#     locations.close()
