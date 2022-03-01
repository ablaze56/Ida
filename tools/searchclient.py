# finding elements

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import all as c
from models.attribute import Attribute



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


# elements with similar attribute, i.e. menus
def find_similar_elements(s):
    found_all = []

    if s.attribute_id == Attribute.NAME:
        found_all = c.DRIVER.find_elements_by_name(s.attribute_value)

    elif s.attribute_id == Attribute.CLASS:
        found_all = c.DRIVER.find_elements_by_class_name(s.attribute_value)

    elif s.attribute_id == Attribute.XPATH:
        found_all = c.DRIVER.find_elements_by_xpath(s.attribute_value)

    elif s.attribute_id == Attribute.CSS_SELECTOR:
        found_all = c.DRIVER.find_elements_by_css_selector(s.attribute_value)

    elif s.attribute_id == Attribute.LINK_TEXT:
        found_all = c.DRIVER.find_elements_by_link_text(s.attribute_value)

    else:
        print('unsupported type for automated testing')

    count = 100
    ids = []
    for f in found_all:
        e = str(f.get_attribute(c.ID))
        if len(e) > 0:
            n = s
            n.attribute_id = c.ID
            n.section_id += count
            n.attribute_value = e
            ids.append(n)
            count += 1

    return ids