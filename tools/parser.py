import json
import constants.all as c
from models.sequence import Sequence


def parse(names):
    res = []
    for n in names:
        print(n)
        with open(f'{c.FOLDER}\\{n}') as f:
            data = json.load(f)

            if n == 'settings.json':
                c.URL = data['url']
            else:
                res.append(parse_sequence(data['seq']))

    return res



def parse_sequence(data):
    sequences = []
    for s in data:
        n = Sequence()

        if 'desc' in s:
            n.desc = s['desc']

        if 'id' in s:
            n.id = s['id']

        if 'name' in s:
            n.name = s['name']

        if 'class' in s:
            n.className = s['class']

        if 'containsText' in s:
            n.containsText = s['containsText']

        if 'containsID' in s:
            n.containsID = s['containsID']

        if 'type' in s:
            n.type = s['type']

        if 'input' in s:
            n.input = s['input']

        sequences.append(n)

    return sequences
