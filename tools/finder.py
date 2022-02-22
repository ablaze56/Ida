# Finds json files in .\SEQUENCE folder
# Puts settings.json to first position


from os import listdir
import constants.all as c
from os.path import isfile, join

def read():
    all_files = [f for f in listdir(c.FOLDER) if isfile(join(c.FOLDER, f))]
    selection = []
    for f in all_files:
        if f.endswith('json'):
            if f == 'settings.json':
                selection.insert(0, f)
            else:
                selection.append(f)

    return selection