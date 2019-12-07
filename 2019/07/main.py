import itertools
from collections import deque
import queue
import threading

def get_codes():
    with open("./input.txt") as f:
        return [int(i.strip()) for i in f.read().strip().split(",")]


def run(codes, inq, outq):
    idx = 0
    while True:
        code = "{:0>5}".format(codes[idx])
        op = int(code[3:])
        # halt
        if op == 99:
            return
        # add
        elif op == 1:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            codes[codes[idx+3]] = a + b
            idx += 4
        # multiply
        elif op == 2:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            codes[codes[idx+3]] = a * b
            idx += 4
        # input
        elif op == 3:
            codes[codes[idx+1]] = inq.get()
            idx += 2
        # output
        elif op == 4:
            a = codes[idx+1] if int(code[2]) else codes[codes[idx+1]]
            outq.put(a)
            idx += 2
        # jump if true
        elif op == 5:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            if a == 1:
                idx = b
            else:
                idx += 3
        # jump if false
        elif op == 6:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            if a == 0:
                idx = b
            else:
                idx += 3
        # jump if less than
        elif op == 7:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            codes[codes[idx+3]] = int(a < b)
            idx += 4
        # jump if eq
        elif op == 8:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            codes[codes[idx+3]] = int(a == b)
            idx += 4
        else:
            print("Unknown op:", op)
            return


def run_amps(phases):
    ab, bc, cd, de, ea = queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue()
    a = threading.Thread(target=run, args=(get_codes(), ea, ab))
    b = threading.Thread(target=run, args=(get_codes(), ab, bc))
    c = threading.Thread(target=run, args=(get_codes(), bc, cd))
    d = threading.Thread(target=run, args=(get_codes(), cd, de))
    e = threading.Thread(target=run, args=(get_codes(), de, ea))

    for t in (a, b, c, d, e):
        t.start()

    ea.put(phases[0])
    ea.put(0)
    ab.put(phases[1])
    bc.put(phases[2])
    cd.put(phases[3])
    de.put(phases[4])

    for t in (a, b, c, d):
        t.join()

    output = ea.get()
    e.join()
    return output

max_output = 0

for phases in itertools.permutations(range(5)):
    output = run_amps(phases)
    if output > max_output:
        max_output = output

print("Answer 1:", max_output)

max_output = 0

for phases in itertools.permutations(range(5, 10)):
    output = run_amps(phases)
    if output > max_output:
        max_output = output

print("Answer 2:", max_output)
