from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

def getContentFromPage(driver):
    #Wait the page's loading
    time.sleep(5)
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

    #to navigate back
    #driver.navigate().back();

    return featureList

#init chrome
driver = webdriver.Chrome("/Users/tutu/Desktop/python/web-scrapping/chromedriver")
#go to the web site with the search which we will scrap
driver.get("https://finance.yahoo.com/screener/unsaved/7a33d557-ff00-4cc7-a821-6c571565efe2")

#Click on the popup
element = driver.find_element_by_name("agree")
element.click()
#Get the content
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

#Get the main table
searchTable = soup.find_all("tbody")[0]

#Get the first row
firstRow = searchTable.find_all("tr")[0]

#Click the button to the page the details
buttonTd = firstRow.find_all("td")[0]
button = buttonTd.find_all("a")[0]
element = driver.find_element_by_link_text(button.text)
element.click()

#Get the content
featureList = getContentFromPage(driver)

driver.quit()

df = pd.DataFrame(featureList) 
df.to_csv('etfs.csv', index=False, encoding='utf-8')