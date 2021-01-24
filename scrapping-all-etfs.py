from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from collections import defaultdict


def getContentFromPage(driver, data):
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

    data["name"].append(name.strip())
    data["ticker"].append(ticker)

    for tr in trData:
        td = tr.find_all("td")
        content = (td[1].text).replace(",",".")
        data[td[0].text].append(content)
    return data

def clickOnEtf(driver, row):
    buttonTd = row.find_all("td")[0]
    button = buttonTd.find_all("a")[0]
    driver.find_element_by_link_text(button.text).click()
    #Wait the page's loading
    time.sleep(2)
    
def clickNext(driver):
    for span in driver.find_elements_by_tag_name("span"):
        if (span.text == "Next"):
            driver.execute_script("arguments[0].click();", span)

#init chrome
#TODO move this path to an external file
driver = webdriver.Chrome("/Users/tutu/Desktop/programming/python/web-scrapping/chromedriver")
#go to the web site with the search which we will scrap
driver.get("https://finance.yahoo.com/screener/etf/new")

#Click on the popup
driver.find_element_by_name("agree").click()

#Objet to save the data scrapped
data = defaultdict(list)

#search etfs
driver.find_element_by_xpath("//button[@title='★★★★★']").click()
time.sleep(2)
driver.find_element_by_xpath("//button[@title='★★★★★']").click()
time.sleep(2)
driver.find_element_by_xpath("//button[@data-test='find-stock']").click()
time.sleep(2)


while True :
    #Get the content
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    #Get the main table
    searchTable = soup.find_all("tbody")[0]
    #Iterate through all the rows
    for row in searchTable.find_all("tr"):
        #Click the button to the page the details
        clickOnEtf(driver, row)
        #Get the content
        data = getContentFromPage(driver, data)
        #Go back to the main page
        #This doesnt work TODO fix it
        driver.back()
        #Wait the page's loading
        time.sleep(2)
    try:
        clickNext(driver)
    except:
        break
    time.sleep(2)

driver.quit()

df = pd.DataFrame(data) 
df.to_csv('etfs.csv', index=False, encoding='utf-8')