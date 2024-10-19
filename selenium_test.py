from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
'''
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless=new") # for Chrome >= 109
chrome_options.add_argument("--headless")
chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)
start_url = "https://ncl.com"
driver.get(start_url)


driver.quit()
'''


# Automatically download and set up the latest ChromeDriver
driver = webdriver.Chrome()

# Open a test website to verify
driver.get("https://www.ncl.com")

time.sleep(15)
driver.quit
