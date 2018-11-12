import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
# It is simple but useful to get cookies by manually logging in the website and setting down the cookies in local directory.
# If you have better solution to get cookies you can skip this file.
COOKIES_SAVED_PATH = r"./cookie.txt"
s = requests.session()
s.keep_alive = False
requests.adapters.DEFAULT_RETRIES = 9999
driver=webdriver.Chrome()
driver.get("https://myaccount.nytimes.com/auth/login?URI=https%3A%2F%2Fwww.nytimes.com%2F")
time.sleep(5)
input("PRess any key to continue")
cookie=driver.get_cookies()
cookie_to_save = json.dumps(cookie)
with open(COOKIES_SAVED_PATH, "w") as file:
    file.write(cookie_to_save)