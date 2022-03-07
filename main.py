import tkinter as tk
import platform
import constants.all as c
from open import Open
from pathlib import Path
from os import getcwd


def main():
    root = tk.Tk()

    root.title("Ida")
    root.geometry('360x180')
    root.attributes("-topmost", True)
    root.config(bg=c.FRAME_BG_COLOR)
    setup(root)

    Open(root)
    root.mainloop()


def setup(rt):

    cwd = getcwd()
    c.SYSTEM = platform.system()
    if c.SYSTEM == 'Windows':
        c.WORK_FOLDER = cwd
        rt.iconbitmap('./img/ikona.ico')
    elif c.SYSTEM == 'Darwin':
        c.WORK_FOLDER = cwd.replace('Ida.app/Contents/Resources', '')
        img = tk.Image("photo", file="./img/ikona.png")
        rt.iconphoto(True, img)

    c.LIBRARY_FOLDER = Path(f'{c.WORK_FOLDER}/library')
    c.LOG_FOLDER = Path(f'{c.WORK_FOLDER}/reports')
    c.SETTINGS_FOLDER = Path(f'{c.WORK_FOLDER}/library/settings')
    c.SEQUENCES_FOLDER = Path(f'{c.WORK_FOLDER}/library/sequences')


if __name__ == '__main__':
    main()
