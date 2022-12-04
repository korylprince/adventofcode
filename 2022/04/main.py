with open("./input.txt") as f:
    pairs = [[r.split("-") for r in line.strip().split(",")] for line in f.read().strip().splitlines()]
    pairs = [(set(range(int(p[0][0]), int(p[0][1])+1)), set(range(int(p[1][0]), int(p[1][1])+1))) for p in pairs]

print("Answer 1:", len([p for p in pairs if p[0].issubset(p[1]) or p[1].issubset(p[0])]))
print("Answer 2:", len([p for p in pairs if len(p[0].intersection(p[1])) > 0]))
