import itertools
from collections import deque
import queue
import threading

def get_codes():
    with open("./input.txt") as f:
        return [int(i.strip()) for i in f.read().strip().split(",")]

class InfiniteList(list):
    def __getitem__(self, key):
        if key >= len(self):
            self += [0] * (key - (len(self) - 1))
        return super().__getitem__(key)

    def __setitem__(self, key, val):
        if key >= len(self):
            self += [0] * (key - (len(self) - 1))
        return super().__setitem__(key, val)


def run(codes, inq, outq):
    codes = InfiniteList(codes)
    idx = 0
    rel = 0

    def mode_get(i, mode):
        if mode == "0":
            return codes[codes[i]]
        elif mode == "1":
            return codes[i]
        elif mode == "2":
            return codes[rel + codes[i]]
        else:
            raise Exception("Unknown get mode {}".format(mode))

    def mode_set(i, val, mode):
        if mode == "0":
            codes[codes[i]] = val
        elif mode == "2":
            codes[rel + codes[i]] = val
        else:
            raise Exception("Unknown set mode {}".format(mode))

    while True:
        code = "{:0>5}".format(codes[idx])
        op = int(code[3:])
        # halt
        if op == 99:
            return
        # add
        elif op == 1:
            a = mode_get(idx+1, code[2])
            b = mode_get(idx+2, code[1])
            mode_set(idx + 3, a + b, code[0])
            idx += 4
        # multiply
        elif op == 2:
            a = mode_get(idx+1, code[2])
            b = mode_get(idx+2, code[1])
            mode_set(idx + 3, a * b, code[0])
            idx += 4
        # input
        elif op == 3:
            mode_set(idx + 1, inq.get(), code[2])
            idx += 2
        # output
        elif op == 4:
            a = mode_get(idx+1, code[2])
            outq.put(a)
            idx += 2
        # jump if true
        elif op == 5:
            a = mode_get(idx+1, code[2])
            b = mode_get(idx+2, code[1])
            if a == 1:
                idx = b
            else:
                idx += 3
        # jump if false
        elif op == 6:
            a = mode_get(idx+1, code[2])
            b = mode_get(idx+2, code[1])
            if a == 0:
                idx = b
            else:
                idx += 3
        # jump if less than
        elif op == 7:
            a = mode_get(idx+1, code[2])
            b = mode_get(idx+2, code[1])
            mode_set(idx + 3, int(a < b), code[0])
            idx += 4
        # jump if eq
        elif op == 8:
            a = mode_get(idx+1, code[2])
            b = mode_get(idx+2, code[1])
            mode_set(idx + 3, int(a == b), code[0])
            idx += 4
        # add relative
        elif op == 9:
            a = mode_get(idx+1, code[2])
            rel += a
            idx += 2
        else:
            raise Exception("Unknown opcode {}".format(op))


inq, outq = queue.Queue(), queue.Queue()
a = threading.Thread(target=run, args=(get_codes(), inq, outq))
a.start()
inq.put(1)
a.join()
while not outq.empty():
    print("Answer 1:", outq.get())

a = threading.Thread(target=run, args=(get_codes(), inq, outq))
a.start()
inq.put(2)
a.join()
while not outq.empty():
    print("Answer 2:", outq.get())
