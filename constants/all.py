from pathlib import Path
from selenium import webdriver

DRIVER: webdriver

FOLDER = Path('./library')
LOG_FOLDER = Path('./reports')

URL = ''

USER_CONSTANTS = []

# types of sequences
CLICK = 'click'
INPUT = 'input'
FUNCTION = 'function'
COMMON = 'common'
USER_CONSTANT = 'userConstant'
LINK_TEXT = 'linkText'

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


# VIEW Components
FRAME_BG_COLOR = '#f8f9fa'
ITEM_BG_COLOR = 'white'
TITLE_FONT = ("Arial", 8, "normal")
SMALL_FONT = ("Arial", 9, "normal")
SCORE_COLOR = '#1b75bc'
SCORE_FONT = ("Arial", 42, "bold")
ERROR_COLOR = '#851619'