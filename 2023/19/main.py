import re
import math

def parseRule(rule):
    name, rest = re.match(r"([a-z]+){(.*)}", rule).groups()
    rules = tuple(tuple(r.split(":")) for r in rest.split(","))
    # name : (rules..., otherwise)
    return name, (rules[:-1], rules[-1][0])

def parsePart(part):
    return tuple(int(n) for n in re.findall(r"\d+", part))

with open("./input.txt") as f:
    rulestext, partstext = f.read().strip().split("\n\n")
    rules = dict([parseRule(line) for line in rulestext.strip().splitlines()])
    parts = [parsePart(line) for line in partstext.strip().splitlines()]

accepted = set()

def process(x, m, a, s, workflow):
    if workflow == "A":
        accepted.add((x, m, a, s))
        return
    elif workflow == "R":
        return

    w = rules[workflow]
    for rule, result in w[0]:
        if eval(rule):
            return process(x, m, a, s, result)

    return process(x, m, a, s, w[1])

for part in parts:
    process(*part, workflow="in")

print("Answer 1:", sum([sum(p) for p in accepted]))

accepted = set()

def solve(part, workflow):
    if workflow == "A":
        accepted.add((part["x"], part["m"], part["a"], part["s"]))
        return
    elif workflow == "R":
        return

    w = rules[workflow]
    for rule, result in w[0]:
        letter, amount = re.split("[<>]", rule)
        amount = int(amount)
        sym = rule[1]
        if sym == "<":
            if part[letter][0] < amount:
                if part[letter][1] < amount:
                    return solve(part, result)
                # first half - meets condition
                part2 = part.copy()
                part2[letter] = (part[letter][0], amount - 1)
                solve(part2, result)
                # second half - doesn't meet condition
                part2 = part.copy()
                part2[letter] = (amount, part[letter][1])
                return solve(part2, workflow)
        elif sym == ">":
            if part[letter][1] > amount:
                if part[letter][0] > amount:
                    return solve(part, result)
                # first half - doesn't meet condition
                part2 = part.copy()
                part2[letter] = (part[letter][0], amount)
                solve(part2, workflow)
                # second half - meets condition
                part2 = part.copy()
                part2[letter] = (amount + 1, part[letter][1])
                return solve(part2, result)

    return solve(part, w[1])

for part in parts:
    solve({"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}, workflow="in")

total = 0
for part in accepted:
    total += math.prod([b-a+1 for a, b, in part])

print("Answer 2:", total)
