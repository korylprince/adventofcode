from collections import deque

G = dict()

with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            G[(x, y)] = char
    start = [coords for coords, char in G.items() if char == "S"][0]
    end = [coords for coords, char in G.items() if char == "E"][0]
    G[start] = "a"
    G[end] = "z"


def bfs(G, start, cmp, target):
    seen = set(start)
    q = deque([(0, start)])
    while True:
        length, (x, y) = q.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if target((x, y)):
            return length
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x1, y1 = x+dx, y+dy
            if (x1, y1) in seen or (x1, y1) not in G:
                continue
            if cmp(G[(x, y)], G[(x1, y1)]):
                q.append((length+1, (x1, y1)))

print("Answer 1:", bfs(G, start, lambda a, b: ord(a) + 1 >= ord(b), lambda c: c == end))
print("Answer 2:", bfs(G, end, lambda a, b: ord(a) - 1 <= ord(b), lambda c: G[c] == "a"))
