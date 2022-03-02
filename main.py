import platform
import tkinter as tk
from modules.finder import read
from modules.parser import parse
from modules.webclient import WebClient
from modules.main_module import execute
from threading import Thread


def begin():
    # imports settings and sequences from .\library folder and parse them into objects
    data = read()
    sequences = parse(data)
    WebClient()
    execute(sequences)



def main():
    Thread(target=begin).start()

    # VIEW
    #root = tk.Tk()
    #root.title("Ida (v:1.0)")
    #root.geometry('800x280')
    #root.attributes("-topmost", True)

    system = platform.system()
    #if system == 'Windows':
    #    root.iconbitmap('./img/ikona.ico')
    #elif system == 'Darwin':
    #    img = tk.Image("photo", file="./img/ikona.png")
    #    root.iconphoto(True, img)
    #root.mainloop()


if __name__ == '__main__':
    main()
