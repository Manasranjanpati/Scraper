import re
import time
import urllib.parse
import lxml.html
import pandas as pd
import requests
from lxml import html
from pandas import ExcelFile
from pandas import ExcelWriter
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
import threading
from threading import Thread
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import chrome


siteurl = 'https://www.hindawi.com'
driver = webdriver.Chrome('C:\\webdriver\\chromedriver.exe')  #Give your chrome webdriver path
driver.get(siteurl)
WebDriverWait(driver, 5)
driver.maximize_window()

def search():
    driver.find_element_by_name("TxtSearchField1").send_keys("atomic engineering")  #desired keywords
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    WebDriverWait(driver, 2)
    driver.find_element_by_xpath('//*[@id="RbYearRange"]').click()
    driver.find_element_by_name("TxtYearFrom").send_keys("2017") #year range from
    driver.find_element_by_name("TxtYearTo").send_keys("2019")   #year range to
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    WebDriverWait(driver, 3)

def nextbutton():
    driver.find_element_by_link_text("next 25 articles »").click()
    WebDriverWait(driver, 5)

alltitles = list()
allnames = list()
allmails = list()

def extractor():
    getsoup = html.fromstring(driver.page_source)
    geturls = getsoup.xpath('//*[@id="SearchResultPnl"]//ul//li//a//@href')
    for uri in geturls:
        allurl = []
        allurl.append(urllib.parse.urljoin(siteurl, uri))
        for eachurl in allurl:
            eaget = requests.get(eachurl)
            makesoup = html.fromstring(eaget.content)
            alinks = makesoup.xpath("//a[contains(@class, 'coemail')]//@data-email")
            nameone = makesoup.xpath("//a[contains(@class, 'coemail')]//preceding::a[1]//span[1]//text()")
            nametwo = makesoup.xpath("//a[contains(@class, 'coemail')]//preceding::a[1]//span[2]//text()")
            title = makesoup.xpath("//h2//text()")
            for (ii, jj, kk, tit) in zip(alinks, nameone, nametwo, title):
                alltitles.append(tit)
                allmails.append(ii[::-1])
                allnames.append(jj + " " + kk)
                fullfile = pd.DataFrame({'Names': allnames, 'Mails': allmails, 'Title': alltitles})
                writer = ExcelWriter('D:\\Manas\\AtomicEngineering(hindawi17-19).xlsx') 
                fullfile.to_excel(writer, 'Sheet1', index=False)
                writer.save()
                print(jj + " " + kk, ii[::-1], tit, sep='\t')


search()
while True:
    extractor()
    nextbutton()
