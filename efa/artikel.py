from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from Constants import Constants as c

import tools.random as random
#import common.menu as menu
import common.element as element
import common.dialog as dialog




def insert():
    print('Vnos artikla')
    element.insert([
        ['SIFRA', random.numberFor(12), 'name'],
        ['NAZIV', random.stringFor(20), 'name'],
        ['NAZIV2', 'Automated test', 'name'],
        ['ENOTA', 'KOS', 'name'],
        ['GRUPA', '1', 'name'],
        ['PRODAJNA_CENA', '12.20', 'xpath'],
        ['KODA', random.numberFor(12), 'name']
    ])
    dialog.confirm()

def edit():
    print('Popravi artikel')
    #print(c.DRIVER.text)
    wait = WebDriverWait(c.DRIVER, 10)

  #  el = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'dx-row dx-data-row dx-row-lines dx-row-focused dx-cell-focus-disabled')))
  #  print('el: ', el.text)


  #  xpath = "//td[@class='dx-row dx-data-row dx-row-lines dx-row-focused dx-cell-focus-disabled']"
   # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, e[0])))

    xpath = "//*[contains(@class, 'dx-scrollable-container')]"
    el = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    print('el: ', el.containsText)
    el.click()
    el.insert(['NAZIV', random.stringFor(20), 'name'])
    dialog.confirm()

