from collections import defaultdict

START, END = "start", "end"

G = defaultdict(lambda:set())

with open("./input.txt") as f:
    for n1, n2 in [row.strip().split("-") for row in f.read().strip().splitlines()]:
        G[n1].add(n2)
        G[n2].add(n1)

def dfs(v, seen, twice):
    if v == END:
        return 1
    paths = 0
    for n in G[v]:
        if n.isupper():
            paths += dfs(n, seen, twice)
            continue
        if n not in seen:
            seen.add(n)
            paths += dfs(n, seen, twice)
            seen.remove(n)
        elif twice and n not in (START, END):
            paths += dfs(n, seen, False)
    return paths


print("Answer 1:", dfs(START, set((START,)), False))
print("Answer 2:", dfs(START, set((START,)), True))
