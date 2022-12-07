from collections import defaultdict

with open("./input.txt") as f:
    lines = [line.strip().split(" ") for line in f.read().strip().splitlines()]

dir = ()
sizes = defaultdict(lambda:0)

for line in lines:
    if line[1] == "cd":
        if line[2] == "..":
            dir = dir[:-1]
        else:
            dir = dir + (line[2],)
    elif line[0].isdigit():
        sizes[dir] += int(line[0])
        for idx in range(1, len(dir)):
            sizes[dir[:-idx]] += int(line[0])

print("Answer 1:", sum([v for v in sizes.values() if v <= 100_000]))

target = 30_000_000 - (70_000_000 - sizes[("/",)])
print("Answer 2:", min([v for v in sizes.values() if v >= target]))
