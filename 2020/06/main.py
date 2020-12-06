with open("./input.txt") as f:
    groups = [[set(p) for p in g.strip().split("\n")] for g in f.read().strip().split("\n\n")]

print("Answer 1:", sum([len(set.union(*g)) for g in groups]))
print("Answer 1:", sum([len(set.intersection(*g)) for g in groups]))
