from collections import deque
import re

from PIL import Image


def debug_print(*args):
    if debug:
        print(*args)


def get_clay(file):
    clay = []

    with open(file) as f:
        for line in f.read().strip().splitlines():
            groups = re.match("([xy])=(\d+), ([xy])=(\d+)..(\d+)", line).groups()
            groups = {groups[0]: [int(groups[1])], groups[2]: range(int(groups[3]), int(groups[4]) + 1)}
            for x in groups["x"]:
                for y in groups["y"]:
                    clay.append((x, y))

    return clay


def write_image(output, clay, water, still_water, sources):
    boundaries = (
        (min([x for x, y in clay+list(water)]),
        max([x for x, y in clay+list(water)])),
        (min([y for x, y in clay+list(water)]),
        max([y for x, y in clay+list(water)])),
    )

    img = Image.new("RGB", (boundaries[0][1] - boundaries[0][0] + 1, boundaries[1][1] - boundaries[1][0] + 1), "black")
    pixels = img.load() # Create the pixel map
    for x, y in clay:
        pixels[x - boundaries[0][0], y - boundaries[1][0]] = (255, 255, 255)
    for x, y in water:
        pixels[x - boundaries[0][0], y - boundaries[1][0]] = (0, 0, 255)
    for x, y in still_water:
        pixels[x - boundaries[0][0], y - boundaries[1][0]] = (0, 127, 255)
    for x, y in sources:
        pixels[x - boundaries[0][0], y - boundaries[1][0]] = (0, 255, 0)

    img.save(output)


def down(clay, water, still_water, start):
    y = start[1]
    while y <= max([y for x, y in clay]):
        if (start[0], y) in clay:
            return y - 1, True
        if (start[0], y) in still_water:
            if (start[0], y - 1) in water:
                return y - 1, True
            return y - 1, True
        y += 1
    return y - 1, False


def spread_left(clay, water, sources, start):
    x = start[0]
    while True:
        if (x - 1, start[1]) in clay:
            return x, False
        if (x, start[1] + 1) not in clay and (x, start[1] + 1) not in water:
            if (x + 1, start[1]) in sources:
                return x + 1, True
            return x, True
        x -= 1


def spread_right(clay, water, sources, start):
    x = start[0]
    while True:
        if (x + 1, start[1]) in clay:
            return x, False
        if (x, start[1] + 1) not in clay and (x, start[1] + 1) not in water:
            if (x - 1, start[1]) in sources:
                return x - 1, True
            return x, True
        x += 1


def generate_water(clay):
    sources = [(500, min([y for x, y in clay]))]
    source = sources[0]
    allsources = set([source])
    water = set()
    still_water = set()
    while sources:
        parent = source
        source = sources.pop()

        # fall down
        debug_print("falling from:", source)
        bottom, spread = down(clay, water, still_water, source)
        debug_print("Bottom found: {0}; should spread: {1}".format((source[0], bottom), spread))
        water.update([(source[0], y) for y in range(source[1], bottom + 1)])
        # if past bottom or hit water
        if bottom == max([y for x, y in clay]) or not spread:
            continue

        # fill bucket
        sourceleft, sourceright = False, False
        while not sourceleft and not sourceright and bottom >= source[1]:
            debug_print("spreading from:", (source[0], bottom))

            # spread left
            leftx, sourceleft = spread_left(clay, water, allsources, (source[0], bottom))
            debug_print("spread left until {0}; Was source: {1}".format(leftx, sourceleft))
            if sourceleft:
                if (leftx, bottom) not in allsources:
                    sources.append((leftx, bottom))
                    allsources.add((leftx, bottom))
                water.update([(x, bottom) for x in range(leftx + 1, source[0])])
            else:
                water.update([(x, bottom) for x in range(leftx, source[0])])

            # spread right
            rightx, sourceright = spread_right(clay, water, allsources, (source[0], bottom))
            debug_print("spread right until {0}; Was source: {1}".format(rightx, sourceright))
            if sourceright:
                if (rightx, bottom) not in allsources:
                    sources.append((rightx, bottom))
                    allsources.add((rightx, bottom))
                water.update([(x, bottom) for x in range(source[0] + 1, rightx)])
            else:
                water.update([(x, bottom) for x in range(source[0] + 1, rightx + 1)])

            if not sourceleft and not sourceright:
                still_water.update([(x, bottom) for x in range(leftx, rightx + 1)])

            if bottom == source[1]:
                debug_print("Hit source level. Re-adding source:", parent)
                sources.append(parent)

            # move to next level
            bottom -= 1

    return water, still_water, allsources


debug = False
clay = get_clay("./input.txt")
water, still_water, sources = generate_water(clay)
write_image("./output.bmp", clay, water, still_water, sources)
print("Answer 1:", len(water))
print("Answer 2:", len(still_water))
