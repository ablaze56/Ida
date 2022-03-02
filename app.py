import tkinter as tk
import platform
from components.semaphore import Semaphore, SemaphoreKind
from components.record import Record, RecordKind


class App(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        root.title("Ida (v:1.0)")
        root.geometry('360x180')
        root.attributes("-topmost", True)

        self.system = platform.system()
        if self.system == 'Windows':
            root.iconbitmap('./img/ikona.ico')
        elif self.system == 'Darwin':
            img = tk.Image("photo", file="./img/ikona.png")
            root.iconphoto(True, img)

        self.top = tk.Frame(root)
        self.top.place(relx=0.02, rely=0.02, relwidth=0.98, relheight=0.50)

        self.all_nr = Semaphore(self.top, SemaphoreKind.ALL)
        self.cur_nr = Semaphore(self.top, SemaphoreKind.CURRENT)
        self.err_nr = Semaphore(self.top, SemaphoreKind.ERRORS)

        self.bottom = tk.Frame(root)
        self.bottom.place(relx=0.02, rely=0.52, relwidth=0.98, relheight=0.44)

        self.past = Record(self.bottom, RecordKind.PAST)
        self.running = Record(self.bottom, RecordKind.RUNNING)
        self.next = Record(self.bottom, RecordKind.NEXT)
