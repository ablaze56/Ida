import tkinter as tk
import constants.all as c
from datetime import date
import logging
import os



class OpenLogButton(tk.Button):
    def __init__(self, fr, data):
        tk.Button.__init__(self, fr)

        self.data = data

        self.config(text='Open', font=c.SMALL_FONT, bd=1, justify='center', bg=c.ITEM_BG_COLOR, command=lambda: self.create_report())
        self.place(relx=0.6, rely=0.6, relwidth=0.2, relheight=0.3)

        self.today = date.today()
        self.d = self.today.strftime("%Y-%m-%d--%H-%M-%S")
        self.name = f'{self.d}_{len(self.data)}_errors'

        if not os.path.isdir(c.LOG_FOLDER):
            try:
                os.mkdir(c.LOG_FOLDER)
            except:
                tk.MessageBox('Error', f'I cannot create folder: {c.LOG_FOLDER}')

        logging.basicConfig(filename=f'{c.LOG_FOLDER}/{self.name}', filemode='a', format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S', level=logging.INFO)


    def create_report(self):
        print('Create report')
        for d in self.data:
            logging.error(d.desc)


        self.open_log()

    def open_log(self):
        print('Open err log')
