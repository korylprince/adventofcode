import re
import heapq

import numpy as np

ruleRegexp = r"^((?:\w ?)+): (\d+)-(\d+) or (\d+)-(\d+)$"

with open("./input.txt") as f:
    sections = f.read().strip().split("\n\n")
    rules = [re.match(ruleRegexp, line).groups() for line in sections[0].splitlines()]
    rules = [(rule, int(a), int(b), int(c), int(d)) for rule, a, b, c, d in rules]
    ticket = [int(n) for n in sections[1].splitlines()[1].split(",")]
    other = [[int(n) for n in line.split(",")] for line in sections[2].splitlines()[1:]]

all_valid = set.union(*[set(range(a, b+1)).union(set(range(c, d+1))) for rule, a, b, c, d in rules])

good = []
rate = 0
for o in other:
    g = True
    for n in o:
        if n not in all_valid:
            rate += n
            g = False
    if g:
        good.append(o)

print("Answer 1:", rate)

names = {r[0] for r in rules}
valid = {rule: set(range(a, b+1)).union(set(range(c, d+1))) for rule, a, b, c, d in rules}
#transpose
fields = list(map(set, zip(*good)))

def solve():
    final = {}
    sets = {name: {i for i, f in enumerate(fields) if len(f.difference(rule)) == 0} for name, rule in valid.items()}
    while len(final) < len(names):
        found, val = [(name, val) for name, val in sets.items() if len(val) == 1][0]
        final[found] = list(val)[0]
        del sets[found]
        for name in sets:
            sets[name].remove(list(val)[0])

    return final

print("Answer 2:", np.prod([ticket[v] for name, v in solve().items() if "departure" in name]))

def astar():
    target = len(fields)
    precompute = {name: {i for i, f in enumerate(fields) if len(f.difference(rule)) == 0} for name, rule in valid.items()}
    h = [(len(idxs)-1, [name], [i]) for name, idxs in precompute.items() for i in idxs]
    heapq.heapify(h)
    while True:
        prio, names, idxs = heapq.heappop(h)
        if len(names) == target:
            return dict(zip(names, idxs))
        next = [(len(_idxs.difference(set(idxs)))-1, name, i) for name, _idxs in precompute.items() for i in _idxs if name not in names]
        for p, n, i in next:
            heapq.heappush(h, (prio+p, names+[n], idxs + [i]))

print("Answer 2:", np.prod([ticket[v] for name, v in astar().items() if "departure" in name]))
