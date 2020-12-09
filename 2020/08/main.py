import re
from collections import deque

import networkx as nx

class Computer:
    def __init__(self, code_file=None, instructions=None):
        if instructions is None:
            with open(code_file) as f:
                instructions = [re.match(r"^(\w+) \+?(-?\d+)$", line.strip()).groups() for line in f.read().strip().splitlines()]
                self.instructions = [(cmd, int(val)) for cmd, val in instructions]
        else:
            self.instructions = instructions
        self.ptr = 0
        self.accum = 0

    def acc(self, val):
        self.accum += val
        self.ptr += 1

    def jmp(self, val):
        self.ptr += val

    def nop(self, val):
        self.ptr += 1

    def execute(self):
        ins, val = self.instructions[self.ptr]
        if ins == "acc":
            self.acc(val)
        elif ins == "jmp":
            self.jmp(val)
        elif ins == "nop":
            self.nop(val)
        return self.ptr

    def run(self):
        seen = set()
        ptr = -1
        target = len(self.instructions)
        while True:
            if ptr == target:
                return "SUCCESS", self.accum
            if ptr in seen:
                return "LOOP", self.accum
            seen.add(ptr)
            if ptr > target:
                return "OOB", self.accum
            ptr = self.execute()
    

def dfs(instructions):
    q = deque(((0, 0, None),)) #ptr, accum, changed
    target = len(instructions)
    seen = set()
    while True:
        ptr, accum, changed = q.pop()
        if ptr == target:
            return accum
        elif (ptr, changed) in seen or ptr > target:
            continue
        seen.add((ptr, changed))

        ins, val = instructions[ptr]
        if changed is None:
            if ins == "nop":
                q.append((ptr + val, accum, ptr))
            elif ins == "jmp":
                q.append((ptr + 1, accum, ptr))
        if ins == "nop":
            q.append((ptr + 1, accum, changed))
        elif ins == "jmp":
            q.append((ptr + val, accum, changed))
        elif ins == "acc":
            q.append((ptr + 1, accum + val, changed))


def graph(instructions):
    G = nx.DiGraph()
    start = 0
    target = len(instructions)
    for i, (ins, val) in enumerate(instructions):
        if ins == "jmp":
            G.add_edge(i, i + val, weight=0)
        elif ins == "acc":
            G.add_edge(i, i + 1, weight=val)
        elif ins == "nop":
            G.add_edge(i, i + 1, weight=0)

    starting = {node for node in nx.dfs_tree(G, start).nodes()}
    winning = {edge[0] for edge in nx.edge_dfs(G, target, orientation="reverse")}
    for i in starting:
        ins, val = instructions[i]
        if ins == "nop" and i + val in winning:
            G.add_edge(i, i+val, weight=0)
            break
        elif ins == "jmp" and i + 1 in winning:
            G.add_edge(i, i+1, weight=0)
            break

    return nx.shortest_path_length(G, start, target, weight="weight")


comp = Computer("./input.txt")
print("Answer 1:", comp.run()[1])
print("Answer 2:", dfs(comp.instructions))
print("Answer 2 (graph):", graph(comp.instructions))
