# finding elements

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import all as c
from models.attribute import Attribute
from models.sequence import Sequence



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
AUTO_ORIGINAL = ''

def find_similar_elements(s):
    found_all = []
    print("Išče podobnega: ", s.attribute_value)

    if s.attribute_id == Attribute.NAME:
        found_all = (c.DRIVER.find_elements_by_name(s.attribute_value))

    elif s.attribute_id == Attribute.CLASS:
        found_all = (c.DRIVER.find_elements_by_class_name(s.attribute_value))

    elif s.attribute_id == Attribute.XPATH:
        found_all = (c.DRIVER.find_elements_by_xpath(s.attribute_value))

    elif s.attribute_id == Attribute.CSS_SELECTOR:
        found_all = (c.DRIVER.find_elements_by_css_selector(s.attribute_value))

    elif s.attribute_id == Attribute.LINK_TEXT:
        found_all = (c.DRIVER.find_elements_by_link_text(s.attribute_value))


    else:
        print('unsupported type for automated testing')

    count = 100
    ids = []

    # iterate WebElements
    for f in found_all:
        section_id = s.section_id + count
        n = Sequence(file_id=s.file_id, section_id=section_id, desc=s.desc, sequence_type=s.type,
                     attribute_id=s.attribute_id, attribute_value=s.attribute_value, insert_text=s.insert_text, wait=s.wait, find_all=False)
        n.superior_att_value=s.attribute_value

        if not isinstance(f, Sequence):
            e = str(f.get_attribute(c.ID))
            print('e: ', e)
            if len(e) > 0:
                n.attribute_value = e

        ids.append(n)
        count += 1
        print('dodal: isd', n.attribute_value)

    print('-- KONEC --')
    for a in ids:
        print(a.section_id, a.attribute_id, a.attribute_value)

    return ids