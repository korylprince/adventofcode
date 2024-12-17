import heapq
from collections import defaultdict

walls = set()

start = (0, 0)
end = (0, 0)
with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            match char:
                case "#":
                    walls.add((x, y))
                case "S":
                    start = (x, y)
                case "E":
                    end = (x, y)

def dijstrka():
    # (score, (x, y), (dx, dy), seen)
    q = [(0, start, (1, 0), set([(start, (1, 0))]))]

    best = None
    best_seats = set()
    lowest = defaultdict(lambda:1_000_000)
    while len(q) > 0:
        score, (x, y), (dx, dy), seen = heapq.heappop(q)

        if best is not None and score > best:
            continue

        if (x, y) == end:
            best = score
            best_seats = best_seats.union([s[0] for s in seen])

        if score <= lowest[((x, y), (dx, dy))]:
            lowest[((x, y), (dx, dy))] = score
        else:
            continue

        if (next := (x+dx, y+dy)) not in walls and next not in seen:
            s = seen.copy()
            s.add((next, (dx, dy)))
            heapq.heappush(q, (score+1, next, (dx, dy), s))

        if (x+dy, y-dx) not in walls and ((x, y), (dy, -dx)) not in seen:
            s = seen.copy()
            s.add(((x, y), (dy, -dx)))
            heapq.heappush(q, (score+1000, (x, y), (dy, -dx), s))

        if (x-dy, y+dx) not in walls and ((x, y), (-dy, dx)) not in seen:
            s = seen.copy()
            s.add(((x, y), (-dy, dx)))
            heapq.heappush(q, (score+1000, (x, y), (-dy, dx), s))

    return best, len(best_seats)

first, second = dijstrka()
print("Answer 1:", first)
print("Answer 2:", second)
