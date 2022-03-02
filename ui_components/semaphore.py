import tkinter as tk
from enum import Enum


class SemaphoreKind(Enum):
    ALL = ('Tests', 1)
    CURRENT = ('Current', 2)
    ERRORS = ('Errors', 3)


class Semaphore(tk.Frame):
    def __init__(self, fr, score=0, kind=SemaphoreKind):
        tk.Frame.__init__(self, fr)

        self.config(bd=1, relief='sunken')
        self.place(relx=0.3, rely=0.3, relwidth=0.3, relheight=0.3)

        self.score = 0
        self.kind = kind


        self.lb = tk.Label(fr, text=self.kind[0], font=("Arial", 11, "normal"), justify='left', bg='white')
        self.lb.place(relx=0.3, rely=0.3, relwidth=0.3, relheight=0.3)

        self.nr = tk.Label(fr, text='', font=("Arial", 36, "bold"), justify='left', bg='white')
        self.nr.place(relx=0.3, rely=0.3, relwidth=0.3, relheight=0.3)



    def update(self,):
        print('update score')
        self.score += self.score
        self.nr.configure(text=f'{self.score}')