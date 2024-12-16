dxdy = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

walls = set()
boxes = set()
robot = (0, 0)

with open("./input.txt") as f:
    text = f.read().strip().split("\n\n")
    for y, line in enumerate(text[0].strip().splitlines()):
        for x, char in enumerate(line.strip()):
            match char:
                case "#":
                    walls.add((x, y))
                case "O":
                    boxes.add((x, y))
                case "@":
                    robot = (x, y)
    d = [dxdy[char] for char in text[1].strip().replace("\n", "")]

_robot = robot
_boxes = boxes.copy()

for dx, dy in d:
    next = (robot[0]+dx, robot[1]+dy) 
    if next not in walls and next not in boxes:
        robot = next
        continue
    elif next in walls:
        continue

    n = (next[0]+dx, next[1]+dy)
    while True:
        if n in boxes:
            n = (n[0]+dx, n[1]+dy)
            continue
        elif n in walls:
            break
        robot = next
        boxes.remove(next)
        boxes.add(n)
        break

print("Answer 1:", sum([b[0] + 100*b[1] for b in boxes]))

walls2 = set()
for x, y in walls:
    walls2.add((2*x, y))
    walls2.add((2*x + 1, y))

boxes2 = set()
linked = dict()
for x, y in _boxes:
    boxes2.add((2*x, y))
    boxes2.add((2*x + 1, y))
    linked[(2*x, y)] = (2*x + 1, y)
    linked[(2*x + 1, y)] = (2*x, y)

robot = (_robot[0]*2, _robot[1])

def printmap():
    print()
    maxx = max([x for x, _ in walls2])
    maxy = max([y for _, y in walls2])
    for y in range(maxy+1):
        for x in range(maxx+1):
            if (x, y) in walls2:
                print("#", end="")
            elif (x, y) in boxes2:
                print("O", end="")
            elif (x, y) == robot:
                print("@", end="")
            else:
                print(".", end="")
        print()


def move_box(box, dx, dy):
    next0 = (box[0][0]+dx, box[0][1]+dy)
    next1 = (box[1][0]+dx, box[1][1]+dy)

    if next0 in walls2 or next1 in walls2:
        return None

    moves = set([(box, (next0, next1))])
    if dx == 0 and next0 not in boxes2 and next1 not in boxes2:
        return moves
    elif dx == -1 and next0 not in boxes2:
        return moves
    elif dx == 1 and next1 not in boxes2:
        return moves


    if next0 not in box and next0 in boxes2:
        res = move_box(tuple(sorted((next0, linked[next0]))), dx, dy)
        if res is None:
            return None
        moves = moves.union(res)

    if next1 not in box and next1 in boxes2:
        res = move_box(tuple(sorted((next1, linked[next1]))), dx, dy)
        if res is None:
            return None
        moves = moves.union(res)

    return moves


for dx, dy in d:
    next = (robot[0]+dx, robot[1]+dy) 
    if next not in walls2 and next not in boxes2:
        robot = next
        continue
    elif next in walls2:
        continue

    moves = move_box(tuple(sorted((next, linked[next]))), dx, dy)
    if moves is None:
        continue

    for box, next_box in moves:
        boxes2.remove(box[0])
        boxes2.remove(box[1])
        del linked[box[0]]
        del linked[box[1]]
    for box, next_box in moves:
        boxes2.add(next_box[0])
        boxes2.add(next_box[1])
        linked[next_box[0]] = next_box[1]
        linked[next_box[1]] = next_box[0]

    robot = next

# make sure we only count everything once
final_boxes = {frozenset((k, v)) for k, v in linked.items()}
print("Answer 2:", sum([min(b1[0], b2[0]) + 100*b1[1] for b1, b2 in final_boxes]))
