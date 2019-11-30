from collections import deque, defaultdict

with open("./input.txt") as f:
    input = int(f.read().strip())

def generate(target):
    path = [(0, 0), (1, 0)]
    pathSet = set(path)
    d = deque(((0, 1), (-1, 0), (0, -1), (1, 0)))

    while len(path) != target:
        next = (path[-1][0] + d[0][0], path[-1][1] + d[0][1])

        if next in pathSet:
            d.rotate(1)
            next = (path[-1][0] + d[0][0], path[-1][1] + d[0][1])
            d.rotate(-1)

        path.append(next)
        pathSet.add(next)

        if abs(path[-1][0]) == abs(path[-1][1]):
            d.rotate(-1)

    return path

path = generate(input)

print("Answer 1:", path[-1][0] + path[-1][1])

def generate2(target):
    path = [(0, 0), (1, 0)]
    pathSet = set(path)
    pathValues = defaultdict(lambda:0, {(0, 0): 1, (1, 0): 1})

    d = deque(((0, 1), (-1, 0), (0, -1), (1, 0)))
    adj = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))

    while pathValues[path[-1]] <= target:
        next = (path[-1][0] + d[0][0], path[-1][1] + d[0][1])

        if next in pathSet:
            d.rotate(1)
            next = (path[-1][0] + d[0][0], path[-1][1] + d[0][1])
            d.rotate(-1)

        path.append(next)
        pathSet.add(next)

        num = 0
        for a in adj:
            num += pathValues[(next[0] + a[0], next[1] + a[1])]
        pathValues[next] = num

        if abs(path[-1][0]) == abs(path[-1][1]):
            d.rotate(-1)

    return num

print("Answer 2", generate2(input))
