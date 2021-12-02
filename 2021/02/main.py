FWD = "forward"
UP = "up"
DOWN = "down"

with open("./input.txt") as f:
    cmds = [(lambda c, v: (c, int(v)))(*row.strip().split(" ")) for row in f.read().strip().splitlines()]

def part1(cmds):
    x = 0
    y = 0
    for d, v in cmds:
        if d == FWD:
            x += v
        elif d == UP:
            y -= v
        elif d == DOWN:
            y += v
    return x, y

x, y = part1(cmds)
print("Answer 1:", abs(x * y))

def part2(cmds):
    x = 0
    y = 0
    aim = 0
    for d, v in cmds:
        if d == FWD:
            x += v
            y += v * aim
        elif d == UP:
            aim -= v
        elif d == DOWN:
            aim += v
    return x, y

x, y = part2(cmds)
print("Answer 2:", abs(x * y))
