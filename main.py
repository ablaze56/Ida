import platform
from pathlib import Path
import tkinter as tk
from tools.finder import read
from tools.parser import parse
from tools.webclient import WebClient
from tools.execute import execute


def main():
    # imports settings and sequences from .\library folder and parse them into objects
    data = read()
    sequences = parse(data)
    WebClient()
    execute(sequences)

    # VIEW
    root = tk.Tk()

    system = platform.system()
    if system == 'Windows':
        root.iconbitmap('./img/ikona.ico')
    elif system == 'Darwin':
        # mac
        img = tk.Image("photo", file="./img/ikona.png")
        root.iconphoto(True, img) # you may also want to try this.
        root.tk.call('wm', 'iconphoto', root._w, img)


       # root.iconbitmap('./img/ikona.icns')
    root.title("Ida (v:1.0)")
    root.geometry('950x400')
    root.mainloop()


if __name__ == '__main__':
    main()
