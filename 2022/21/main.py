import re
import math

with open("./input.txt") as f:
    parsed = [re.search(r"(^[a-z]{4}): (\d+|[a-z]{4} [*\/+\-] [a-z]{4})$", line).groups() for line in f.read().strip().splitlines()]
    monkeys = {p[0]: int(p[1]) if p[1].isdigit() else p[1].strip().split(" ") for p in parsed}

def solve(monkeys, elem, humn = monkeys["humn"]):
    if elem == "humn":
        return humn
    if isinstance(v := monkeys[elem], int):
        return v
    k1, op, k2 = monkeys[elem]
    if op == "+":
        return solve(monkeys, k1, humn) + solve(monkeys, k2, humn)
    elif op == "-":
        return solve(monkeys, k1, humn) - solve(monkeys, k2, humn)
    elif op == "*":
        return solve(monkeys, k1, humn) * solve(monkeys, k2, humn)
    elif op == "/":
        return solve(monkeys, k1, humn) / solve(monkeys, k2, humn)

print("Answer 1:", int(solve(monkeys, "root")))

# find changing key
key = monkeys["root"][0]
target = solve(monkeys, monkeys["root"][2])
if int(solve(monkeys, key, 0)) == int(solve(monkeys, key, 1000)):
    target = solve(monkeys, key)
    key = monkeys["root"][2]

# find bounds
v1 = 1
v2 = 1
if solve(monkeys, key) > target:
    while solve(monkeys, key, v2) > target:
        v1 = v2
        v2 *= 2
else:
    while solve(monkeys, key, v1) < target:
        v2 = v1
        v1 *= 2

# binary search
while True:
    m = math.floor((v1+v2)/2)
    monkeys["humn"] = m
    if (s := solve(monkeys, key, m)) == target:
        print("Answer 2:", m)
        break
    elif s > target:
        v1 = m
    else:
        v2 = m
