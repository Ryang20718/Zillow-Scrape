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
zillow_pleasanton_url = "https://www.trulia.com/CA/San_Diego/92130"
driver.get(zillow_pleasanton_url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
