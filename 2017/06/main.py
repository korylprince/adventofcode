from collections import deque

with open("./input.txt") as f:
    banks = deque([int(b.strip()) for b in f.read().strip().split("\t")])

seen = set(tuple(banks))
seen2 = set()
cycles = 0
first = 0
next = 0

while True:
    val, idx = max(banks), banks.index(max(banks))
    banks[idx] = 0

    banks.rotate(-idx)
    for i in range(val):
        banks.rotate(-1)
        banks[0] += 1
    banks.rotate(idx + val)
    if tuple(banks) in seen:
        if first == 0:
            first = cycles
        if tuple(banks) in seen2:
            next = cycles
            break
        seen2.add(tuple(banks))
    seen.add(tuple(banks))
    cycles += 1

print("Answer 1:", first + 1)
print("Answer 2:", next - first)
