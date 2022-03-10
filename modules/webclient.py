from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from constants import all as c


def is_returned_http_error():
    wait = WebDriverWait(c.DRIVER, 4)
    try:
        err = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'error-code')))
        return [True, err.text]
    except (ValueError, Exception) as e:
        print('Good, error-code is not found.')
        return [False, '']


class WebClient:
    def __init__(self):
        s = Service(ChromeDriverManager().install())
        c.DRIVER = webdriver.Chrome(service=s)
        c.DRIVER.get(c.URL)
