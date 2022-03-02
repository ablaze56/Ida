import tkinter as tk
from modules.finder import read
from modules.parser import parse
from modules.webclient import WebClient
from main_module import execute
from threading import Thread

from app import App


def begin():
    # imports settings and sequences from .\library folder and parse them into objects
    data = read()
    sequences = parse(data)
    WebClient()
    execute(sequences)


def main():
    Thread(target=begin).start()
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
