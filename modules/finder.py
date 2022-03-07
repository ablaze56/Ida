# Finds json files in .\LIBRARY folders
# Puts settings.json to first position, commons after that commons
# They are split for order control - sequences must be sorted!


import constants.all as c
import os.path


def read():
    settings = []
    commons = []
    sequences = []

    selection = []

    for path, _, files in os.walk(c.LIBRARY_FOLDER):
        for f in files:
            if f.endswith('json'):
                full_path = os.path.join(path, f)
                if 'settings' in path:
                    settings.append(full_path)
                elif 'commons' in path:
                    commons.append(full_path)
                else:
                    sequences.append(full_path)

    selection.extend(settings)
    selection.extend(commons)

    sequences.sort()
    selection.extend(sequences)
    return selection
