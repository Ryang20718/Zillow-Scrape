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
zillow_pleasanton_url = "https://www.zillow.com/homes/recently_sold/Pleasanton-CA/house_type/47164_rid/globalrelevanceex_sort/37.739092,-121.750317,37.583086,-122.028408_rect/11_zm/"
driver.get(zillow_pleasanton_url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
listings = soup.find_all("a", class_="zsg-photo-card-overlay-link")
listings[:5]
listings[0]['href']
'/homedetails/2804-Tangelo-Ct-Pleasanton-CA-94588/25085538_zpid/'
house_links = ['https://www.zillow.com'+row['href'] for row in listings]
next_button = soup.find_all("a", class_="on")
next_link = ['https://www.zillow.com'+row['href'] for row in next_button]


def get_house_links(url, driver, pages=20):
    house_links=[]
    driver.get(url)
    for i in range(pages):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        listings = soup.find_all("a", class_="zsg-photo-card-overlay-link")
        page_data = ['https://www.zillow.com'+row['href'] for row in listings]
        house_links.append(page_data)
        time.sleep(np.random.lognormal(0,1))
        next_button = soup.find_all("a", class_="on")
        next_button_link = ['https://www.zillow.com'+row['href'] for row in next_button]
        if i<19:
            driver.get(next_button_link[0])
    
    return house_links

def get_html_data(url, driver):
    driver.get(url)
    time.sleep(np.random.lognormal(0,1))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup
def get_price(soup):
    try:
        for element in soup.find_all(class_='estimates'):
            price = element.find_all("span")[1].text
        price = price.replace(",", "").replace("+", "").replace("$", "").lower()
        return int(price)
    except:
        return np.nan
    
def get_sale_date(soup):
    try:
        for element in soup.find_all(class_='estimates'):
            sale_date = element.find_all("span")[3].text
        sale_date = sale_date.strip()
        return sale_date
    except:
        return 'None'
    
def get_lot_size(soup):
    try:
        lot_size_regex = re.compile('Lot:')
        obj = soup.find(text=lot_size_regex).find_next()
        return obj.text
    except:
        return 'None'
def get_address(soup):
    try:
        obj = soup.find("header",class_="zsg-content-header addr").text.split(',')
        address = obj[0]
        return address
    except:
        return 'None'
def get_city(soup):
    try:
        obj = soup.find("header",class_="zsg-content-header addr").text.split(',')
        city = obj[1]
        return city
    except:
        return 'None'
    
def get_zip(soup):
    try:
        obj = soup.find("header",class_="zsg-content-header addr").text.split(',')
        list = obj[2].split()
        zip_code = list[1]
        return zip_code
    except:
        return 'None'
def get_num_beds(soup):
    try:
        obj = soup.find_all("span",class_='addr_bbs')
        beds = obj[0].text.split()[0]
        return beds
    except:
        return 'None'
    
def get_num_baths(soup):
    try:
        obj = soup.find_all("span",class_='addr_bbs')
        beds = obj[1].text.split()[0]
        return beds
    except:
        return 'None'
    
def get_floor_size(soup):
    try:
        obj = soup.find_all("span",class_='addr_bbs')
        floor_size_string = obj[2].text.split()[0]
        floor_size = floor_size_string.replace(",","")
        return floor_size
    except:
        return 'None'
    
def get_year_built(soup):
    try:
        objs = soup.find_all("span",class_='hdp-fact-value')
        built_in_regex = re.compile('Built in')
        for obj in objs:
            out = obj.find(text=built_in_regex)
            if out is not None:
                return out
    except:
        return 'None'
    
def flatten_list(house_links):
    house_links_flat=[]
    for sublist in house_links:
        for item in sublist:
            house_links_flat.append(item)
    return house_links_flat
def get_house_data(driver,house_links_flat):
    house_data = []
    for link in house_links_flat:
        soup = get_html_data(link,driver)
        address = get_address(soup)
        city = get_city(soup)
        zip_code = get_zip(soup)
        beds = get_num_beds(soup)
        baths = get_num_baths(soup)
        floor_size = get_floor_size(soup)
        lot_size = get_lot_size(soup)
        year_built = get_year_built(soup)
        sale_date = get_sale_date(soup)
        price = get_price(soup)
        house_data.append([address,city,zip_code,beds,baths,    floor_size,lot_size,year_built,sale_date,price])
    return house_data

house_links_10pages = get_house_links(zillow_pleasanton_url,driver,pages=10)
house_links_flat = flatten_list(house_links_10pages)
house_data_10pages = get_house_data(driver,house_links_flat)

file_name = "%s_%s.csv" % (str(time.strftime("%Y-%m-%d")), 
                           str(time.strftime("%H%M%S")))
columns = ["address", "city", "zip", "bedrooms", "bathrooms", "floor_size", "lot_size", "year_built", "sale_date", "sale_price"]
pd.DataFrame(house_data_10pages, columns = columns).to_csv(
    file_name, index = False, encoding = "UTF-8"
)
