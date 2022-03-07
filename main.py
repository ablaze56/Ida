import tkinter as tk
import platform
import constants.all as c
from open import Open
from pathlib import Path
from os import path


def main():
    root = tk.Tk()

    root.title("Ida")
    root.geometry('360x180')
    root.attributes("-topmost", True)
    root.config(bg=c.FRAME_BG_COLOR)
    create_paths()

    system = platform.system()
    if system == 'Windows':
        root.iconbitmap('./img/ikona.ico')
    elif system == 'Darwin':
        img = tk.Image("photo", file="./img/ikona.png")
        root.iconphoto(True, img)

    Open(root)
    root.mainloop()




def create_paths():
    c.WORK_FOLDER = path.dirname(path.realpath(__file__))
    c.LIBRARY_FOLDER = Path(f'{c.WORK_FOLDER}/library')
    c.LOG_FOLDER = Path(f'{c.WORK_FOLDER}/reports')
    c.SETTINGS_FOLDER = Path(f'{c.WORK_FOLDER}/library/settings')
    c.SEQUENCES_FOLDER = Path(f'{c.WORK_FOLDER}/library/sequences')

    print(f'lib: {c.LIBRARY_FOLDER}')
    print(f'log: {c.LOG_FOLDER}')
    print('-----')


if __name__ == '__main__':
    main()
