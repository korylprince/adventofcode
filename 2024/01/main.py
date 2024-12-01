with open("./input.txt") as f:
    data = [[int(n) for n in line.strip().split(" ") if n != ""] for line in f.read().strip().splitlines()]

left = sorted([d[0] for d in data])
right = sorted([d[1] for d in data])

print("Answer 1:", sum([abs(left[idx] - right[idx]) for idx in range(len(left))]))

print("Answer 2:", sum([left[idx] * right.count(left[idx]) for idx in range(len(left))]))
