from collections import deque

with open("./input.txt") as f:
    hands = f.read().strip().split("\n\n")
    p1 = deque([int(line.strip()) for line in hands[0].strip().splitlines()[1:]])
    p2 = deque([int(line.strip()) for line in hands[1].strip().splitlines()[1:]])


while len(p1) != 0 and len(p2) != 0:
    c1 = p1.popleft()
    c2 = p2.popleft()
    if c1 > c2:
        p1 += [c1, c2]
    else:
        p2 += [c2, c1]

winner = p1 if len(p1) > 0 else p2
print("Answer 1:", sum([(i + 1) * c for i, c in enumerate(reversed(winner))]))

def recurse(p1, p2, level=0):
    seen = set()
    while len(p1) != 0 and len(p2) != 0:

        if (tuple(p1), tuple(p2)) in seen:
            return 1, 0
        seen.add((tuple(p1), tuple(p2)))

        c1 = p1.popleft()
        c2 = p2.popleft()

        if len(p1) >= c1 and len(p2) >= c2:
            winner, _ = recurse(deque(list(p1)[:c1]), deque(list(p2)[:c2]), level=level+1)
            if winner == 1:
                p1 += [c1, c2]
            else:
                p2 += [c2, c1]
        elif c1 > c2:
            p1 += [c1, c2]
        else:
            p2 += [c2, c1]

    if len(p1) > 0:
        return 1, sum([(i+1)*n for i, n in enumerate(reversed(p1))]) 
    return 2, sum([(i+1)*n for i, n in enumerate(reversed(p2))]) 

with open("./input.txt") as f:
    hands = f.read().strip().split("\n\n")
    p1 = deque([int(line.strip()) for line in hands[0].strip().splitlines()[1:]])
    p2 = deque([int(line.strip()) for line in hands[1].strip().splitlines()[1:]])

print("Answer 2:", recurse(p1, p2)[1])
