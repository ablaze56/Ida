import tkinter as tk
import constants.all as c


class SemaphoreKind:
    ALL = ['Tests', 0.01]
    CURRENT = ['Current', 0.335]
    ERRORS = ['Errors', 0.66]


class Semaphore(tk.Frame):
    def __init__(self, fr, kind):
        tk.Frame.__init__(self, fr)

        self.score = 0
        self.kind = kind

        self.config(bd=1, relief='sunken', bg=c.BACKGROUND_COLOR)
        self.place(relx=self.kind[1], rely=0.05, relwidth=0.31, relheight=0.85)

        self.lb = tk.Label(fr, text=self.kind[0], bd=0, font=c.SMALL_FONT, justify='center', bg=c.BACKGROUND_COLOR,
                           fg='black')
        self.lb.place(relx=self.kind[1] + 0.02, rely=0.7, relwidth=0.25, relheight=0.15)

        self.nr = tk.Label(fr, text='666', bd=0, font=c.SCORE_FONT, justify='center', bg=c.BACKGROUND_COLOR, fg='black')
        self.nr.place(relx=self.kind[1] + 0.02, rely=0.1, relwidth=0.28, relheight=0.5)

    def update(self, ):
        print('update score')
        self.score += self.score
        self.nr.configure(text=f'{self.score}')
