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
# time.sleep(5)
# driver.find_element_by_xpath('//*[@id="nav-packard-glow-loc-icon"]').click()
# time.sleep(5)
# if (country == 'United States (US)'):
#     driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys(zipcode)
# else:
#     driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys('10001')
# time.sleep(5)
# driver.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input').click()
# time.sleep(5)
# driver.get('https://www.amazon.com/')
# # print('\n Amazon ZIPCode:'+ driver.find_element_by_xpath('//*[@id="glow-ingress-line2"]').text)

lists =[]
for i in range (601,1001):
    # driver.get('https://www.amazon.com/' + linkStr + '&page=' + str(i)+ '&language=en_US') 
    driver.get('https://www.amazon.com/hz/leaderboard/top-reviewers/ref=cm_cr_tr_link_'+str(i)+'?page='+str(i))
    time.sleep(5)
    print(str(i)+'\n')
    for an in range(3,13):
        xpath = '//*[@id="pha-lb-page"]/div[2]/div/div/table/tbody/tr['+ str(an) +']/td[3]/a[1]'
        # print(xpath)
        driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        facebook = soup.find_all(href=re.compile('facebook.com'))
        twitter = soup.find_all(href=re.compile('twitter.com'))
        pinterest = soup.find_all(href=re.compile('pinterest.com'))
        instagram = soup.find_all(href=re.compile('instagram.com'))
        youtube = soup.find_all(href=re.compile('youtube.com'))
        flags = False
        if facebook:
            flags = True
            # break
        elif twitter:
            flags = True
            # break
        elif pinterest:
            flags = True
            # break
        elif instagram:
            flags = True
            # break
        elif youtube:
            flags = True
            # break
        if flags:
            # print(driver.current_url)
            lists.append(driver.current_url)
        driver.back()
print('\n\n\n\n\n\n\n\n\n\n')
for i in lists:
    print(i)
driver.quit()
