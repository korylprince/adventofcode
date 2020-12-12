from collections import deque

d = deque(((1, 0), (0, 1), (-1, 0), (0, -1)))
loc = (0, 0)

with open("./input.txt") as f:
    for line in f.read().strip().splitlines():
        ins, amt = line[0], int(line[1:])
        if ins == "N":
            loc = (loc[0], loc[1] - amt)
        elif ins == "S":
            loc = (loc[0], loc[1] + amt)
        elif ins == "E":
            loc = (loc[0] + amt, loc[1])
        elif ins == "W":
            loc = (loc[0] - amt, loc[1])
        elif ins == "F":
            loc = (loc[0] + d[0][0] * amt, loc[1] + d[0][1] * amt)
        elif ins == "L":
            d.rotate(int(amt/90))
        elif ins == "R":
            d.rotate(int(-amt/90))

print("Answer 1:", abs(loc[0]) + abs(loc[1]))

loc = (0, 0)
wloc = (10, -1)

with open("./input.txt") as f:
    for line in f.read().strip().splitlines():
        ins, amt = line[0], int(line[1:])
        if ins == "N":
            wloc = (wloc[0], wloc[1] - amt)
        elif ins == "S":
            wloc = (wloc[0], wloc[1] + amt)
        elif ins == "E":
            wloc = (wloc[0] + amt, wloc[1])
        elif ins == "W":
            wloc = (wloc[0] - amt, wloc[1])
        elif ins == "F":
            loc = (loc[0] + wloc[0] * amt, loc[1] + wloc[1] * amt)
        elif ins == "L":
            for x in range(int(amt/90)):
                wloc = (wloc[1], -wloc[0])
        elif ins == "R":
            for x in range(int(amt/90)):
                wloc = (-wloc[1], wloc[0])

print("Answer 2:", abs(loc[0]) + abs(loc[1]))
