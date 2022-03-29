# finding elements
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from constants import all as c
from models.attribute import Attribute
from models.sequence import Sequence
from time import sleep


def wait_until_visible(s):
    wait = WebDriverWait(c.DRIVER, 10)

    if s.attribute_id == Attribute.ID:
        return wait.until(EC.visibility_of_element_located((By.ID, s.attribute_value)))

    elif s.attribute_id == Attribute.NAME:
        return wait.until(EC.visibility_of_element_located((By.NAME, s.attribute_value)))

    elif s.attribute_id == Attribute.CLASS:
        return wait.until(EC.visibility_of_element_located((By.CLASS_NAME, s.attribute_value)))

    elif s.attribute_id == Attribute.XPATH:
        return wait.until(EC.visibility_of_element_located((By.XPATH, s.attribute_value)))

    elif s.attribute_id == Attribute.CSS_SELECTOR:
        return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, s.attribute_value)))

    elif s.attribute_id == Attribute.LINK_TEXT:
        return wait.until(EC.visibility_of_element_located((By.LINK_TEXT, s.attribute_value)))

    elif s.attribute_id == Attribute.JS_FUNCTION:
        return s.attribute_value


def find_similar_elements(s):
    found_all = []

    if s.attribute_id == Attribute.NAME:
        found_all = (c.DRIVER.find_elements_by_name(s.superior_att_value))

    elif s.attribute_id == Attribute.CLASS:
        found_all = (c.DRIVER.find_elements_by_class_name(s.superior_att_value))

    elif s.attribute_id == Attribute.XPATH:
        found_all = (c.DRIVER.find_elements_by_xpath(s.superior_att_value))

    elif s.attribute_id == Attribute.CSS_SELECTOR:
        found_all = (c.DRIVER.find_elements_by_css_selector(s.superior_att_value))

    elif s.attribute_id == Attribute.LINK_TEXT:
        found_all = (c.DRIVER.find_elements_by_link_text(s.superior_att_value))

    else:
        print('unsupported type for automated testing')

    count = 100
    ids = []

    # iterate WebElements
    for f in found_all:
        section_id = s.section_id + count

        if not isinstance(f, Sequence):
            e = str(f.get_attribute(c.ID))
            if len(e) > 0:
                # replace similar for finding this element
                splitted = s.attribute_value.split("'")
                if len(splitted) != 3:
                    print('Error handling automated menu testing..')
                    break

                val = splitted[0] + "'" + e + "'" + splitted[2]
                desc = f'{s.desc}'
                if '#auto' not in desc:
                    desc = f'{s.desc} #auto'
                n = Sequence(file_id=s.file_id, section_id=section_id, desc=desc, sequence_type=s.type,
                             attribute_id=c.XPATH, attribute_value=val, insert_text=s.insert_text, wait=s.wait,
                             auto_find=False)
                n.auto_find = True

        ids.append(n)
        count += 1

    return ids


def escape_send():

    try:
        WebDriverWait(c.DRIVER, 1).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'dx-popup-content')))
        print('NAŠEL')
        sleep(0.5)
        webdriver.ActionChains(c.DRIVER).send_keys(Keys.ESCAPE).perform()
       # b.click()
       # sleep(1.5)

    except TimeoutException:
        print('no alert present')


  #  try:
  #      WebDriverWait(c.DRIVER, 0.5).until(
  #          EC.visibility_of_element_located((By.CSS_SELECTOR, 'div > div > div.dx-toolbar.dx-widget.dx-visibility-change-handler.dx-collection.dx-popup-title.dx-has-close-button > div > div.dx-toolbar-after > div > div > div > div > i')))
  #      print('ALERT PRESENT')
  #      webdriver.ActionChains(c.DRIVER).send_keys(Keys.ESCAPE).perform()
  #      sleep(1)
  #
  #  except TimeoutException as e:
  #      print('no alert present')





