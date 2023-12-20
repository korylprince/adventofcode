import re
from collections import deque, defaultdict
from itertools import pairwise
import math

LOW = 0
HIGH = 1

class Base:
    def __init__(self, name):
        self.name = name
        self.outputs = []
        self.inputs = []
        self.pulses = {LOW: 0, HIGH: 0}

    def add_input(self, input):
        self.inputs.append(input)

    def add_output(self, output):
        self.outputs.append(output)

    def recv(self, _, pulse):
        self.pulses[pulse] += 1

    def send(self, pulse):
        return self.name, pulse, self.outputs

class FlipFlop(Base):
    def __init__(self, name):
        super().__init__(name)
        self.on = False

    def recv(self, name, pulse):
        super().recv(name, pulse)
        if pulse == HIGH:
            return None

        self.on = not self.on

        if self.on: # if it *was* off
            return self.send(HIGH)

        # if it *was* on
        return self.send(LOW)

class Conjunction(Base):
    def __init__(self, name):
        super().__init__(name)
        self.last_pulses = {}

    def add_input(self, input):
        super().add_input(input)
        self.last_pulses[input.name] = LOW

    def recv(self, name, pulse):
        super().recv(name, pulse)
        self.last_pulses[name] = pulse

        if all([p == HIGH for p in self.last_pulses.values()]):
            return self.send(LOW)

        return self.send(HIGH)

class Broadcaster(Base):
    def recv(self, name, pulse):
        super().recv(name, pulse)
        return self.send(pulse)

    def button(self):
        return self.recv("button", LOW)

class Untyped(Base):
    def process(self, *_):
        pass

def get_modules():
    modules = {}
    with open("./input.txt") as f:
        ins = [re.match(r"([%&]?)([a-z]+) -> (.*)", line.strip()).groups() for line in f.read().strip().splitlines()]
        for i in ins:
            if i[0] == "":
                modules[i[1]] = Broadcaster(i[1])
            elif i[0] == "%":
                modules[i[1]] = FlipFlop(i[1])
            elif i[0] == "&":
                modules[i[1]] = Conjunction(i[1])
        for i in ins:
            module_names = [n.strip() for n in i[2].split(",")]
            for n in module_names:
                if n not in modules:
                    modules[n] = Untyped(n)
            outputs = [modules[n] for n in module_names]
            for o in outputs:
                modules[i[1]].add_output(o)
                o.add_input(modules[i[1]])
    return modules

modules = get_modules()
targets = [set(m.last_pulses.keys()) for m in modules.values() if modules["rx"] in m.outputs][0]
cycles = defaultdict(list)

def computer(modules, step):
    q = deque([modules["broadcaster"].button()])
    while len(q) > 0:
        sender, pulse, outputs = q.popleft()
        if sender in targets and pulse == HIGH:
            cycles[sender].append(step)
        for o in outputs:
            if (res := o.recv(sender, pulse)) is not None:
                q.append(res)

for i in range(1000):
    computer(modules, i)

low = sum(m.pulses[LOW] for m in modules.values())
high = sum(m.pulses[HIGH] for m in modules.values())
print("Answer 1:", low * high)

for i in range(1001, 10_000):
    computer(modules, i)

def diff(nums):
    return next(iter(set([b - a for a, b in pairwise(nums)])))

print("Answer 2:", math.lcm(*[diff(v) for v in cycles.values()]))
