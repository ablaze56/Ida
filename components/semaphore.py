import tkinter as tk
import constants.all as c


class SemaphoreKind:
    ALL = ['Nr of tests', 0.01]
    CURRENT = ['Completed', 0.335]
    ERRORS = ['Errors', 0.66]


class Semaphore(tk.Frame):
    def __init__(self, fr, kind):
        tk.Frame.__init__(self, fr)

        self.score = 0
        self.kind = kind

        self.config(bd=1, relief='sunken', bg=c.ITEM_BG_COLOR)
        self.place(relx=self.kind[1], rely=0.05, relwidth=0.31, relheight=0.85)

        self.lb = tk.Label(fr, text=self.kind[0], bd=0, font=c.TITLE_FONT, justify='center', bg=c.ITEM_BG_COLOR,
                           fg='black')
        self.lb.place(relx=self.kind[1] + 0.02, rely=0.75, relwidth=0.28, relheight=0.15)

        self.nr = tk.Label(fr, text='0', bd=0, font=c.SCORE_FONT, justify='center', bg=c.ITEM_BG_COLOR, fg=c.SCORE_COLOR)
        self.nr.place(relx=self.kind[1] + 0.02, rely=0.15, relwidth=0.28, relheight=0.5)


    def update(self, fix=0, add=0):
        print(self.kind, ' update record: ', 'fix: ', fix, 'add: ', add)
        if fix > 0:
            self.score = fix

        elif add > 0:
            self.score += add
        self.nr.configure(text=f'{self.score}')


        if self.kind == SemaphoreKind.ERRORS:
            if self.score > 0:
                self.nr.configure(fg='red')

