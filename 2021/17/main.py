import re
from functools import cache

with open("./input.txt") as f:
    ints = [int(i) for i in re.findall(r"\-?\d+", f.read())]
    xlow, xhigh, ylow, yhigh = ints[0], ints[1], ints[2], ints[3]

@cache
def stepx(dx, t):
    tw = t if dx > t else t - (t - dx)
    return int((dx * (dx + 1) - (dx-tw) * ((dx-tw) + 1))/2)

@cache
def stepy(dy, t):
    return int((dy * (dy + 1) - (dy-t) * ((dy-t) + 1))/2)

@cache
def highest(dy, t):
    return int((dy * (dy + 1))/2)

@cache
def binx(dx, t):
    tgt = xhigh + 1
    low = 0
    high = t
    mid = None
    while low + 1 < high:
        mid = (high + low) // 2
        x = stepx(dx, mid)
        if x < tgt:
            low = mid
        elif x > tgt:
            high = mid
        else:
            return high
    return high

@cache
def biny(dy, t1, t2):
    tgt = yhigh + 1
    low = t1
    high = t2
    mid = None
    while low < high - 1:
        mid = (high + low) // 2
        y = stepy(dy, mid)
        if y > tgt:
            low = mid
        elif y < tgt:
            high = mid
        else:
            return low
    return low


def find_intersect(dx, dy):
    t = dx
    x = stepx(dx, t)

    # never reaches zone x
    if x < xlow:
        return

    # ends vertically in zone - track forward in time
    if x <= xhigh:
        t1 = biny(dy, t, t*2)
        y = stepy(dy, t1)
        while y >= ylow:
            if y <= yhigh:
                return x, y, highest(dy, t1)
            t1 += 1
            y = stepy(dy, t1)

    # goes past zone - track backward in time
    t = binx(dx, t)
    while x >= xlow:
        if x <= xhigh:
            y = stepy(dy, t)
            if ylow <= y <= yhigh:
                return x, y, highest(dy, t)
        t -= 1
        x = stepx(dx, t)


# find minimum x
xstart = 1
while stepx(xstart, xstart) < xlow:
    xstart += 1


m = (0, 0, 0)
count = 0
found = set()

for x in range(xstart, xhigh + 2):
    for y in range(ylow-1, 100): # y max found through experimentation
        res = find_intersect(x, y)
        if res is not None:
            count += 1
            found.add((x, y))
            if res[2] > m[2]:
                m = (x, y, res[2])

print("Answer 1:", m[2])
print("Answer 2:", count)
