import tkinter as tk
from tkinter import messagebox
from threading import Thread
from time import sleep
import constants.all as c
from components.semaphore import Semaphore, SemaphoreKind
from components.record import Record, RecordKind
from components.openLogButton import OpenLogButton
from modules.finder import read
from modules.parser import parse
from modules.webclient import WebClient
from models.type import Type
from modules.searchclient import find_similar_elements as find_similar, wait_until_visible as wait_until, escape_send
from modules.webclient import is_returned_http_error as returned_error


class App(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        Thread(target=self.get_data).start()

        self.sequences = []
        self.finished = []
        self.failed = []

        self.run_count = 0

        # Widgets
        self.top = tk.Frame(root, bg=c.FRAME_BG_COLOR)
        self.top.place(relx=0.02, rely=0.02, relwidth=0.98, relheight=0.50)

        self.all_nr = Semaphore(self.top, SemaphoreKind.ALL)
        self.cur_nr = Semaphore(self.top, SemaphoreKind.CURRENT)
        self.err_nr = Semaphore(self.top, SemaphoreKind.ERRORS)

        self.bottom = tk.Frame(root, bg=c.FRAME_BG_COLOR)
        self.bottom.place(relx=0.02, rely=0.52, relwidth=0.98, relheight=0.44)

        self.past = Record(self.bottom, RecordKind.PAST)
        self.running = Record(self.bottom, RecordKind.RUNNING)
        self.next = Record(self.bottom, RecordKind.NEXT)

    def get_data(self):
        # imports settings and sequences from .\library folder and parse them into objects
        data = read()
        print('data: ', data)
        self.sequences = parse(data)
        print("self.sequences: ", len(self.sequences))
        WebClient()
        self.all_nr.update(fix=len(self.sequences))
        self.begin()

    def begin(self):
        for seq in self.sequences:
            # if any click on previous elements in this file failed it will skip next sections
            failed_clicks = filter(lambda
                                       s: s.file_id == seq.file_id and s.section_id < seq.section_id and not s.success and s.type == c.CLICK,
                                   self.sequences)

            if len(list(failed_clicks)) > 0:
                print('skip for failed click: ', seq.desc)
            else:
                # search all occurrences in then execute them all
                print('seq: ', seq.desc, seq.find_all)
                if seq.find_all:
                    # sequence split to several sequnces
                    self.create_similar(seq)
                else:
                    self.perform(seq)
                    sleep(seq.wait)

        self.create_report()
        print('Finished')

    def perform(self, seq):
        print("Locating... ", seq.desc, seq.type, seq.attribute_id, seq.attribute_value)
        self.finished.append(seq)

        try:
            element = wait_until(seq)
            seq.success = True
            print("Ok")

            if seq.type == Type.CLICK:
                element.click()
            elif seq.type == Type.INPUT:
                if len(seq.insert_text) > 0:
                    element.send_keys(seq.insert_text)
            else:
                print("seq.type: ", seq.type)
                self.err_nr.update(add=1)
                seq.error = f'Internal application error: Unknown sequence type: {seq.type}'
                self.failed.append(seq)

        except (ValueError, Exception) as e:
            err = f"Unable to locate an element with {seq.attribute_id} expression {seq.attribute_value}."
            returned_err = returned_error()
            if returned_err[0]:
                err = f'{returned_err[1]}'

            self.err_nr.update(add=1)
            seq.error = err
            self.failed.append(seq)

        self.update_recorde()

    # Create sub events - Automatic recognition based on similar id inside xpath
    def create_similar(self, s):
        # Find similar items by ID and remove the same to avoid duplicates
        sim = find_similar(s)
        sim = filter(lambda x: x.attribute_value != s.attribute_value, sim)
        similar = list(sim)
        similar.sort(key=lambda x: x.attribute_value)

        # extend list after current sequence
        ind = self.sequences.index(s)
        self.sequences[ind + 1:1] = similar
        self.all_nr.update(fix=len(self.sequences))

        self.recursive_perform()

    def recursive_perform(self):
        undone = [x for x in self.sequences if x not in self.finished and x.find_all]
        # print('AUTO_SEQ count: ', len(self.sequences), 'undone count: ', len(undone))
        for u in undone:
            self.finished.append(u)
            self.perform(u)
            similar = find_similar(u)

            for s in similar:
                if s.attribute_value != u.attribute_value:
                    ind = self.sequences.index(u)
                    self.sequences.insert(ind, s)

            if len(self.sequences) > len(self.finished):
                # restart
                # check for modal pop up and close it if necessary:
                escape_send()
                self.recursive_perform()
                break
            else:
                break

    def update_recorde(self):
        nr_seq = len(self.sequences)

        self.all_nr.update(fix=nr_seq)
        self.cur_nr.update(fix=len(self.finished))
        self.err_nr.update(fix=len(self.failed))

        if nr_seq == 0:
            messagebox.showerror('Error', 'No Sequences found!')

        else:

            txt = self.sequences[self.run_count].desc
            if self.sequences[self.run_count].wait > 0:
                txt += f' waiting {self.sequences[self.run_count].wait}s'
            self.running.update(txt)

            if self.run_count+1 < nr_seq:
                txt = self.sequences[self.run_count+1].desc
                if self.sequences[self.run_count+1].wait > 0:
                    txt += f'waiting {self.sequences[self.run_count+1].wait}s'

                self.next.update(self.sequences[self.run_count+1].desc)
            else:
                self.next.clear()

            if self.run_count == 0:
                self.past.clear()
            else:
                if self.sequences[self.run_count-1].error:
                    self.past.update(self.sequences[self.run_count-1].desc, err=True)
                else:
                    self.past.update(self.sequences[self.run_count - 1].desc)

        self.run_count += 1

    def create_report(self):
        for widgets in self.bottom.winfo_children():
            widgets.destroy()

        finished_lbl = tk.Label(self.bottom, justify='left', anchor="w",
                                bg=c.FRAME_BG_COLOR, font=c.END_MESSAGE_FONT)
        col = c.SCORE_COLOR
        message = ':) Good job! No errors found.'
        if len(self.failed) > 0:
            col = c.ERROR_COLOR
            message = ':( Errors found.'
            OpenLogButton(self.bottom, self.failed)

        finished_lbl.config(text=message, fg=col)
        finished_lbl.place(relx=0.02, rely=0.25, relwidth=0.85, relheight=0.25)
