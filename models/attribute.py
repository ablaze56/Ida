# differentiate between the attributes of dom elements
# needed to perform search


from enum import Enum


class Attribute(Enum):
    ID = 1
    NAME = 2
    CLASS = 3
    XPATH = 4
    CSS_SELECTOR = 5
    JS_FUNCTION = 6
