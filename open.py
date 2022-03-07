import tkinter as tk
from constants import all as c
from app import App
from os import path
from PIL import Image, ImageTk
from pathlib import Path


class Open(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        self.root = root

        # Widgets
        self.top = tk.Frame(root, bg=c.LOGO_BLUE_COLOR)
        self.top.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.logo_frame = tk.Frame(root, bg=c.LOGO_BLUE_COLOR)
        self.logo_frame.place(relx=0, rely=0, relwidth=0.6, relheight=1)

        self.logo_file = './img/idaBlue.png'
        self.img = ImageTk.PhotoImage(Image.open(self.logo_file))
        self.lbl = tk.Label(self.logo_frame, image=self.img)
        self.lbl.pack()

        self.text_frame = tk.Frame(root, bg=c.LOGO_BLUE_COLOR)
        self.text_frame.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)

        self.i1 = tk.Label(self.text_frame, bg=c.LOGO_BLUE_COLOR, fg=c.FRAME_BG_COLOR, anchor='w')
        self.i1.config(text='Hi :)')
        self.i1.place(relx=0, rely=0.05, relwidth=1, relheight=0.18)

        self.i2 = tk.Label(self.text_frame, bg=c.LOGO_BLUE_COLOR, fg=c.FRAME_BG_COLOR, anchor='w')
        self.i2.config(text='Prepare sequences')
        self.i2.place(relx=0, rely=0.2, relwidth=1, relheight=0.18)

        self.i3 = tk.Label(self.text_frame, bg=c.LOGO_BLUE_COLOR, fg=c.FRAME_BG_COLOR, anchor='w')
        self.i3.config(text='and let me do my job.')
        self.i3.place(relx=0, rely=0.35, relwidth=1, relheight=0.18)

        self.start_btn = tk.Button(root, text='Go', font=c.END_MESSAGE_FONT, justify='center', fg=c.LOGO_BLUE_COLOR,
                                   bd=0, highlightthickness=2, highlightbackground=c.LOGO_BLUE_COLOR, borderwidth=2,
                                   command=lambda: self.begin_tests())

        self.start_btn.place(relx=0.75, rely=0.66, relwidth=0.2, relheight=0.25)





    def begin_tests(self):
        self.lbl.pack_forget()

        prf = tk.Frame(self.root, bg=c.LOGO_BLUE_COLOR)
        prf.place(relx=0, rely=0.014, relwidth=0.98, relheight=0.984)

        App(prf)
