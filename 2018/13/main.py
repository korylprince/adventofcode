import sys


replaceMap = {"^": "|", "v": "|", ">": "-", "<": "-"}
velocityMap = {"^": (0, -1), "v": (0, 1), ">": (1, 0), "<": (-1, 0)}
symbolMap = {v: k for k, v in velocityMap.items()}


def sortTrains(trains):
    trains.sort(key=lambda t: t[0][1]*10000 + t[0][0])


def readTrack(file):
    with open(file) as f:
        tracks = [[x for x in y] for y in f.read().splitlines()]

    trains = []
    i = 0

    for y in range(len(tracks)):
        for x in range(len(tracks[y])):
            if tracks[y][x] in replaceMap:
                trains.append([(x, y), velocityMap[tracks[y][x]], 0])
                tracks[y][x] = replaceMap[tracks[y][x]]
                i += 1

    sortTrains(trains)

    return tracks, trains


def printTracks(tracks, trains):
    for y in range(len(tracks)):
        for x in range(len(tracks[y])):
            train = False
            for t in trains:
                if (x, y) == t[0]:
                    sys.stdout.write(symbolMap[t[1]])
                    train = True
            if not train:
                sys.stdout.write(tracks[y][x])
        sys.stdout.write("\n")


leftTurn = {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}
rightTurn = {(-1, 0): (0, -1), (0, -1): (1, 0), (1, 0): (0, 1), (0, 1): (-1, 0)}

def step(tracks, trains):
    sortTrains(trains)

    crashes = set()

    for train in trains:
        if train[0] in crashes:
            continue

        t = tracks[train[0][1]][train[0][0]]
        if t == "\\":
            train[1] = (train[1][1], train[1][0])
        elif t == "/":
            train[1] = (-train[1][1], -train[1][0])
        elif t == "+":
            train[2] += 1
            mod = train[2] % 3
            if mod == 1:
                train[1] = leftTurn[train[1]]
            elif mod == 0:
                train[1] = rightTurn[train[1]]

        train[0] = (train[0][0] + train[1][0], train[0][1] + train[1][1])

        c = checkCrash(trains)
        if len(c) > 0:
            crashes.add(c[0])

    return crashes


def checkCrash(trains):
        coords = [t[0] for t in trains]
        return [c for c in coords if coords.count(c) > 1]

def crash(tracks, trains):
    while True:
        crashes = step(tracks, trains)
        if len(crashes) > 0:
            return crashes

def crashUntilLast(tracks, trains):
    while len(trains) > 2:
        coords = crash(tracks, trains)
        trains = [t for t in trains if t[0] not in coords]
    return trains[0][0]

tracks, trains = readTrack("./input.txt")
print("First Crash:", crash(tracks, trains))

tracks, trains = readTrack("./input.txt")
print("Last Cart:", crashUntilLast(tracks, trains))
