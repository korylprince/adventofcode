UP = "U"
DOWN = "D"
LEFT = "L"
RIGHT = "R"

moves = {UP: (0, -1), DOWN: (0, 1), LEFT: (-1, 0), RIGHT: (1, 0)}

d = ((0, 0), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))


with open("./input.txt") as f:
    commands = [(line.strip().split(" ")[0], int(line.strip().split(" ")[1])) for line in f.read().strip().splitlines()]

def move(H, T):
    while True:
        for dx, dy in d:
            if T == (H[0]+dx, H[1]+dy):
               return T 

        if H[0] == T[0]:
            return (T[0], H[1] - (H[1]-T[1])//2)
        if H[1] == T[1]:
            return (H[0] - (H[0]-T[0])//2, T[1])

        dx, dy = abs(H[0]-T[0])/(H[0]-T[0]), abs(H[1]-T[1])/(H[1]-T[1])
        T = (T[0]+dx, T[1]+dy)

H = (0, 0)
T = (0, 0)
seen = set()

for (dir, count) in commands:
    for i in range(count):
        dx, dy = moves[dir]
        H = (H[0]+dx, H[1]+dy)
        T = move(H, T)
        seen.add(T)

print("Answer 1:", len(set(seen)))

knots = [(0,0)]*10
seen = set()

for (dir, count) in commands:
    for i in range(count):
        dx, dy = moves[dir]
        knots[0] = (knots[0][0]+dx, knots[0][1]+dy)
        for idx in range(1, len(knots)):
            knots[idx] = move(knots[idx-1], knots[idx])
        seen.add(knots[-1])

print("Answer 2:", len(set(seen)))
