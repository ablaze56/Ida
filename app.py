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


# Globals
# tracking automated testing, made specifically for menus with similar id, i.e. menu_1, menu_1_!
auto_seq = []
auto_seq_done = []
auto_seq_failed = []



class App(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        Thread(target=self.begin).start()
        self.sequences = []

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


    def begin(self):
        # imports settings and sequences from .\library folder and parse them into objects
        data = read()
        self.sequences = parse(data)
        WebClient()
        self.all_nr.update(fix=len(self.sequences))
        self.execute(self.sequences)


    def execute(self, all_seq):
        for seq in all_seq:
            # if any click on previous elements in this file failed it will skip next sections
            failed_clicks = filter(lambda
                                       s: s.file_id == seq.file_id and s.section_id < seq.section_id and not s.success and s.type == cons.CLICK,
                                   all_seq)

            if len(list(failed_clicks)) > 0:
                print('skip for failed click: ', seq.desc)
            else:
                # search all occurrences in then execute them all
                print('seq: ', seq.desc, seq.findAll)
                if seq.findAll:
                    # sequence split to several sequnces
                    self.split_single_to_multiple(seq)

                else:
                    self.execute_single(seq)
                    sleep(seq.wait)

        # Failed
        failed = filter(lambda s: not s.success, all_seq)
        count_all = len(list(all_seq))
        count_failed = len(list(failed))
        print('Success: ', count_all - count_failed, '/', count_all)


    def execute_single(self, seq):
        print("Locating... ", seq.desc, seq.type, seq.attribute_id, seq.attribute_value)
        self.cur_nr.update(add=1)

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
            if returned_error():
                print('CRITICAL ERROR')
                self.err_nr.update(add=1)
            else:
                print("ERROR: Not found")
                self.err_nr.update(add=1)

    # NOVA
    def split_single_to_multiple(self, s):
        global auto_seq
        print('split_single_to_multiple from ', s.attribute_id, s.attribute_value)
        similar = find_similar(s)

        auto_seq.extend(similar)
        auto_seq.sort(key=lambda x: x.attribute_value)

        self.repetitve_execute()


    def repetitve_execute(self):
        global auto_seq, auto_seq_done
        print('repetitve_execute')

        undone = [x for x in auto_seq if x not in auto_seq_done]
        print('AUTO_SEQ count: ', len(auto_seq), 'undone count: ', len(undone))
        for u in undone:
            auto_seq_done.append(u)
            self.execute_single(u)
            similar = find_similar(u)

            for s in similar:
                if s.attribute_value != u.attribute_value:
                    auto_seq.append(s)
                    self.all_nr.update(add=1)

            auto_seq.sort(key=lambda x: x.attribute_value)

            if len(auto_seq) > len(auto_seq_done):
                print('Ponovno od začetka')
                # check for modal pop up and close it:
                escape_send()
                self.repetitve_execute()
                break
            else:
                break



