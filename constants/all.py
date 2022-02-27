from pathlib import Path
from selenium import webdriver

DRIVER: webdriver

# ali dela na winsih
FOLDER = Path('./library')
URL = ''

USER_CONSTANTS = []

# types of sequences
CLICK = 'click'
INPUT = 'input'
FUNCTION = 'function'
COMMON = 'common'
USER_CONSTANT = 'userConstant'

# json elements

SEARCH = 'search'

SKIP = 'skip'

DESC = 'desc'
ID = 'id'
NAME = 'name'
CLASS = 'class'
TYPE = 'type'
INSERT_TEXT = 'insertText'
XPATH = 'xpath'
CSS_SELECTOR = 'css_selector'
WAIT = 'wait'
