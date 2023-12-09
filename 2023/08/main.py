#!/opt/homebrew/bin/python3.12
import re
from itertools import cycle
import math

with open("./input.txt") as f:
    text = f.read().strip().split("\n\n")
    instructions = text[0].strip()
    maptext = [re.findall(r"[A-Z0-9]{3}", line) for line in text[1].strip().splitlines()]
    map = {m[0]: (m[1], m[2]) for m in maptext}

sides = {"L": 0, "R": 1}
def solve(start, target):
    ins = cycle(instructions)
    node = start
    steps = 0
    while node != target:
        node = map[node][sides[next(ins)]]
        steps += 1
    return steps

print("Answer 1:", solve("AAA", "ZZZ"))

ins = cycle(instructions)
nodes = [node for node in map if node[2] == "A"]
target = len(nodes)
steps = 0
tracker = {}
while len(tracker) != len(nodes):
    i = next(ins)
    steps += 1
    for idx in range(len(nodes)):
        nodes[idx] = map[nodes[idx]][sides[i]]
        # This is a finite directed graph, so each distinct cycle is always the same length. We just need to find the first time each target is found
        if nodes[idx][2] == "Z":
            tracker[nodes[idx]] = steps

# find the lcm of all cycle lengths
print("Answer 2:", math.lcm(*tracker.values()))
