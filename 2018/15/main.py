from collections import deque
import sys


def get_grid(file):
    with open(file) as f:
        return [list(line) for line in f.read().splitlines()]


def print_grid(grid, units):
    for y in range(len(grid)):
        sys.stdout.write("".join(grid[y]))
        sys.stdout.write("\t")
        for x in range(len(grid[y])):
            if (x, y) in units:
                sys.stdout.write("{0}({1}), ".format(grid[y][x], units[(x, y)]))
        sys.stdout.write("\n")


def get_units(grid, power):
    units = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in "EG":
                units[(x, y)] = power

    return units


def move(grid, units, prev, next):
    grid[next[1]][next[0]] = grid[prev[1]][prev[0]]
    grid[prev[1]][prev[0]] = "."
    units[next] = units[prev]
    del units[prev]


def get_goals(grid, enemy):
    goals = set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == enemy:
                for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
                    if grid[y+dy][x+dx] == ".":
                        goals.add((x+dx, y+dy))

    return goals


def reading_order(items):
    return sorted(items, key=lambda i: (i[1], i[0]))[0]


def bfs_next_safe(grid, unit, goals):
    visited = [[False] * len(grid[0]) for r in range(len(grid))]
    visited[unit[1]][unit[0]] = True

    queue = deque([[unit]])

    while len(queue):
        paths = []
        found = []
        while len(queue):
            path = queue.popleft()
            x, y = c = path[-1]
            if c in goals:
                found.append(path)
                continue
            for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
                if grid[y+dy][x+dx] == "." and not visited[y+dy][x+dx]:
                    visited[y+dy][x+dx] = True
                    paths.append(path+[(x+dx, y+dy)])
        if len(found) > 0:
            dest = reading_order([p[-1] for p in found])
            return reading_order([p[1] for p in found if p[-1] == dest])

        queue = deque(paths)


def bfs_next(grid, unit, goals):
    visited = [[False] * len(grid[0]) for r in range(len(grid))]
    visited[unit[1]][unit[0]] = True

    queue = deque([[unit]])

    while len(queue):
        paths = []
        while len(queue):
            path = queue.popleft()
            x, y = c = path[-1]
            if c in goals:
                return path[1]
            for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
                if grid[y+dy][x+dx] == "." and not visited[y+dy][x+dx]:
                    visited[y+dy][x+dx] = True
                    paths.append(path+[(x+dx, y+dy)])

        queue = deque(sorted(paths, key=lambda p: (p[-1][1], p[-1][0], p[1][1], p[1][0])))


def get_targets(grid, unit, enemy):
    targets = []
    for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
        if grid[unit[1]+dy][unit[0]+dx] == enemy:
            targets.append((unit[0]+dx, unit[1]+dy))
    return targets


def attack(grid, units, targets, power):
    if len(targets) == 1:
        target = targets[0]
    else:
        targets = {t: units[t] for t in targets}
        target = reading_order([t for t, p in targets.items() if p == min(targets.values())])
    units[target] -= power
    if units[target] <= 0:
        grid[target[1]][target[0]] = "."
        del units[target]
        return target


def unit_turn(grid, units, unit, power):
    #check if unit died
    if unit not in units:
        return

    enemy = {"E": "G", "G": "E"}[grid[unit[1]][unit[0]]]
    power = {"E": power, "G": 3}[grid[unit[1]][unit[0]]]

    # check and targets
    targets = get_targets(grid, unit, enemy)
    if targets:
        return attack(grid, units, targets, power)

    # move
    goals = get_goals(grid, enemy)
    next = bfs_next(grid, unit, goals)
    if next is None:
        return
    move(grid, units, unit, next)

    # attack targets
    targets = get_targets(grid, next, enemy)
    if targets:
        return attack(grid, units, targets, power)


def cycle(grid, units, power):
    killed = []
    for u in sorted(units.keys(), key=lambda u: (u[1], u[0])):
        if u in killed:
            continue
        if not check(grid, units):
            return False
        k = unit_turn(grid, units, u, power)
        if k:
            killed.append(k)
    return True


def check(grid, units):
    e = [u for u in units if grid[u[1]][u[0]] == "E"]
    if len(e) == 0:
        return False
    g = [u for u in units if grid[u[1]][u[0]] == "G"]
    return len(g) != 0


def battle(file, power, debug=False):
    grid = get_grid(file)
    units = get_units(grid, 200)
    i = 0
    if debug:
        print("Round:", i)
        print_grid(grid, units)
    while True:
        i += 1
        if debug:
            print("Round:", i)

        if not cycle(grid, units, power):
            if debug:
                print_grid(grid, units)
            return (i - 1) * sum(units.values())

        if debug:
            print_grid(grid, units)


def findPower(file, debug=False):
    for power in range(3, 100):
        grid = get_grid(file)
        units = get_units(grid, 200)
        elveCount = len([u for u in get_units(grid, 200) if grid[u[1]][u[0]] == "E"])
        i = 0
        if debug:
            print("Round:", i)
            print_grid(grid, units)
        while True:
            i += 1
            if debug:
                print("Round:", i)

            if not cycle(grid, units, power):
                if debug:
                    print_grid(grid, units)
                if elveCount == len([u for u in get_units(grid, 200) if grid[u[1]][u[0]] == "E"]):
                    return (i - 1) * sum(units.values())
                break

            if debug:
                print_grid(grid, units)


print("Answer 1:", battle("./input.txt", 3))
print("Answer 2:", findPower("./input.txt"))
