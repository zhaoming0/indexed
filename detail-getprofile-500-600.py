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
# time.sleep(15)
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

final_result = {}
for i in range (500,601):
    driver.get('https://www.amazon.com/hz/leaderboard/top-reviewers/ref=cm_cr_tr_link_'+str(i)+'?page='+str(i))
    time.sleep(5)
    print(str(i))
    for an in range(3,13):
        helpfulPercentPath = '//*[@id="pha-lb-page"]/div[2]/div/div/table/tbody/tr['+ str(an) + ']/td[6]'
        helpfulVotesPath = '//*[@id="pha-lb-page"]/div[2]/div/div/table/tbody/tr['+str(an)+']/td[5]'
        reviewsPath = '//*[@id="pha-lb-page"]/div[2]/div/div/table/tbody/tr['+str(an)+']/td[4]'
        reviews = driver.find_element_by_xpath(reviewsPath).text
        if reviews != 0:
            helpfulPer = driver.find_element_by_xpath(helpfulPercentPath).text
            helpfulVotes = driver.find_element_by_xpath(helpfulVotesPath).text
            xpath = '//*[@id="pha-lb-page"]/div[2]/div/div/table/tbody/tr['+ str(an) +']/td[3]/a[1]'
            driver.find_element_by_xpath(xpath).click()
            time.sleep(3)
            hearts =       driver.find_element_by_xpath('//*[@id="profile_v5"]/div/div/div[4]/div[2]/div[1]/div[2]/div/div[3]/a/div/div[1]/span').text
            idealists =    driver.find_element_by_xpath('//*[@id="profile_v5"]/div/div/div[4]/div[2]/div[1]/div[2]/div/div[4]/a/div/div[1]/span').text
        else:
            helpfulPer = 0
            helpfulVotes = 0
            xpath = '//*[@id="pha-lb-page"]/div[2]/div/div/table/tbody/tr['+ str(an) +']/td[3]/a[1]'
            driver.find_element_by_xpath(xpath).click()
            time.sleep(3)
            hearts = 0
            idealists = 0

        soup = BeautifulSoup(driver.page_source, "html.parser")
        facebook = soup.find_all(href=re.compile('facebook.com'))
        twitter = soup.find_all(href=re.compile('twitter.com'))
        pinterest = soup.find_all(href=re.compile('pinterest.com'))
        instagram = soup.find_all(href=re.compile('instagram.com'))
        youtube = soup.find_all(href=re.compile('youtube.com'))
        # get vine badge
        vineBadge = False
        for vine in soup.find_all(href=re.compile('nodeId=14279681')):
            if 'badge_VINE_VOICE' in str(vine):
                vineBadge = True

        number = soup.find_all(href=re.compile('top-reviewers'))
        rank = str(number).split('#')[0].split('=')[-1]
        userName = str(number).split('#')[1].split('"')[0]
        if userName not in final_result:
            final_result[userName] = {}
            final_result[userName]['rank']=rank
            final_result[userName]['Vine']= vineBadge
            final_result[userName]['helpPer'] = helpfulPer
            final_result[userName]['helpfulVotes'] = helpfulVotes
            final_result[userName]['reviews'] = reviews
            final_result[userName]['hearts'] = hearts
            final_result[userName]['idealists'] = idealists
            
        if facebook:
            results = str(facebook).split(' ')[1].split("=")[1].strip('"')
            final_result[userName]['FB'] = results

        if twitter:
            results = str(twitter).split(' ')[1].split("=")[1].strip('"')
            final_result[userName]['TW'] = results

        if pinterest:
            results = str(pinterest).split(' ')[1].split("=")[1].strip('"')
            final_result[userName]['PIN'] = results

        if instagram:
            results = str(instagram).split(' ')[1].split("=")[1].strip('"')
            final_result[userName]['INS'] = results

        if youtube:
            results = str(youtube).split(' ')[1].split("=")[1].strip('"')
            final_result[userName]['YTB'] = results

        driver.back()

for i,j in final_result.items():
    if i:
        print(i,j)
driver.quit()

pf = pd.DataFrame(final_result)
pf = pd.DataFrame(pf.values.T, index= pf.columns, columns=pf.index)
file_path = pd.ExcelWriter('facebook-500-600.xlsx')
pf.to_excel(file_path,encoding='utf-8',index=True)
file_path.save()
