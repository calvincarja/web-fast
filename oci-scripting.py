import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
import re
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


# 11/8/2024 - loading maps from the website
'''
improved version ** 11/8/2024
def process_url (url, keyword):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless=new") # for Chrome >= 109
    chrome_options.add_argument("--headless")
    chrome_options.headless = True # also works
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)
    body_inner_html = driver.execute_script("return document.body.innerHTML;")
    driver.quit()
    soup = BeautifulSoup(body_inner_html, 'html5lib')
    map_soup = soup.find("div", class_ = "image").find("a")
    map_soup_ahref = map_soup['href']

    if keyword in soup.get_text():
        return (url, map_soup_ahref, "missing map")
    else:
        return (url, map_soup_ahref, "map present")

def csv_to_list (csv):
    df = pd.read_csv(csv)
    oci_list = df['urls'].tolist()
    return oci_list

def scan_list (oci_list, keyword):
    text_list = []
    counter = 0 # refernce the position of the csv file

    for url in oci_list:
        try:
            result = process_url(url, keyword)
            text_list.append(result)
            counter += 1
            print(f"Prossed {url}")
        except WebDriverException as e:
            print(f"An error occurred: {e}")
        time.sleep(random.uniform(10, 12))
    return text_list

def master ():
    oci_list = csv_to_list('/Users/calvinpineda/Downloads/oci-urls.csv')
    keyword = 'image-unavailable-sm'
    text_list = scan_list(oci_list, keyword)
    print(text_list)


master()

'''
'''
# 11/8/2024 - updated version with multiple csv files

def process_url (url, keyword):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless=new") # for Chrome >= 109
    chrome_options.add_argument("--headless")
    chrome_options.headless = True # also works
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)
    body_inner_html = driver.execute_script("return document.body.innerHTML;")
    driver.quit()
    soup = BeautifulSoup(body_inner_html, 'html5lib')
    
    try:
        p_soup = soup.find("div", class_ = "col-md-8").find("p")
        if keyword in p_soup.get_text().lower():
            return (url)
        else:
            return ("No match")
    except AttributeError:
        # Log the error and return a note indicating the issue
        print(f"An error occurred while processing {url}: AttributeError")
        return (url, "error")

def csv_to_list (csv):
    df = pd.read_csv(csv)
    oci_list = df['urls'].tolist()
    return oci_list

def scan_list (oci_list, keyword):
    text_list = []
    counter = 0 # refernce the position of the csv file

    for url in oci_list:
        try:
            result = process_url(url, keyword)
            text_list.append(result)
            counter += 1
        except WebDriverException as e:
            print(f"An error occurred: {e}")
        time.sleep(random.uniform(4, 8))
    return text_list

def master ():
    csv_files = [
    '/Users/calvinpineda/Downloads/alaska.csv', 
    '/Users/calvinpineda/Downloads/south-tahiti.csv',
    '/Users/calvinpineda/Downloads/MED.csv',
    '/Users/calvinpineda/Downloads/south-america.csv',
    '/Users/calvinpineda/Downloads/caribbean.csv',
    '/Users/calvinpineda/Downloads/asia.csv',
    '/Users/calvinpineda/Downloads/australia.csv',
    '/Users/calvinpineda/Downloads/british.csv',
    '/Users/calvinpineda/Downloads/baltic.csv',
    '/Users/calvinpineda/Downloads/new-england.csv'
    ]

    keyword = 'soon'
    master_text_list = []
    counter_csv = 0

    for csv in csv_files:
        oci_list = csv_to_list(csv)
        text_list = scan_list(oci_list, keyword)
        master_text_list.extend(text_list)
        counter_csv += 1
        print(f"Processed {csv}")
        print(master_text_list)


master()



'''
'''
def csv_to_list (csv):
    df = pd.read_csv(csv)
    oci_list = df['urls'].tolist()
    return oci_list

def scan_list (oci_list):
    text_list = []

    for url in oci_list:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--headless=new") # for Chrome >= 109
            chrome_options.add_argument("--headless")
            chrome_options.headless = True # also works
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            time.sleep(5)
            body_inner_html = driver.execute_script("return document.body.innerHTML;")
            driver.quit()
            soup = BeautifulSoup(body_inner_html, 'html5lib')
            text_soup = soup.find("div", class_ = "col-sm-8") # finds the class
            text_content = text_soup.get_text(strip=True) # gets the text
            text_length = len(text_content)
            text_list.append(text_length)
            print(f"Prossed {url}")
        except WebDriverException as e:
            print(f"An error occurred: {e}")
        time.sleep(random.uniform(5, 8))
    return text_list

def master ():
    oci_list = csv_to_list('/Users/calvinpineda/Downloads/oci-collection-urls-overviews-test.csv')
    text_list = scan_list(oci_list)
    print(text_list)


master()
'''

# 12/16/24 - use HTTP request on API url

url = "https://qa1-aws.oceaniacruises.com/api/cruise-details/v1/special-offers"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

loop_breaker = 0
while loop_breaker != 1:
    response = requests.get(url, headers=headers)
    dict_response = response.json()

    for x in dict_response:
        print(x["id"])
        if x["id"] == "oceania-cruises":
            loop_breaker += 1
            print("Loop broken")
            break
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Current time: {current_time}")
    time.sleep(60)

print("Loop broken successfully")


