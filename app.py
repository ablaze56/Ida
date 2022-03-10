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
        self.run_count = 0

        # Widgets
        self.top = tk.Frame(root, bg=c.FRAME_BG_COLOR)
        self.top.place(relx=0.02, rely=0.02, relwidth=0.98, relheight=0.50)

        self.all_nr = Semaphore(self.top, SemaphoreKind.ALL)
        self.success_nr = Semaphore(self.top, SemaphoreKind.SUCCESS)
        self.err_nr = Semaphore(self.top, SemaphoreKind.ERRORS)

        self.bottom = tk.Frame(root, bg=c.FRAME_BG_COLOR)
        self.bottom.place(relx=0.02, rely=0.52, relwidth=0.98, relheight=0.44)

        self.past = Record(self.bottom, RecordKind.PAST)
        self.running = Record(self.bottom, RecordKind.RUNNING)
        self.next = Record(self.bottom, RecordKind.NEXT)

    def get_data(self):
        # imports settings and sequences from .\library folder and parse them into objects
        data = read()
        self.sequences = parse(data)
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
                print('begin: ', seq.attribute_value, seq.auto_find)
                if seq.auto_find:
                    # sequence split to several sequnces
                    self.create_similar(seq)
                else:
                    self.perform(seq)
                    sleep(seq.wait)

        self.create_report()
        print('Finished')

    def perform(self, seq):
        print("perform... ", seq.desc, seq.type, seq.attribute_id, seq.attribute_value)
        seq.invoked = True
        try:
            element = wait_until(seq)
            if seq.type == Type.CLICK:
                seq.success = True
                element.click()
            elif seq.type == Type.INPUT:
                if len(seq.insert_text) > 0:
                    seq.success = True
                    element.send_keys(seq.insert_text)
                else:
                    seq.error = f'Unknown type of in then sequence : {seq.type}'
                    seq.failed = True
            else:
                print("seq.type: ", seq.type)
                # self.err_nr.update(add=1)
                seq.error = f'Internal application error: Unknown sequence type: {seq.type}'
                seq.failed = True

        except (ValueError, Exception) as e:
            err = f"Unable to locate an element with {seq.attribute_id} expression {seq.attribute_value}."
            returned_err = returned_error()
            if returned_err[0]:
                err = f'{returned_err[1]}'
                print('HTML Error: ', err )
            seq.error = err
            seq.failed = True

        self.update_records()

    # Create sub events - Automatic recognition based on similar id inside xpath
    def create_similar(self, s):
        # Find similar items by ID and remove the same to avoid duplicates
        sim = find_similar(s)

        # list of attributes values
        existing_attribute_values = [x.attribute_value for x in self.sequences]

        # add non-existing sequences and sort them
        similar = list(filter(lambda x: x.attribute_value not in existing_attribute_values, sim))
        similar.sort(key=lambda x: x.attribute_value)

        # extend list after current sequence
        ind = self.sequences.index(s)
        self.sequences[ind + 1:1] = similar

        # update score
        self.all_nr.update(fix=len(self.sequences))

        self.recursive_perform()

    def recursive_perform(self):
        # recursion only for elements which weren't invokend and mare marked with auto_find
        undone = [x for x in self.sequences if not x.invoked and x.auto_find]

        # avoid duplications
        existing_attribute_values = [x.attribute_value for x in self.sequences]

        for u in undone:
            # click and find other similar
            self.perform(u)
            similar = find_similar(u)
            similar.sort(key=lambda x: x.attribute_value)

            for i, s in enumerate(similar):
                if s.attribute_value not in existing_attribute_values:
                    ind = self.sequences.index(u)
                    # if not existing add it to sequences after previous
                    self.sequences.insert(ind+i, s)

            # recheck for invoked after addaing new elements
            not_invoked = list(filter(lambda x: not x.invoked and x.auto_find, self.sequences))
            if len(not_invoked) > 0:
                # check for modal pop up and close it if necessary:
                escape_send()
                # restart
                self.recursive_perform()
                break
            else:
                break

    def update_records(self):
        nr_of_seq = len(self.sequences)

        if nr_of_seq == 0:
            messagebox.showerror('Error', 'No Sequences found!')
            return

        invoked = list(filter(lambda x: x.invoked, self.sequences))
        counter = len(invoked) + 1

        success = list(filter(lambda x: x.success and not x.failed, self.sequences))
        failed = list(filter(lambda x: x.failed, self.sequences))

        # update counters on top
        self.all_nr.update(fix=nr_of_seq)
        self.success_nr.update(fix=len(success))
        self.err_nr.update(fix=len(failed))

        # update records on bottom
        # current record
        if len(invoked) < 1:
            self.running.clear()
            return

        txt = invoked[-1].desc
        if self.sequences[-1].wait > 0:
            txt += f' waiting {self.sequences[-1].wait}s'
        self.running.update(txt)

        # next record
        following = counter + 1
        if following < nr_of_seq:
            self.next.update(self.sequences[following].desc)
        else:
            self.next.clear()

        # previous record
        if len(success) > 0:
            if self.sequences[-1].error:
                self.past.update(self.sequences[-1].desc, err=True)
            else:
                self.past.update(self.sequences[-1].desc)
        else:
            self.past.clear()




    def create_report(self):
        for widgets in self.bottom.winfo_children():
            widgets.destroy()

        finished_lbl = tk.Label(self.bottom, justify='left', anchor="w",
                                bg=c.FRAME_BG_COLOR, font=c.END_MESSAGE_FONT)

        failed = list(filter(lambda x: x.failed, self.sequences))
        col = c.SCORE_COLOR
        message = ':) Good job! No errors found.'
        if len(failed) > 0:
            col = c.ERROR_COLOR
            message = ':( Errors found.'
            OpenLogButton(self.bottom, failed)

        finished_lbl.config(text=message, fg=col)
        finished_lbl.place(relx=0.02, rely=0.25, relwidth=0.85, relheight=0.25)
