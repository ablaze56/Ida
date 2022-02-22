from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from constants import all as c


class Web_client:
    def __init__(self):
        s = Service(ChromeDriverManager().install())
        c.DRIVER = webdriver.Chrome(service=s)
        c.DRIVER.get(c.URL)
