from collections import deque, defaultdict
from itertools import cycle, product

with open("./input.txt") as f:
    lines = f.read().strip().splitlines()
    p1, p2 = int(lines[0].strip()[-1]), int(lines[1].strip()[-1])

rolls = 0
d = cycle(range(1, 101))

def derdie():
    global rolls
    while True:
        rolls += 1
        yield next(d)

def part1():
    die = derdie()
    b1 = deque(range(1, 11))
    b1.rotate(-p1+1)
    b2 = deque(range(1, 11))
    b2.rotate(-p2+1)
    s1 = 0
    s2 = 0

    while True:
        b1.rotate(-(next(die) + next(die) + next(die)))
        s1 += b1[0]
        if s1 >= 1000:
            break
        b2.rotate(-(next(die) + next(die) + next(die)))
        s2 += b2[0]
        if s2 >= 1000:
            break
    return min(s1, s2) * rolls

print("Answer 1:", part1())

dice = list(product((1, 2, 3), repeat=3))
# turn, p1 position, p1 score, p2 position, p2 score: amount
state = defaultdict(lambda: 0, {(1, p1, 0, p2, 0): 1})
p1wins = 0
p2wins = 0
while len(state) > 0:
    newstate = defaultdict(lambda:0)
    for (turn, p1p, p1s, p2p, p2s), num in state.items():
        for d in dice:
            if turn == 1:
                p = ((p1p + sum(d) - 1) % 10) + 1
                ps = p1s + p
                if ps >= 21:
                    p1wins += num
                else:
                    newstate[(2, p, ps, p2p, p2s)] += num
            elif turn == 2:
                p = ((p2p + sum(d) - 1) % 10) + 1
                ps = p2s + p
                if ps >= 21:
                    p2wins += num
                else:
                    newstate[(1, p1p, p1s, p, ps)] += num
    state = newstate

print("Answer 2:", max(p1wins, p2wins))
