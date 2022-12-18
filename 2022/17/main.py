from itertools import cycle
from collections import defaultdict

from PIL import Image

LEFT, RIGHT = "<", ">"
jetdir = {LEFT: -1, RIGHT: 1}

rocks = cycle((
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
))

with open("./input.txt") as f:
    text = f.read().strip()
    jets = cycle(text)


def translatex(rock, dx):
    for idx in range(len(rock)):
        rock[idx][0] += dx

def translatey(rock, dy):
    for idx in range(len(rock)):
        rock[idx][1] += dy

def checkwalls(rock, dx):
    for p in rock:
        if not (0 <= p[0]+dx <= 6):
            return False
    return True

def checkblock(rock, G, dx, dy):
    for x, y in rock:
        if (x+dx, y+dy) in G:
            return False
    return True

def prune(G, top):
    for p in [p for p in G if p[1] < top - 100]:
        G.remove(p)


target = 1_000_000_000_000 - 1 # -1 for zero-based indexing
G = set([(x, 0) for x in range(7)])
top = 0
idx = -1
part1 = None
tracker = defaultdict(list)
initial = None
divisor = None
amount = None
tgtidx = -1

while True:
    idx += 1

    # rock falling procedure
    rock = [[x+2, y+top+4] for x, y in next(rocks)]
    while True:
        dir = jetdir[next(jets)]
        if checkwalls(rock, dir) and checkblock(rock, G, dir, 0):
            translatex(rock, dir)
        if not checkblock(rock, G, 0, -1):
            break
        translatey(rock, -1)
    G.update([(x, y) for x, y in rock])
    top = max([p[1] for p in rock] + [top])
    prune(G, top)

    # part 1
    if idx == 2021:
        print("Answer 1:", top)

    # part 2 after finding divisor
    if idx == tgtidx:
        modulus = top - (initial + ((idx // divisor) - 1) * amount)
        part2 = initial + ((target // divisor) - 1) * amount + modulus
        print("Answer 2:", part2)
        break

    # skip tracking after finding divisor
    if divisor is not None:
        continue

    # track differences for divisors and return the first one that is the same for 3 times in a row
    if idx != 0:
        tracker[idx] = [(top, top)]

    for i in [i for i in tracker if idx % i == 0]:
        tracker[i].append((top, top-tracker[i][-1][0]))
        if len(tracker[i]) > 3 and tracker[i][-1][1] == tracker[i][-2][1] == tracker[i][-3][1] == tracker[i][-4][1]:
            # divisor is how many shapes are required to have a perfect cycle
            divisor = i
            # initial is the height for the first cycle since it's different
            initial = tracker[i][0][0]
            # amount is the height per normal cycle
            amount = tracker[i][-1][1]
            # run for modulus more cycles
            tgtidx = idx + (target % divisor)
            # delete tracker
            tracker = None
            break
        elif len(tracker[i]) > 3 and tracker[i][-1][1] != tracker[i][-2][1]:
            del tracker[i]
