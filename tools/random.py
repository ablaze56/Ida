import random
import string


def numberFor(length):
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(length))


def stringFor(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))