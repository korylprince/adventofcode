def parse(p):
    row = eval(f"0b{p[:7].replace('F', '0').replace('B', '1')}")
    col = eval(f"0b{p[7:].replace('L', '0').replace('R', '1')}")
    return row, col

with open("./input.txt") as f:
    passes = [parse(line.strip()) for line in f.read().strip().splitlines()]


def prob2(passes):
    ids = [row * 8 + col for row, col in passes]
    id = min(ids)
    while id < max(ids):
        if id not in ids and (id - 1) in ids and (id +1 ) in ids:
            return id
        id += 1

print("Answer 1:", max([row * 8 + col for row, col in passes]))
print("Answer 2:", prob2(passes))
