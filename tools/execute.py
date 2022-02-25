# Seznam vseh taskov, ki se delijo naprej po programih

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import all as cons
from time import sleep


def execute(all_seq):

    for seq in all_seq:
        print(seq.desc)

        # if any click on previous elements in this file failed it will skip next sections
        failed_clicks = filter(lambda s: s.fileId == seq.fileId and s.sectionid < seq.sectionid and not s.success and s.type == cons.CLICK, all_seq)

        if len(list(failed_clicks)) > 0:
            print('preskoči: ', seq.desc)
        else:
            sleep(0.2)
            execute_single(seq)

    # Failed
    failed = filter(lambda s: not s.success, all_seq)
    print('Success: ', list(all_seq) - len(list(failed)), '/', len(list(all_seq)))



def execute_single(seq):
    print("Iščem: ", seq.desc)

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
        print("NAPAKA: Nisem našel")


def choose(s):
    wait = WebDriverWait(cons.DRIVER, 10)
    if len(s.id) > 0:
        return wait.until(EC.visibility_of_element_located((By.ID, s.id)))

    elif len(s.name) > 0:
        return wait.until(EC.visibility_of_element_located((By.NAME, s.name)))

    elif len(s.className) > 0:
        return wait.until(EC.visibility_of_element_located((By.CLASS_NAME, s.className)))

    elif len(s.xpath) > 0:
        return wait.until(EC.visibility_of_element_located((By.XPATH, s.xpath)))

    elif len(s.cssSelector) > 0:
        return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, s.cssSelector)))

    elif len(s.jsFunction) > 0:
        return s.jsFunction
