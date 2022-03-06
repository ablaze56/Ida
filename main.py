import tkinter as tk
import platform
import constants.all as c
from open import Open


def main():
    root = tk.Tk()

    root.title("Ida")
    root.geometry('360x180')
    root.attributes("-topmost", True)
    root.config(bg=c.FRAME_BG_COLOR)

    system = platform.system()
    if system == 'Windows':
        root.iconbitmap('./img/ikona.ico')
    elif system == 'Darwin':
        img = tk.Image("photo", file="./img/ikona.png")
        root.iconphoto(True, img)

    Open(root)
    root.mainloop()


if __name__ == '__main__':
    main()
