with open("./input.txt") as f:
    directions = [[x.strip() for x in line.strip().split(",")] for line in f.read().strip().splitlines()]

def wire_coords(segments):
    wire = [(0, 0)]
    dirs = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
    for s in segments:
        for i in range(int(s[1:])):
            wire.append((
                wire[-1][0] + dirs[s[0]][0],
                wire[-1][1] + dirs[s[0]][1],
            ))
    return wire

wire1 = wire_coords(directions[0])
wire2 = wire_coords(directions[1])

intersections = [i for i in (set(wire1)).intersection(set(wire2)) if i != (0, 0)]
print("Answer 1:", min([x + y for x, y in intersections]))

print("Answer 2:", min([wire1.index(i) + wire2.index(i) for i in intersections]))
