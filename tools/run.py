# Seznam vseh taskov, ki se delijo naprej po programih

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import all as c


def run(seq):
    try:
        element = choose(seq)

        if seq.type == 'click':
            element.click()
        elif seq.type == 'input':
            if len(seq.input) > 0:
                element.send_keys(seq.input)
    except:
        print("Nisem našel: ", seq.desc)


def choose(s):
    wait = WebDriverWait(c.DRIVER, 10)
    if len(s.id) > 0:
        return wait.until(EC.visibility_of_element_located((By.ID, s.id)))

    elif len(s.name) > 0:
        return wait.until(EC.visibility_of_element_located((By.NAME, s.name)))

    elif len(s.className) > 0:
        return wait.until(EC.visibility_of_element_located((By.CLASS_NAME, s.className)))

    elif len(s.containsText) > 0:
        xp = f"//*[contains(text(), '{s.containsText}')]"
        return wait.until(EC.visibility_of_element_located((By.XPATH, xp)))

    elif len(s.containsID) > 0:
        xp = f"//*[contains(@id, '{s.containsID}')]"
        return wait.until(EC.visibility_of_element_located((By.XPATH, xp)))
