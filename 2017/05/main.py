with open("./input.txt") as f:
    ins = [int(val.strip()) for val in f.read().strip().splitlines()]

pos = 0
steps = 0

while 0 <= pos < len(ins):
    delta = ins[pos]
    ins[pos] += 1
    pos += delta
    steps += 1

print("Answer 1:", steps)

with open("./input.txt") as f:
    ins = [int(val.strip()) for val in f.read().strip().splitlines()]

pos = 0
steps = 0

while 0 <= pos < len(ins):
    delta = ins[pos]
    if delta >= 3:
        ins[pos] -= 1
    else:
        ins[pos] += 1
    pos += delta
    steps += 1

print("Answer 2:", steps)
