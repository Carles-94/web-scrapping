from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import re

#init chrome
driver = webdriver.Chrome("/Users/tutu/Desktop/python/web-scrapping/chromedriver")
#go to the web site
driver.get("https://finance.yahoo.com/quote/RDVY?p=RDVY")

#Click on the popup
element = driver.find_element_by_name("agree")
element.click()

#Get the content
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

#Get the title
title = soup.find_all("h1")[0].text
name, ticker = title.split("(")
ticker = ticker[:-1]

#Get the information of the table
allTable = soup.find_all("tbody")

#Init tr data
leftTable = allTable[0].find_all("tr")
rightTable = allTable[1].find_all("tr")
trData = leftTable + rightTable

featureList={}

featureList["name"] = name.strip()
featureList["ticker"] = ticker

for tr in trData:
    td = tr.find_all("td")
    content = (td[1].text).replace(",",".")
    featureList[td[0].text] = [content]

driver.quit()

df = pd.DataFrame(featureList) 
df.to_csv('etfs.csv', index=False, encoding='utf-8')
