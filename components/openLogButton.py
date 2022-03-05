import tkinter as tk
from tkinter import messagebox
import errno
import constants.all as c
from datetime import datetime
import logging
import os
import subprocess
import platform


class OpenLogButton(tk.Button):
    def __init__(self, fr, failed):
        tk.Button.__init__(self, fr)

        self.failed = failed

        self.config(text='Open log', font=c.RECORD_FONT, justify='center', fg=c.ERROR_COLOR,
                    bg=c.ITEM_BG_COLOR, bd=1, highlightthickness=2,
                    highlightbackground=c.FRAME_BG_COLOR, borderwidth=2,
                    command=lambda: self.open_log())

        self.place(relx=0.79, rely=0.63, relwidth=0.2, relheight=0.35)

        self.today = datetime.today()
        self.d = self.today.strftime("%Y-%m-%d-%H-%M-%S")
        self.err_f_name = 'errors'
        if len(self.failed) == 1:
            self.err_f_name = 'error'

        self.name = f'{self.d}_{len(self.failed)}_{self.err_f_name}.log'

        if not os.path.isdir(c.LOG_FOLDER):
            try:
                os.mkdir(c.LOG_FOLDER)
            except OSError as oe:
                if oe.errno != errno.EEXIST:
                    raise
                pass
                messagebox.showerror('Error', f'I cannot create folder: {c.LOG_FOLDER}')

        logging.basicConfig(filename=f'{c.LOG_FOLDER}/{self.name}', filemode='a', format='%(asctime)s,%(msecs)d %('
                                                                                         'message)s',
                            datefmt='%H:%M:%S', level=logging.INFO)

        self.create_report()

    def create_report(self):
        print('Create report')
        for d in self.failed:
            print(f'report data: {d.file_id}, desc: {d.desc}, err: {d.error}')
            logging.error(f'file: {d.file_id}, desc: {d.desc}, err: {d.error}')

    def open_log(self):
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', f'{c.LOG_FOLDER}/{self.name}'))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(f'{c.LOG_FOLDER}/{self.name}')
            else:  # linux variants
                subprocess.call(('xdg-open', f'{c.LOG_FOLDER}/{self.name}'))
        except OSError as oe:
            messagebox.showerror('Error', f'{oe.strerror}:{oe.filename}')
