from itertools import combinations
from collections import deque
import heapq

A, B, C, D = "A", "B", "C", "D"
costs = {A: 1, B: 10, C: 100, D: 1000}
d = ((1, 0), (-1, 0), (0, 1), (0, -1))

def dfs_target(spaces):
    def f(start, target, locations):
        s = deque(((0, start),))
        seen = set.union({coords for typ, coords in locations}, {start})
        paths = []
        while len(s) > 0:
            cost, (x, y) = s.pop()
            if (x, y) in target:
                paths.append((cost, (x, y)))
            for dx, dy in d:
                if (x1 := x+dx, y1 := y+dy) in spaces and (x1, y1) not in seen:
                    seen.add((x1, y1))
                    s.append((cost+1, (x1, y1)))
        return paths
    return f


def dijkstra(spaces, rooms, stops, targets, start):
    dfs = dfs_target(spaces)

    h = [(0, start)]
    seen = set()
    while len(h) > 0:
        cost, locs = heapq.heappop(h)

        if locs in seen:
            continue
        seen.add(locs)

        # win condition
        win = True
        for typ, coords in locs:
            if coords not in targets[typ]:
                win = False
                break
        if win:
            return cost

        for idx, (typ, coords) in enumerate(locs):
            # check that target room can be moved to
            tidx = -1
            for idx2, (typ2, coords2) in enumerate(locs):
                if idx == idx2:
                    continue
                if coords2 in targets[typ]:
                    # already partially filled: select next space
                    if typ == typ2:
                        tidx -= 1
                    # room occupied by wrong type
                    else:
                        tidx = None
                        break

            if tidx is not None:
                # already in target
                if coords in targets[typ]:
                    continue
                path = dfs(coords, {targets[typ][tidx]}, locs)
                if len(path) > 0:
                    c, next = path[0]
                    heapq.heappush(h, (cost + c*costs[typ], (*locs[:idx], (typ, next), *locs[idx+1:])))
                    continue

            # move into hallway
            if coords in rooms:
                for c, next in dfs(coords, stops, locs):
                    heapq.heappush(h, (cost + c*costs[typ], (*locs[:idx], (typ, next), *locs[idx+1:])))
                continue

def read_grid(fn):
    with open(fn) as f:
        grid = {(x, y): c for y, row in enumerate(f.read().splitlines()) for x, c in enumerate(row)}


    spaces = {k for k, v in grid.items() if v in list(costs.keys()) + ["."]}
    rooms = sorted([k for k, v in grid.items() if v in costs.keys()])
    doorways = {(x, min({y for x, y in rooms}) - 1) for x in {x for x, y in rooms}}
    stops = spaces.difference(rooms).difference(doorways)
    lr = len(rooms)//4
    targets = {A: rooms[:lr], B: rooms[lr:lr*2], C: rooms[lr*2:lr*3], D: rooms[lr*3:lr*4]}
    locations = tuple(sorted([(v, k) for k, v in grid.items() if v in costs.keys()], key=lambda a: (a[0], a[1][1], a[1][0])))
    return dijkstra(spaces, rooms, stops, targets, locations)

print("Answer 1:", read_grid("./input.txt"))
print("Answer 2:", read_grid("./input2.txt"))
