import tkinter as tk
from components.semaphore import Semaphore, SemaphoreKind
from components.record import Record, RecordKind
import constants.all as c

from modules.finder import read
from modules.parser import parse
from modules.webclient import WebClient
from threading import Thread
from constants import all as cons
from time import sleep
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
        self.sequences = parse(data)
        print("self.sequences: ", len(self.sequences))
        WebClient()
        self.all_nr.update(fix=len(self.sequences))
        self.begin()

    def begin(self):
        for seq in self.sequences:
            # if any click on previous elements in this file failed it will skip next sections
            failed_clicks = filter(lambda
                                       s: s.file_id == seq.file_id and s.section_id < seq.section_id and not s.success and s.type == cons.CLICK,
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

        # Failed
        failed = filter(lambda s: not s.success, self.sequences)
        count_all = len(list(self.sequences))
        count_failed = len(list(failed))
        print('Success: ', count_all - count_failed, '/', count_all)

    def perform(self, seq):
        print("Locating... ", seq.desc, seq.type, seq.attribute_id, seq.attribute_value)
        self.finished.append(seq)
        self.update_recorde()

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
        except:
            self.failed.append(seq)
            if returned_error():
                print('CRITICAL ERROR')
                self.err_nr.update(add=1)
            else:
                print("ERROR: Not found")
                self.err_nr.update(add=1)

    # Create sub events - Automatic recognition based on similar id inside xpath
    def create_similar(self, s):
        print('split_single_to_multiple from ', s.attribute_id, s.attribute_value)

        # Find similar items by ID and remove the same to avoid duplicates
        sim = find_similar(s)
        sim = filter(lambda x: x.attribute_value != s.attribute_value, sim)
        similar = list(sim)
        similar.sort(key=lambda x: x.attribute_value)

        # extend list after current sequence
        ind = self.sequences.index(s)
        self.sequences[ind + 1:1] = similar

        self.recursive_perform()

    def recursive_perform(self):
        print('recursive_perform')

        undone = [x for x in self.sequences if x not in self.finished and x.find_all]
        print('AUTO_SEQ count: ', len(self.sequences), 'undone count: ', len(undone))
        for u in undone:
            self.finished.append(u)
            self.perform(u)
            similar = find_similar(u)

            for s in similar:
                if s.attribute_value != u.attribute_value:
                    ind = self.sequences.index(u)
                    self.sequences.insert(ind, s)

            if len(self.sequences) > len(self.finished):
                print('Ponovno od začetka')
                # check for modal pop up and close it:
                escape_send()
                self.recursive_perform()
                break
            else:
                break

    def update_recorde(self):
        print('update records: ', len(self.sequences))

        self.all_nr.update(fix=len(self.sequences))
        self.cur_nr.update(fix=len(self.finished))
        self.err_nr.update(fix=len(self.failed))

        if len(self.sequences) == 0:
            self.past.clear()
            self.running.clear()
            self.next.clear()
        else:
            index = 0

            if len(self.finished) > 0:
                # index of the next sequence is the current sequence
                index = self.sequences.index(self.finished[-1]) + 1
                self.past.update(self.finished[-1].desc)
            else:
                self.past.clear()

            if index < len(self.sequences):
                self.running.update(self.sequences[index].desc)
            else:
                self.running.clear()

            if index + 1 < len(self.sequences):
                self.next.update(self.sequences[index + 1].desc)
            else:
                self.next.clear()
