import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# build out the structure for one url
'''
driver = webdriver.Chrome()

oci_url = "https://qa1-aws.oceaniacruises.com/caribbean-cruises/miami-to-miami-VIS241205/"
driver.get(oci_url)

time.sleep(10)

body_inner_html = driver.execute_script("return document.body.innerHTML;") #entire HTML as a string, no need for .text

driver.quit()
soup = BeautifulSoup(body_inner_html, 'html5lib')
keyword = "ultimate"
if keyword in soup.get_text():
    print(f"found keyword {keyword}")
else:
    print("keyword not found")
'''

'''
# above was succesfull, now load into a list
urls = []
driver = webdriver.Chrome()

oci_url = "https://qa1-aws.oceaniacruises.com/caribbean-cruises/miami-to-miami-VIS241205/"
driver.get(oci_url)

time.sleep(10)

body_inner_html = driver.execute_script("return document.body.innerHTML;") #entire HTML as a string, no need for .text

driver.quit()
soup = BeautifulSoup(body_inner_html, 'html5lib')
find_map = soup.find("div", class_ = "image").find("a") #it finds it - now extract the href

if find_map:
    print(True)
    anchor_tag = find_map['href']
    print(anchor_tag)
else:
    print(None)

keyword = "image-unavailable-sm"
if keyword in soup.get_text():
    urls.append((oci_url, anchor_tag, "Map mising"))
else:
    urls.append((oci_url, anchor_tag, "Map is present"))

print("complete")
print(urls)
'''

'''
# load the map urls into a folder on my desktop - update 10/17/2024
def csv_to_list (csv):
    df = pd.read_csv(csv)
    oci_list = df['urls'].tolist()
    return oci_list

def downlaod_maps (oci_list):
    for url in oci_list:
        try:
            response = requests.get(url)
            response.raise_for_status()

            # generate a filename from url
            img_name = os.path.basename(url)

'''

'''

# find image not avalible map urls only - update 10/14/2024
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
            map_soup = soup.find("div", class_ = "image").find("a")
            map_soup_ahref = map_soup['href']
            text_list.append((url, map_soup_ahref))
            print(f"Prossed {url}")
            print(text_list)
        except WebDriverException as e:
            print(f"An error occurred: {e}")
        time.sleep(random.uniform(2, 4))
    return text_list



def list_to_txt (text_list, file_path):
    try:
        with open(file_path, 'w') as file:
            for item in text_list:
                file.write(str(item) + '\n')
        return True, f"data sucessfully saved to {file_path}" # returns two items
    except IOError as e:
        return False, f"an error as occurred while writing to the file: {e}"

def master ():
    oci_list = csv_to_list('/Users/calvinpineda/Downloads/collection-map-urls-segment.csv')
    text_list = scan_list(oci_list)
    print('complete')

master()


'''

'''
def csv_to_list (csv):
    df = pd.read_csv(csv)
    oci_list = df['urls'].tolist()
    return oci_list

def scan_list (oci_list, keyword):
    text_list = []
    counter = 0 # refernce the position of the csv file

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
            map_soup = soup.find("div", class_ = "image").find("a")
            map_soup_ahref = map_soup['href']

            if keyword in soup.get_text():
                text_list.append((url, map_soup_ahref, "missing map"))
            else:
                text_list.append((url, map_soup_ahref, "map present"))
            
            counter += 1
            print(f"Prossed {url}")
        except WebDriverException as e:
            print(f"An error occurred: {e}")
        time.sleep(random.uniform(10, 12))
    return text_list

def master ():
    oci_list = csv_to_list('/Users/calvinpineda/Downloads/oci-urls.csv')
    keyword = 'image-unavailable-sm'
    # file_path = '/Users/calvinpineda/Downloads/collection-map-urls.txt'
    text_list = scan_list(oci_list, keyword)
    print(text_list)


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


'''
if keyword in soup.get_text():
    urls.append((oci_url, element_html, "image-unavailable present"))
        print(f"Processed {url} - voyage map not found")
          #else:
            #store_urls.append(url, element_html, "voyage map present")
            #print(f"Processed {url} - voyage map found")

'''

"""
inner_text = elements.text
print(inner_text)

inner_html = elements.decode_contents()
print(inner_html)
"""


"""

def extract (url, keyword):
    store_bad_urls = []
    store_urls = []
    try:
          response_url = requests.get(url)
          response_url.raise_for_status()
          response_url_text = response_url.text
          response_url_text_readble = BeautifulSoup(response_url_text, 'html5lib')
          print(response_url_text_readble)
          elements = response_url_text_readble.find("div", element_class = "image") # only one image so lets try find (not find_all)
          print(elements)
          print('10')
          #for element in elements:
            #print("Text:", element.text)
            #print("HTML Content:", element.decode_contents())
          #if keyword in response_url_text_readble:
            #store_urls.append((url, element_html, "image-unavailable present"))
            #print(f"Processed {url} - voyage map not found")
          #else:
            #store_urls.append(url, element_html, "voyage map present")
            #print(f"Processed {url} - voyage map found")
        
    except requests.exceptions.RequestException as e:
        store_bad_urls.append((url, str(e)))
        print(f"Error Processing {url}: {e}")

extract(oci_url, keyword)

"""
# loading target
driver = webdriver.Chrome()

# Open a test website to verify
driver.get("https://www.target.com")

time.sleep(5)
driver.quit