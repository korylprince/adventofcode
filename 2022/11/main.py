import re
from collections import deque
import math
from copy import deepcopy

class Monkey:
    def __init__(self, text):
        self.id = int(re.findall(r"Monkey (\d+)", text)[0])
        self.items = deque(eval(re.findall(r"Starting items:((?:\s(?:\d+),?)+)", text)[0].strip() + ","))
        self.op = eval("lambda old:" + re.findall("Operation: new = (.*)$", text, re.M)[0])
        self.test = int(re.findall(r"divisible by (\d+)", text)[0])
        self.true = int(re.findall(r"If true: throw to monkey (\d+)", text)[0])
        self.false = int(re.findall(r"If false: throw to monkey (\d+)", text)[0])
        self.inspect = 0

with open("./input.txt") as f:
    monkeys = [Monkey(text) for text in f.read().strip().split("\n\n")]
    monkeys = {m.id: m for m in monkeys}
    monkeys2 = deepcopy(monkeys)

def round(round1=True):
    for idx in range(len(monkeys)):
        m = monkeys[idx]
        while len(m.items) > 0:
            worry = m.op(m.items.popleft()) // 3 if round1 else m.op(m.items.popleft()) % (2*3*5*7*11*13*17*19)
            m.inspect += 1
            if worry % m.test == 0:
                monkeys[m.true].items.append(worry)
            else:
                monkeys[m.false].items.append(worry)

for i in range(20):
    round()

print("Answer 1:", math.prod(sorted([m.inspect for m in monkeys.values()])[-2:]))

monkeys = monkeys2
for i in range(10_000):
    round(False)

print("Answer 2:", math.prod(sorted([m.inspect for m in monkeys.values()])[-2:]))
