# differentiate between the attributes of dom elements
# needed to perform search
# user_constant is defined in settings and saved to constants


from enum import Enum


class Attribute(Enum):
    ID = 1
    NAME = 2
    CLASS = 3
    XPATH = 4
    CSS_SELECTOR = 5
    JS_FUNCTION = 6
