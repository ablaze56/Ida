# finding elements
from selenium import webdriver
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
    print("Išče podobnega: ", s.superior_att_value)

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
                desc = f'{s.desc} #auto {count - 99}/{len(found_all)}'
                n = Sequence(file_id=s.file_id, section_id=section_id, desc=desc, sequence_type=s.type,
                             attribute_id=c.XPATH, attribute_value=val, insert_text=s.insert_text, wait=s.wait,
                             find_all=False)

        ids.append(n)
        count += 1

    return ids


def escape_send():
    sleep(1)
    webdriver.ActionChains(c.DRIVER).send_keys(Keys.ESCAPE).perform()
