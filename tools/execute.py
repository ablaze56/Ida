
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import all as cons
from models.attribute import Attribute
from time import sleep
from models.type import Type

AUTO_COUNTER = 1000
AUTO_SEQ = []
FAILED_AUTO_SEQ = []


def execute(all_seq):
    for seq in all_seq:
        # if any click on previous elements in this file failed it will skip next sections
        failed_clicks = filter(lambda
                                   s: s.file_id == seq.file_id and s.section_id < seq.section_id and not s.success and s.type == cons.CLICK,
                               all_seq)

        if len(list(failed_clicks)) > 0:
            print('skip for failed click: ', seq.desc)
        else:
            # search all occurrences in then execute them all
            if seq.findAll:
                find_and_execute_auto(seq)
            else:
                execute_single(seq)
                sleep(seq.wait)

    # Failed
    failed = filter(lambda s: not s.success, all_seq)
    count_all = len(list(all_seq))
    count_failed = len(list(failed))
    print('Success: ', count_all - count_failed, '/', count_all)


def find_and_execute_auto(s):
    print("Locating main auto sequence... ", s.desc)
    try:
        elements = choose(s)
        recursive_search(elements, s)
        s.success = True
        print("Ok")

    except:
        print("ERROR: not found")


def recursive_search(elements, main_sequence):
    global AUTO_COUNTER, AUTO_SEQ, FAILED_AUTO_SEQ

    for e in elements:
        e_name = e.get_attribute(cons.NAME)
        if e_name in AUTO_SEQ:
            print(f'{e_name} already ran, skip.')
            continue

        new = main_sequence
        new.section_id += AUTO_COUNTER
        e_id = e.get_attribute(e.attribute_id)
        new.attribute_value = e_id
        new.success = False

        AUTO_SEQ.append(e_name)
        AUTO_COUNTER += 1

        if new.type == cons.CLICK:
            new.click()

            try:
                elements = choose(new)
                recursive_search(elements, main_sequence)
                new.success = True
                sleep(new.wait)
                print("Ok")

            except:
                FAILED_AUTO_SEQ.append(e_name)

                if is_returned_http_error():
                    print('CRITICAL ERROR')
                    break
                else:
                    print("ERROR: Not found")



def execute_single(seq):
    print("Locating... ", seq.desc)

    try:
        element = choose(seq)
        seq.success = True
        print("Ok")

        if seq.type == Type.CLICK:
            element.click()
        elif seq.type == Type.INPUT:
            if len(seq.insert_text) > 0:
                element.send_keys(seq.insert_text)
        else:
            print("seq.type: ", seq.type)
    except:

        if is_returned_http_error():
            print('CRITICAL ERROR')
        else:
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

    elif s.attribute_id == Attribute.LINK_TEXT:
        return wait.until(EC.visibility_of_element_located((By.LINK_TEXT, s.attribute_value)))

    elif s.attribute_id == Attribute.JS_FUNCTION:
        return s.attribute_value


def is_returned_http_error():
    wait = WebDriverWait(cons.DRIVER, 4)
    try:
        err = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'error-code')))
        print(err)
        return True
    except:
        return False
