from itertools import combinations

nodes = set()
galaxies = set()

with open("./input.txt") as f:
    text = f.read().strip()
    lines = text.splitlines()

    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            if char == "#":
                galaxies.add((x, y))
            nodes.add((x, y))

not_rows = set([y for _, y in galaxies])
not_cols = set([x for x, _ in galaxies])
rows = set([y for _, y in nodes if y not in not_rows])
cols = set([x for x, _ in nodes if x not in not_cols])

total = 0
total2 = 0
for n1, n2 in combinations(galaxies, 2):
    dis = abs(n2[0] - n1[0]) + abs(n2[1] - n1[1])
    total += dis
    total2 += dis
    if n1[0] != n2[0]:
        # how many empty columns passed over
        overcols = len(set(range(n1[0], n2[0], abs(n2[0] - n1[0]) // (n2[0] - n1[0]))).intersection(cols))
        total += overcols
        total2 += overcols * (1_000_000 - 1)
    if n1[1] != n2[1]:
        # how many empty rows passed over
        overrows = len(set(range(n1[1], n2[1], abs(n2[1] - n1[1]) // (n2[1] - n1[1]))).intersection(rows))
        total += overrows
        total2 += overrows * (1_000_000 - 1)

print("Answer 1:", total)
print("Answer 2:", total2)
