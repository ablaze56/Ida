from selenium import webdriver

DRIVER: webdriver


WORK_FOLDER = ''
LIBRARY_FOLDER = ''
LOG_FOLDER = ''
SETTINGS_FOLDER = ''
SEQUENCES_FOLDER = ''

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
TITLE_FONT = ("Tahoma", 9, "normal")
END_MESSAGE_FONT = ("Tahoma", 14, "bold")
RECORD_FONT = ("Tahoma", 10, "normal")
CURRENT_RECORD_FONT = ("Tahoma", 11, "normal")
SMALL_FONT = ("Tahoma", 9, "normal")
SCORE_COLOR = '#1b75bc'
SCORE_FONT = ("Tahoma", 42, "bold")
ERROR_COLOR = '#851619'
LOGO_BLUE_COLOR = '#1099d6'