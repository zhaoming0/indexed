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
import shutil

nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-')
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-images')
# chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get('https://www.amazon.com/?currency=USD&language=en_US')

count=1
file_path = 'topReviewer.xlsx'
begin = 1
end = 1001
if os.path.exists(file_path):
    newPath = nowTime+file_path
    # shutil.copy(file_path,newPath)
    lastLine = pd.read_excel(file_path)
    lastLine = lastLine.iloc[-1]['rank']
    begin = (lastLine // 10)
else:
    count = 0


for i in range (begin,end):
    driver.get('https://www.amazon.com/hz/leaderboard/top-reviewers/ref=cm_cr_tr_link_'+str(i)+'?page='+str(i))
    time.sleep(5)
    print(str(i))
    tmpResultDic={}
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
            time.sleep(5)
            hearts =       driver.find_element_by_xpath('//*[@id="profile_v5"]/div/div/div[4]/div[2]/div[1]/div[2]/div/div[3]/a/div/div[1]/span').text
            idealists =    driver.find_element_by_xpath('//*[@id="profile_v5"]/div/div/div[4]/div[2]/div[1]/div[2]/div/div[4]/a/div/div[1]/span').text
        else:
            helpfulPer = 0
            helpfulVotes = 0
            xpath = '//*[@id="pha-lb-page"]/div[2]/div/div/table/tbody/tr['+ str(an) +']/td[3]/a[1]'
            driver.find_element_by_xpath(xpath).click()
            time.sleep(5)
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

        tmpResultDic[userName] = {}
        tmpResultDic[userName]['rank']=rank
        tmpResultDic[userName]['Vine']= vineBadge
        tmpResultDic[userName]['helpPer'] = helpfulPer
        tmpResultDic[userName]['helpfulVotes'] = helpfulVotes
        tmpResultDic[userName]['reviews'] = reviews
        tmpResultDic[userName]['hearts'] = hearts
        tmpResultDic[userName]['idealists'] = idealists
            
        if facebook:
            results = str(facebook).split(' ')[1].split("=")[1].strip('"')
            tmpResultDic[userName]['FB'] = results

        if twitter:
            results = str(twitter).split(' ')[1].split("=")[1].strip('"')
            tmpResultDic[userName]['TW'] = results

        if pinterest:
            results = str(pinterest).split(' ')[1].split("=")[1].strip('"')
            tmpResultDic[userName]['PIN'] = results

        if instagram:
            results = str(instagram).split(' ')[1].split("=")[1].strip('"')
            tmpResultDic[userName]['INS'] = results

        if youtube:
            results = str(youtube).split(' ')[1].split("=")[1].strip('"')
            tmpResultDic[userName]['YTB'] = results

        driver.back()

    if count == 0:
        pff = pd.DataFrame(tmpResultDic)
        pff = pd.DataFrame(pff.values.T, index= pff.columns, columns=pff.index)
        files = pd.ExcelWriter(file_path)
        pff.to_excel(files,encoding='utf-8',index=True)
        files.save()
    else:
        old = pd.read_excel(file_path,index_col=0)
        news =  pd.DataFrame(tmpResultDic)
        news = pd.DataFrame(news.values.T, index= news.columns, columns=news.index)
        old = old.append(news)
        old = pd.DataFrame(old)
        files = pd.ExcelWriter(file_path)
        old.to_excel(files,encoding='utf-8',index=True)
        files.save() 
    count+=1
driver.quit()

