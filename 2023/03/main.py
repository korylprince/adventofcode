grid = dict()
maxy, maxx = 0, 0
with open("./input.txt") as f:
    lines = [line.strip() for line in f.read().strip().splitlines()]
    maxy = len(lines) - 1
    for y, line in enumerate(lines):
        maxx = len(line) - 1
        for x, char in enumerate(line):
            grid[(x, y)] = char

symbols = set([sym for sym in grid.values() if sym != "." and (not sym.isdigit())])

dirs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
pos = (-1, 0)

num = ""
part = False

partstart = (-1, -1)
partend = (-1, -1)
parts = []
# set(start...end) -> part number
partmap = dict()

def endnum():
    global num
    global part
    if len(num) == 0:
        return
    if part:
        parts.append(int(num))
        partpoints = frozenset([(x, partstart[1]) for x in range(partstart[0], partend[0]+1)])
        partmap[partpoints] = int(num)
    num = ""
    part = False

while True:
    # next step
    pos = (pos[0] + 1, pos[1])
    if pos[0] > maxx:
        endnum()
        pos = (0, pos[1] + 1)
    if pos[1] > maxy:
        endnum()
        break

    # find digit
    if (n := grid[pos]).isdigit():
        if num == "":
            partstart = pos
        partend = pos
        num += n
        if part:
            continue
        # check if adjacent
        for dx, dy in dirs:
            if grid.get((pos[0]+dx, pos[1]+dy), ".") in symbols:
                part = True
                break
    else:
        endnum()

print("Answer 1:", sum(parts))

ratios = 0
for x, y in [(x, y) for (x, y), v in grid.items() if v == "*"]:
    adjacent = set()
    for partpoints in partmap:
        for dx, dy in dirs:
            if (x+dx, y+dy) in partpoints:
                adjacent.add(partpoints)
                break
    if len(adjacent) == 2:
        adj1, adj2 = list(adjacent)
        ratios += partmap[adj1] * partmap[adj2]

print("Answer 2:", ratios)
