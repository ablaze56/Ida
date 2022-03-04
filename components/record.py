import tkinter as tk
import constants.all as c


class RecordKind:
    PAST = 0.03
    RUNNING = 0.355
    NEXT = 0.68


class Record(tk.Frame):
    def __init__(self, fr, kind):
        tk.Frame.__init__(self, fr)

        self.score = 0
        self.kind = kind

        self.config(bd=1, relief='sunken', bg=c.ITEM_BG_COLOR)
        self.place(relx=0.01, rely=self.kind-0.014, relwidth=0.96, relheight=0.285)

        self.lb = tk.Label(fr, text='', bd=0, font=c.SMALL_FONT, bg=c.ITEM_BG_COLOR, anchor='w')

        if self.kind == RecordKind.RUNNING:
            self.lb.configure(fg='black')
        else:
            self.lb.configure(fg='gray30')

        self.lb.place(relx=0.05, rely=self.kind + 0.024, relwidth=0.85, relheight=0.18)


    def update(self, text, err=False):
        print('UPDATE!')
        self.lb.configure(text=f'{text}')
        if err:
            self.lb.configure(fg=c.ERROR_COLOR)


    def clear(self):
        self.lb.configure(text='')

