# mac installation

from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': '/img/ikona.icns',
    'plist': {
        'CFBundleShortVersionString': '1.0',
        'LSUIElement': True,
    },
    'packages': [],
}

setup(
    app=APP,
    name='Ida',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=[]
)