#-*-coding: utf-8 -*-
# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
#pip3 install pillow selenium
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

nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-images')
chrome_options.add_argument('--start-maximized')

# prefs = {'profile.managed_default_content_settings.images': 2}
# chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.amazon.com/?currency=USD&language=en_US')

counts = 0
with open('test.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:       
        lineToStr = row[0]
        lineToList = lineToStr.split(' ')
        linkStr='s?k='
        for i in range(len(lineToList)):
            linkStr= linkStr + lineToList[i] + '+'
        linkStr= linkStr[:-1]
        driver.maximize_window()
        counts = 1 + counts
        flags = False
        keyword = linkStr.replace('+', ' ')[4:]
        print(str(counts) + ' for  keyword: ' + keyword)
        driver.get('https://www.amazon.com/' + linkStr + '&language=en_US')
        soup = BeautifulSoup(driver.page_source, "html.parser")
        bandList = []
        for bands in soup.select('#brandsRefinements > ul > li > span > a > span'):
            bandList.append(bands.text)
        print(bandList)
        if 'READY PARD' in bandList:
            print(keyword, '-Y-band')
        else:
            print(keyword, '-N-band')
        break

driver.quit()
