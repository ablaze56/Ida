import tkinter as tk
import platform
from app import App
import constants.all as c


def main():
    root = tk.Tk()

    root.title("Ida (v:1.0)")
    root.geometry('360x180')
    root.attributes("-topmost", True)
    root.config(bg=c.FRAME_BG_COLOR)

    system = platform.system()
    if system == 'Windows':
        root.iconbitmap('./img/ikona.ico')
    elif system == 'Darwin':
        img = tk.Image("photo", file="./img/ikona.png")
        root.iconphoto(True, img)

    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
