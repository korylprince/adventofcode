from collections import deque

G = set()
with open("./input.txt") as f:
    for y, line in enumerate(f.read().strip().splitlines()):
        for x, char in enumerate(line.strip()):
            if char == "S":
                start = (x, y)
                char = "."
            if char == ".":
                G.add((x, y))
maxx, maxy = x, y

def bfs(G, start, max_steps, mod):
    seen = set()
    end = 0
    q = deque([(start[0], start[1], 0)])
    while len(q) > 0:
        x, y, steps = q.popleft()
        if steps > max_steps:
            continue
        if (x, y) in seen:
            continue
        if steps % 2 == mod:
            end += 1
        seen.add((x, y))

        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            newx, newy = x + dx, y + dy
            if (newx % (maxx + 1), newy % (maxy + 1)) in G:
                q.append((newx, newy, steps + 1))

    return end

print("Answer 1:", bfs(G, start, 64, 0))

# modified lagrange from day 9
def lagrange(n, sequence):
    def f(x, idx):
        num = 1
        den = 1
        for xn in [xn for xn in range(len(sequence)) if xn != idx]:
            num *= (x - xn)
            den *= (idx - xn)
        return int(num / den)

    return sum(sequence[idx] * f(n, idx) for idx in range(len(sequence)))

# due to the special diamond shape of the input, the number of plots grows quadratically every 2 x grid size (2 x 131)
# note: in theory, it's actually every grid size, but something about this bfs function calculates the wrong solution if just 131 is used
# so we calculate 3 points (0, goal % grid_size), (1, (goal % grid_size) + grid_size), (2, (goal % grid_size) + 2 * grid_size)
# we can then use lagrange interpolation to derive the quadratic formula from those three points - f(x)
# then f(goal // grid_size) is our solution (goal = (goal // grid_size) + (goal % grid_size)) 

grid_size = (maxx + 1) * 2
print("Answer 2:", lagrange(26501365 // grid_size, (
    bfs(G, start, 65 + grid_size * 0, 1),
    bfs(G, start, 65 + grid_size * 1, 1),
    bfs(G, start, 65 + grid_size * 2, 1),
)))
