from collections import defaultdict
import itertools
import queue

grid = {}
with open("./input.txt") as f:
    for y, line in enumerate(f.read().splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = c

BLOCK_PATH = "."
BLOCK_WALL = "#"
BLOCK_PORTALS =  [chr(o) for o in range(ord("A"), ord("Z") + 1) if chr(o) in grid.values()]

def find_portals(grid):
    coords = [p for p, v in grid.items() if v in BLOCK_PORTALS]
    portals = defaultdict(lambda:[])
    for a, b in itertools.combinations(coords, 2):
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1:
            #hort
            if a[1] == b[1]:
                first = (min([a[0], b[0]]), a[1])
                second = (max([a[0], b[0]]), a[1])
                if (portal := (second[0] + 1, second[1])) in grid and grid[portal] == BLOCK_PATH:
                    portals["{}{}".format(grid[first], grid[second])].append(portal)
                elif (portal := (first[0] - 1, first[1])) in grid and grid[portal] == BLOCK_PATH:
                    portals["{}{}".format(grid[first], grid[second])].append(portal)
            #vert
            elif a[0] == b[0]:
                first = (a[0], min([a[1], b[1]]))
                second = (a[0], max([a[1], b[1]]))
                if (portal := (second[0], second[1] + 1)) in grid and grid[portal] == BLOCK_PATH:
                    portals["{}{}".format(grid[first], grid[second])].append(portal)
                elif (portal := (first[0], first[1] - 1)) in grid and grid[portal] == BLOCK_PATH:
                    portals["{}{}".format(grid[first], grid[second])].append(portal)

    return portals


def bfs(grid, source, target, portals):
    seen = set([source] + [k for k, v in grid.items() if v == BLOCK_WALL or v in BLOCK_PORTALS])
    q = queue.Queue()
    q.put([source])
    while True:
        path = q.get()
        pos = path[-1]
        if pos == target:
            return path
        for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if (new := (pos[0] + d[0], pos[1] + d[1])) not in seen:
                seen.add(new)
                q.put(path + [new])
        if pos in portals and (new := portals[pos]) not in seen:
            seen.add(new)
            q.put(path + [new])


def bfs2(grid, source, target, portals, outer_portals):
    walls = [k for k, v in grid.items() if v == BLOCK_WALL or v in BLOCK_PORTALS]
    seen = set([(source, 0)])
    q = queue.Queue()
    q.put((0, source, 0))
    while True:
        length, pos, level = q.get()
        # this is enough to find answer
        if level > 30:
            continue
        if level == 0 and pos == target:
            return length
        for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if (new := (pos[0] + d[0], pos[1] + d[1])) not in walls and (new, level) not in seen:
                seen.add((new, level))
                q.put((length + 1, new, level))
        if (new := portals.get(pos, None)) is not None:
            if pos in outer_portals:
                if level == 0 or (new, level - 1) in seen:
                    continue
                q.put((length + 1, new, level - 1))
                seen.add((new, level - 1))
            elif (new, level + 1) in seen:
                    continue
            else:
                q.put((length + 1, new, level + 1))
                seen.add((new, level + 1))


portals = find_portals(grid)

source = portals["AA"][0]
target = portals["ZZ"][0]

del portals["AA"]
del portals["ZZ"]

portal_map = {}
for a, b in portals.values():
    portal_map[a] = b
    portal_map[b] = a

path = bfs(grid, source, target, portal_map)
print("Answer 1:", len(path) - 1)

edges = ((
    min([x for (x, y), v in grid.items() if v == BLOCK_WALL]),
    max([x for (x, y), v in grid.items() if v == BLOCK_WALL]),
), (
    min([y for (x, y), v in grid.items() if v == BLOCK_WALL]),
    max([y for (x, y), v in grid.items() if v == BLOCK_WALL]),
))

outer_portals = [p for p in portal_map if p[0] in edges[0] or p[1] in edges[1]]

length = bfs2(grid, source, target, portal_map, outer_portals)
print("Answer 2:", length)
