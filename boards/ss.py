# -*- coding: utf-8 -*-
import signal
from datetime import datetime

from selenium import webdriver

import mechanize
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import re


import selenium as se



options = se.webdriver.ChromeOptions()
options.add_argument('headless')

driver = se.webdriver.Chrome(options=options)
driver.get('https://www.weatherlink.com/embeddablePage/show/733efac978e64479ba1794851d305bb5/wide')
#driver.save_screenshot('screen.png') # save a screenshot to disk

#print(driver.page_source)


soup = BeautifulSoup(driver.page_source, "html.parser")
soup.prettify()
#print(soup)

items = soup.find_all('div', attrs={'class': 'embeddable-page-others-row'})

for i in items:
    z = i.find('div', attrs={'class': 'embeddable-page-others-label'})
    x = i.find('div', attrs={'class': 'embeddable-page-others-value col-xs-5 no-padding text-left'})
    y = i.find('div', attrs={'class': 'embeddable-page-others-desc'})


    label = re.sub("[^a-zA-Z]+", "",z.contents[0].replace('\n', '').strip())

    if label == "Wind":
        currVal = re.sub("[^0-9.]+", "", x.contents[0].replace('\n', '').strip())
        highVal = re.sub("[^0-9.]+", "", y.contents[0].replace('\n', '').strip())
        dt = datetime.now()
        break
    else:
        label="No Val"
        currVal="No Val"
        highVal="No Val"

print(dt.strftime("%m/%d/%Y, %H:%M:%S")+' : '+label + ' ' + currVal + ' : ' + highVal)
#Wind(wind_speed=currVal, highest_gust=highVal).save()
driver.close()
driver.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
driver.quit()                                      # quit the node proc