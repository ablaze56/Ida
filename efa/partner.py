from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from Constants import Constants as c

import tools.random as random
import common.menu as menu
import common.element as element
import common.dialog as dialog




def insert():
    print('Vnos partnerja')
    element.insert([
        ['NAZIV', random.stringFor(20), 'name'],
        ['NAZIV2', 'Automated test', 'name'],
        ['NASLOV', 'Poslovna cona a21', 'name'],
        ['POSTA', '4208 ŠENČUR', 'name'],
        ['DRZAVA', '4', 'name'],
        ['ZIRO_RACUN', '11111-1111111111', 'xpath']
    ])
    dialog.confirm()
