# differentiate between the types of dom elements
# common is a reusable type which you declare in separate json and use later


from enum import Enum


class Type(Enum):
    INPUT = 1
    CLICK = 2
    FUNCTION = 3
    COMMON = 4
