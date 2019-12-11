import itertools
from collections import defaultdict, deque
import queue
import threading

class InfiniteList(list):
    def __getitem__(self, key):
        if key >= len(self):
            self += [0] * (key - (len(self) - 1))
        return super().__getitem__(key)

    def __setitem__(self, key, val):
        if key >= len(self):
            self += [0] * (key - (len(self) - 1))
        return super().__setitem__(key, val)

class Computer:
    def __init__(self, code_file):
        with open(code_file) as f:
            self.code = InfiniteList([int(i.strip()) for i in f.read().strip().split(",")])
        self.idx = 0
        self.rel = 0
        self.inq = queue.Queue()

    def input(self, *vals):
        for v in vals:
            self.inq.put(v)

    def mode_get(self, i, mode):
        if mode == "0":
            return self.code[self.code[i]]
        elif mode == "1":
            return self.code[i]
        elif mode == "2":
            return self.code[self.rel + self.code[i]]
        else:
            raise Exception("Unknown get mode {}".format(mode))

    def mode_set(self, i, val, mode):
        if mode == "0":
            self.code[self.code[i]] = val
        elif mode == "2":
            self.code[self.rel + self.code[i]] = val
        else:
            raise Exception("Unknown set mode {}".format(mode))

    def run(self):
        while True:
            code = "{:0>5}".format(self.code[self.idx])
            op = int(code[3:])
            # halt
            if op == 99:
                return
            # add
            elif op == 1:
                a = self.mode_get(self.idx+1, code[2])
                b = self.mode_get(self.idx+2, code[1])
                self.mode_set(self.idx + 3, a + b, code[0])
                self.idx += 4
            # multiply
            elif op == 2:
                a = self.mode_get(self.idx+1, code[2])
                b = self.mode_get(self.idx+2, code[1])
                self.mode_set(self.idx + 3, a * b, code[0])
                self.idx += 4
            # input
            elif op == 3:
                self.mode_set(self.idx + 1, self.inq.get(), code[2])
                self.idx += 2
            # output
            elif op == 4:
                a = self.mode_get(self.idx+1, code[2])
                self.idx += 2
                return a
            # jump if true
            elif op == 5:
                a = self.mode_get(self.idx+1, code[2])
                b = self.mode_get(self.idx+2, code[1])
                if a == 1:
                    self.idx = b
                else:
                    self.idx += 3
            # jump if false
            elif op == 6:
                a = self.mode_get(self.idx+1, code[2])
                b = self.mode_get(self.idx+2, code[1])
                if a == 0:
                    self.idx = b
                else:
                    self.idx += 3
            # jump if less than
            elif op == 7:
                a = self.mode_get(self.idx+1, code[2])
                b = self.mode_get(self.idx+2, code[1])
                self.mode_set(self.idx + 3, int(a < b), code[0])
                self.idx += 4
            # jump if eq
            elif op == 8:
                a = self.mode_get(self.idx+1, code[2])
                b = self.mode_get(self.idx+2, code[1])
                self.mode_set(self.idx + 3, int(a == b), code[0])
                self.idx += 4
            # add self.relative
            elif op == 9:
                a = self.mode_get(self.idx+1, code[2])
                self.rel += a
                self.idx += 2
            else:
                raise Exception("Unknown opcode {}".format(op))


seen = set()
paint = defaultdict(lambda:0)
loc = (0, 0)
dir = deque([(0, 1), (-1, 0), (0, -1), (1, 0)])
comp = Computer("./input.txt")

while True:
    comp.input(paint[loc])
    out = comp.run()
    if out is None:
        break
    paint[loc] = out
    seen.add(loc)
    out = comp.run()
    if out == 0:
        out = -1
    dir.rotate(out)
    loc = (loc[0] + dir[0][0], loc[1] + dir[0][1])

print("Answer 1:", len(seen))


seen = set()
paint = defaultdict(lambda:0)
loc = (0, 0)
paint[loc] = 1
dir = deque([(0, 1), (-1, 0), (0, -1), (1, 0)])
comp = Computer("./input.txt")

while True:
    comp.input(paint[loc])
    out = comp.run()
    if out is None:
        break
    paint[loc] = out
    seen.add(loc)
    out = comp.run()
    if out == 0:
        out = -1
    dir.rotate(out)
    loc = (loc[0] + dir[0][0], loc[1] + dir[0][1])

white = set([k for k, v in paint.items() if v])

minx, maxx = min([x[0] for x in white]), max([x[0] for x in white])
miny, maxy = min([x[1] for x in white]), max([x[1] for x in white])
width = maxx - minx
height = maxy - miny

print("Answer 2:")
for y in range(maxy, miny - 1, -1):
    for x in range(minx, maxx + 1):
        if (x, y) in white:
            print("#", end="")
        else:
            print(" ", end="")
    print("")
