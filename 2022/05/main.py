from collections import defaultdict
from copy import deepcopy
import re

stacks = defaultdict(list)

with open("./input.txt") as f:
    text = f.read()
    s, m = text.split("\n\n")
    numline = s.strip().splitlines()[-1]
    nums = [int(n) for n in re.findall(r"\d+", numline)]
    for num in nums:
        for line in s.splitlines()[-2::-1]:
            if (item := line[numline.index(str(num))]) not in (" ", "[", "]"):
                stacks[num].append(item)
    moves = [tuple(int(n) for n in re.findall(r"\d+", line)) for line in m.strip().splitlines()]

orig = deepcopy(stacks)

for m in moves:
    for c in range(m[0]):
        stacks[m[2]].append(stacks[m[1]].pop())

print("Answer 1:", "".join([stacks[n][-1] for n in nums]))

stacks = orig

for m in moves:
    pop = stacks[m[1]][-m[0]:]
    stacks[m[1]] = stacks[m[1]][:-m[0]]
    stacks[m[2]] += pop

print("Answer 2:", "".join([stacks[n][-1] for n in nums]))
