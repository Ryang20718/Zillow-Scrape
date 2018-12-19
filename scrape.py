import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import numpy as np
import pandas as pd
import regex as re

driver = webdriver.Chrome()
url = "https://www.redfin.com/zipcode/92130"
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
button = driver.find_elements_by_xpath("////////span[@data-rf-test-name='tableOption']")[1]
button.click()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
listings = soup.find_all("tr", class_="tableRow")
print(listings)

#for i in listings:
   # print(i.get_text())
