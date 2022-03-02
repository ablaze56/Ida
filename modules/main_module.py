from constants import all as cons
from time import sleep
from models.type import Type
from modules.searchclient import find_similar_elements as find_similar, wait_until_visible as wait_until
from modules.webclient import is_returned_http_error as returned_error


AUTO_COUNTER = 1000
AUTO_SEQ = []
AUTO_SEQ_DONE = []
FAILED_AUTO_SEQ = []


class MainModule:
    def __init__(self, root):
        print('main module')



def execute(all_seq):
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
                split_single_to_multiple(seq)

            else:
                execute_single(seq)
                sleep(seq.wait)

    # Failed
    failed = filter(lambda s: not s.success, all_seq)
    count_all = len(list(all_seq))
    count_failed = len(list(failed))
    print('Success: ', count_all - count_failed, '/', count_all)


def execute_single(seq):
    print("Locating... ", seq.desc, seq.type, seq.attribute_id, seq.attribute_value)

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
        else:
            print("ERROR: Not found")


# NOVA
def split_single_to_multiple(s):
    global AUTO_SEQ
    print('split_single_to_multiple from ', s.attribute_id, s.attribute_value)
    similar = find_similar(s)
    AUTO_SEQ.extend(similar)
    AUTO_SEQ.sort(key=lambda x: x.attribute_value)

    print(AUTO_SEQ)
    repetitve_execute()


def repetitve_execute():
    global AUTO_SEQ, AUTO_SEQ_DONE
    print('repetitve_execute')

    undone = [x for x in AUTO_SEQ if x not in AUTO_SEQ_DONE]
    print('AUTO_SEQ count: ', len(AUTO_SEQ), 'undone count: ', len(undone))
    for u in undone:
        AUTO_SEQ_DONE.append(u)
        execute_single(u)
        similar = find_similar(u)
        new = [x for x in similar if x not in AUTO_SEQ]
        AUTO_SEQ.extend(new)
        AUTO_SEQ.sort(key=lambda x: x.attribute_value)
        sleep(u.wait)

        if len(new) > 0:
            print('Ponovno od začetka, ker so od začetka')
            repetitve_execute()
            break


        if len(AUTO_SEQ) > len(AUTO_SEQ_DONE):
            print('Ponovno od začetka')
            repetitve_execute()
            break
        else:
            break
