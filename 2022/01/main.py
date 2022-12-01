with open("./input.txt") as f:
    elves = [list(map(int, e.strip().splitlines())) for e in f.read().strip().split("\n\n")]

print("Answer 1:", max(map(sum, elves)))

sums = sorted(list(map(sum, elves)))
print("Answer 2:", sum(sums[-3:]))
