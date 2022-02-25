import json
import constants.all as c
from models.sequence import Sequence

FILE_ID: int = 0
SECTION_ID: int = 0


def parse(names):
    global FILE_ID, SECTION_ID
    res = []
    for n in names:
        SECTION_ID = 0
        with open(f'{c.FOLDER}\\{n}') as f:
            data = json.load(f)

            if n == c.SETTINGS_FILE_NAME:
                c.URL = data['url']
            else:
                res.extend(parse_sequence(data['seq']))
        FILE_ID += 1

    return res


def parse_sequence(data):
    global FILE_ID, SECTION_ID
    sequences = []
    for s in data:
        n = Sequence()

        if c.DESC in s:
            n.desc = s[c.DESC]

        if c.ID in s:
            n.id = s[c.ID]

        if c.NAME in s:
            n.name = s[c.NAME]

        if c.CLASS in s:
            n.className = s[c.CLASS]

        if c.TYPE in s:
            n.type = s[c.TYPE]

        if c.TEXT in s:
            n.text = s[c.TEXT]

        if c.XPATH in s:
            n.xpath = s[c.XPATH]

        if c.CSS_SELECTOR in s:
            n.cssSelector = s[c.CSS_SELECTOR]

        n.fileId = FILE_ID
        n.sectionid = SECTION_ID

        SECTION_ID += 1
        sequences.append(n)

    return sequences
