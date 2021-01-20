#-*-coding: utf-8 -*-
# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# pip3 install pillow selenium gitpython bs4 pandas pytz
# ssh-keygen -t rsa -C "email@github.com"
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert 
from PIL import Image
import time
import csv
import re
import sys
import datetime
import string
import os
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import sys
import xlrd

nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-')
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--disable-images')
# chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://tools.keycdn.com/geo')
time.sleep(5)
cityName = (driver.find_element_by_xpath('//*[@id="geoResult"]/div[1]/dl[1]/dd[1]').text)
zipcode = (driver.find_element_by_xpath('//*[@id="geoResult"]/div[1]/dl[1]/dd[3]').text)
country = (driver.find_element_by_xpath('//*[@id="geoResult"]/div[1]/dl[1]/dd[4]').text)
print('\n\nNow test begining country: ' + country + ' city: ' + cityName + ' Zipcode: '+ zipcode + '\n\n')

driver.get('https://www.amazon.com/?currency=USD&language=en_US')
time.sleep(5)
driver.find_element_by_xpath('//*[@id="nav-packard-glow-loc-icon"]').click()
time.sleep(5)
if (country == 'United States (US)'):
    driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys(zipcode)
else:
    driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys('10001')
time.sleep(5)
driver.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input').click()
time.sleep(5)
driver.get('https://www.amazon.com/')
print('\n Amazon ZIPCode:'+ driver.find_element_by_xpath('//*[@id="glow-ingress-line2"]').text)

driver.execute_script("document.body.style.zoom='0.9'")

counts = 0
final_result = {}

data = xlrd.open_workbook('test.xlsx')
data.sheet_names()
ASIN = ''.join(data.sheet_names())
table = data.sheet_by_index(0)
col1 = (table.col_values(0))
print("总行数：" + str(table.nrows))
print("总列数：" + str(table.ncols))
print('asin is :' + ASIN)
for i in range(len(col1)):
    col1[i] = str(col1[i]).strip()

for keys in col1:
    if (len(keys) != 0):
        lineToList = keys.split(' ')
        linkStr = 's?k='
        for a in range(len(lineToList)):
            linkStr = linkStr +lineToList[a] + '+'
        linkStr[:-1]
        counts = 1 + counts
        # driver.maximize_window()
        keyword = linkStr.replace('+', ' ')[4:]
        bandlinkStr = linkStr
        linkStr = list(linkStr)
        asinNum = linkStr.index('=') + 1
        linkStr.insert(asinNum, ASIN + '+')
        linkStr = ''.join(linkStr)
        driver.get('https://www.amazon.com/' + linkStr + '&language=en_US')
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for asin in soup.find_all(href=re.compile(ASIN)):
            links = str(asin.get('href'))
            asin_dp = 'dp/'+ASIN
            if(asin_dp in links):
                indexed = 'Y'
                break
            else:
                indexed = 'N'

        driver.get('https://www.amazon.com/' + bandlinkStr + '&language=en_US')
        time.sleep(5)
        count = driver.find_element_by_xpath('//*[@id="search"]/span/div/span/h1/div/div[1]/div/div/span[1]').text
        count = count.split(' ')[-3].replace(',','')
        soup = BeautifulSoup(driver.page_source, "html.parser")
        bandList = []
        for bands in soup.select('#brandsRefinements > ul > li > span > a > span'):
            bandList.append(bands.text)
        # print(bandList)
        if 'READY PARD' in bandList or 'READYPARD' in bandList:
            banded='Y'
        else:
            banded='N'
        print(':Keyword: '+ keyword +' :Index: '+ indexed +' :Band: '+banded+' :Number: '+ count)
        if (keyword not in final_result):
            final_result[keyword] = [0,0,0]
            final_result[keyword][0] = indexed
            final_result[keyword][1] = banded
            final_result[keyword][2] = count
driver.quit()
for k,v in final_result.items():
    print('key:',k,v)
pf = pd.DataFrame(final_result)
pf = pd.DataFrame(pf.values.T, index= pf.columns, columns=pf.index)
file_path = pd.ExcelWriter(nowTime+ASIN+'indexed.xlsx')
pf.to_excel(file_path,encoding='utf-8',index=True)
file_path.save()
