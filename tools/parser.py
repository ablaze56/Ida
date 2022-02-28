import json
import constants.all as c
from models.sequence import Sequence
from models.common import Common

FILE_ID: int = 0
SECTION_ID: int = 0

COMMONS = []


def parse(names):
    global FILE_ID, SECTION_ID, COMMONS
    res = []
    for n in names:
        SECTION_ID = 0

        # with open(f'{c.FOLDER}\\{n}') as f: Stara win varianta
        with open(n) as f:
            data = json.load(f)

            if 'url' in data:
                parse_settings(data)
            else:
                if 'commons' in data:
                    parse_common(data['commons'])
                elif 'seq' in data:
                    res.extend(parse_sequence(data['seq']))

                FILE_ID += 1

    return res


def parse_settings(data):
    c.URL = data['url']
    print('parsed: ', c.URL)

    # optional user defined constants
    if 'constants' in data:
        cons = data['constants']
        for con in cons:
            if 'name' not in con and 'value' not in con:
                print('ERROR - Constants must contain name and value keys.')
                continue

            name = con['name']
            value = con['value']
            c.USER_CONSTANTS.append([name, value])


def parse_sequence(data):
    global FILE_ID, SECTION_ID, COMMONS
    sequences = []
    for s in data:

        # Sequence or common can be marked as SKIP and is ignored
        if c.SKIP in s:
            if s[c.SKIP]:
                print(f'WARNING In Sequence: {s[c.DESC]} - Inactive element, skip.')
                continue

        # search is mandatory in case of sequence
        if c.SEARCH not in s and 'common_id' not in s:
            print(f'ERROR In Sequence {s[c.DESC]} - error in search element!')
            break

        # setting default values for non mandatory elements
        json_text = str(s[c.INSERT_TEXT] if c.INSERT_TEXT in s else ' ')

        # replace text with user defined constant if found
        if len(json_text) > 1:
            if '#constant:' in json_text:
                json_text = json_text.replace('#constant:', '')
                if json_text[0] == ' ':
                    json_text = json_text[1:]

            f = filter(lambda co: co[0] == json_text, c.USER_CONSTANTS)
            found = list(f)
            if len(found) > 0:
                json_text = found[0][1]
                print('text replace with constant: ', json_text)

        json_wait = s[c.WAIT] if c.WAIT in s else 0.1

        n: Sequence

        # if sequence json contains common_id it uses attributes of the Common object
        if 'common_id' in s:
            ids = filter(lambda f: f.common_id == s['common_id'], COMMONS)
            listed = list(ids)
            if len(listed) == 0:
                print(f"Error: Sequence: {s[c.DESC]} containing non existing common_id: {s['common_id']}")
                continue

            found = listed[0].sequence
            n = Sequence(file_id=FILE_ID, section_id=SECTION_ID, desc=s[c.DESC], sequence_type=found.type,
                         attribute_id=found.attribute_id, attribute_value=found.attribute_value,
                         insert_text=found.insert_text,
                         wait=found.wait)

        else:
            n = Sequence(file_id=FILE_ID, section_id=SECTION_ID, desc=s[c.DESC], sequence_type=s[c.TYPE],
                         attribute_id=s[c.SEARCH][0], attribute_value=s[c.SEARCH][1], insert_text=json_text,
                         wait=json_wait)

            # it should run differently - always checking and clicking on menu items
            n.FindAll = n.findAll if 'findAll' in s else False

        SECTION_ID += 1
        sequences.append(n)

    return sequences


def parse_common(data):
    global COMMONS
    for s in data:

        # Sequence or common can be marked as SKIP and is ignored
        if c.SKIP in s:
            if s[c.SKIP]:
                print(f'WARNING In Common: {s[c.DESC]} - Inactive element, skip.')
                break

        # search is mandatory
        if c.SEARCH not in s:
            print(f'ERROR In Common {s[c.DESC]} - error in search element!')
            break

        # id is mandatory
        if c.ID not in s:
            print(f'ERROR In Common {s[c.DESC]} - error in id element!')
            break

        # setting default values for non mandatory elements
        json_text = s[c.INSERT_TEXT] if c.INSERT_TEXT in s else ''
        json_wait = s[c.WAIT] if c.WAIT in s else 0.1

        seq = Sequence(file_id=-1, section_id=-1, desc=s[c.DESC], sequence_type=s[c.TYPE],
                       attribute_id=s[c.SEARCH][0], attribute_value=s[c.SEARCH][1], insert_text=json_text,
                       wait=json_wait)

        com = Common(common_id=s[c.ID], sequence=seq)
        COMMONS.append(com)
