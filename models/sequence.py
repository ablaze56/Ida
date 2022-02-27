# desc: description used for logging test results
# type dom element
# attribute: search dom element by unique attribute, i.e.: id, name, class, css_selector or xpath
# wait can specify how long script can wait after


from constants import all as c
from models.type import Type
from models.attribute import Attribute


# Initialization in Common already contains correct object type
def get_attribute(a):
    if isinstance(a, str):
        if a == c.NAME:
            return Attribute.NAME
        elif a == c.ID:
            return Attribute.ID
        elif a == c.CLASS:
            return Attribute.CLASS
        elif a == c.XPATH:
            return Attribute.XPATH
        elif a == c.USER_CONSTANT:
            return Attribute.USER_CONSTANT
        else:
            print('Unknown library attribute: ', a)
    else:
        return a


# Initialization in Common already contains correct object type
def get_type(t):
    if isinstance(t, str):
        if t == c.CLICK:
            return Type.CLICK
        elif t == c.INPUT:
            return Type.INPUT
        elif t == c.FUNCTION:
            return Type.FUNCTION
        else:
            print("Unknown library type: ", t)
    else:
        return t


class Sequence:
    def __init__(self, file_id, section_id, desc, sequence_type, attribute_id, attribute_value, insert_text, wait):
        self.file_id = file_id
        self.section_id = section_id

        self.desc = desc
        self.type = get_type(sequence_type)
        self.attribute_id = get_attribute(attribute_id)
        self.attribute_value = attribute_value

        self.insert_text = insert_text
        self.wait = wait
        self.findAll = False
        self.success = False

