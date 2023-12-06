import re
import math

with open("./input.txt") as f:
    lines = f.read().strip().splitlines()
    times = [int(n) for n in re.findall(r"\d+", lines[0])]
    dists = [int(n) for n in re.findall(r"\d+", lines[1])]
    map = list(zip(times, dists))

def calc(total, hold):
    return hold * (total-hold)

def find_roots(total, goal):
    # calc(...) is a parabola - binary search it's two roots
    a = 0
    b = total // 2
    while b - a > 1:
        c = (b+a) // 2
        if calc(total, c) <= goal:
            a = c
        else:
            b = c

    d = total // 2
    e = total
    while e - d > 1:
        c = (e+d) // 2
        if calc(total, c) > goal:
            d = c
        else:
            e = c
    return b, d

def wins(total, goal):
    r1, r2 = find_roots(total, goal)
    return r2 - r1 + 1

print("Answer 1:", math.prod([wins(total, goal) for total, goal in map]))

total = int("".join(re.findall(r"\d", lines[0])))
goal = int("".join(re.findall(r"\d", lines[1])))

print("Answer 2:", wins(total, goal))
