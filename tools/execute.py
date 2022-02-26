# Seznam vseh taskov, ki se delijo naprej po programih

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import all as cons
from models.attribute import Attribute
from time import sleep


def execute(all_seq):

    for seq in all_seq:
        # if any click on previous elements in this file failed it will skip next sections
        failed_clicks = filter(lambda s: s.file_id == seq.file_id and s.section_id < seq.section_id and not s.success and s.type == cons.CLICK, all_seq)

        if len(list(failed_clicks)) > 0:
            print('skip for failed click: ', seq.desc)
        else:
            execute_single(seq)
            sleep(seq.wait)

    # Failed
    failed = filter(lambda s: not s.success, all_seq)
    count_all = len(list(all_seq))
    count_failed = len(list(failed))
    print('Success: ', count_all - count_failed, '/', count_all)


def execute_single(seq):
    print("Locating... ", seq.desc)

    try:
        element = choose(seq)
        seq.success = True
        print("Ok")

        if seq.type == cons.CLICK:
            element.click()
        elif seq.type == cons.INPUT:
            if len(seq.text) > 0:
                element.send_keys(seq.text)
    except:
        print("ERROR: Not found")


def choose(s):
    wait = WebDriverWait(cons.DRIVER, 10)

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

    elif s.attribute_id == Attribute.JS_FUNCTION:
        return s.attribute_value
