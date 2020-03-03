# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone
from boards.models import Wind

import signal
from datetime import datetime

from selenium import webdriver

import mechanize
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import re

import selenium as se


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_data(self):

        for i in range(420):
            options = se.webdriver.ChromeOptions()
            options.add_argument('headless')

            driver = se.webdriver.Chrome(options=options)
            driver.get('https://www.weatherlink.com/embeddablePage/show/733efac978e64479ba1794851d305bb5/wide')
            # driver.save_screenshot('screen.png') # save a screenshot to disk

            # print(driver.page_source)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            soup.prettify()
            # print(soup)

            items = soup.find_all('div', attrs={'class': 'embeddable-page-others-row'})

            prevWind = int(0)
            prevGust = int(0)
            for i in items:
                z = i.find('div', attrs={'class': 'embeddable-page-others-label'})
                x = i.find('div', attrs={'class': 'embeddable-page-others-value col-xs-5 no-padding text-left'})
                y = i.find('div', attrs={'class': 'embeddable-page-others-desc'})

                label = re.sub("[^a-zA-Z]+", "", z.contents[0].replace('\n', '').strip())

                if label == "Wind":
                    try:
                        currValStr = re.sub("[^0-9.]+", "", x.contents[0].replace('\n', '').strip())
                        highValStr = re.sub("[^0-9.]+", "", y.contents[0].replace('\n', '').strip())

                        currVal = int(currValStr)
                        highVal = int(highValStr)
                        prevGust = highVal
                        prevWind = currVal
                    except ValueError:
                        currVal = prevWind
                        highVal = prevGust
                        print('Error-')

                    if highVal + currVal != 0:
                        Wind(wind_speed=currVal, highest_gust=highVal).save()
                    dt = datetime.now()
                    print(dt.strftime("%m/%d/%Y, %H:%M:%S") + ' : ' + label + ' ' + str(currVal) + ' : ' + str(highVal))

                    break
                else:
                    label = "No Val"
                    currVal = int(0)
                    highVal = int(0)

            driver.close()
            driver.service.process.send_signal(signal.SIGTERM)  # kill the specific phantomjs child proc
            driver.quit()

            sleep(15)

    def handle(self, *args, **options):
        self._create_data()
