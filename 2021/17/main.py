import re

with open("./input.txt") as f:
    ints = [int(i) for i in re.findall(r"\-?\d+", f.read())]
    xlow, xhigh, ylow, yhigh = ints[0], ints[1], ints[2], ints[3]

def step(dx, dy, t):
    tw = t if dx > t else t - (t - dx)
    return (
        int((dx * (dx + 1) - (dx-tw) * ((dx-tw) + 1))/2), # x
        int((dy * (dy + 1) - (dy-t) * ((dy-t) + 1))/2), # y
        int((dy * (dy + 1))/2), # highest
    )

def find_intersect(dx, dy):
    t = dx
    x, y, h = step(dx, dy, t)

    # never reaches zone x
    if x < xlow:
        return

    # ends vertically in zone - track forward in time
    if x <= xhigh:
        t1 = t
        while y >= ylow:
            if y <= yhigh:
                return x, y, h
            t1 += 1
            x, y, h = step(dx, dy, t1)

    # goes past zone - track backward in time
    while x >= xlow:
        if x <= xhigh:
            if ylow <= y <= yhigh:
                return x, y, h
        t -= 1
        x, y, h = step(dx, dy, t)


m = (0, 0, 0)
count = 0
found = set()
# x and y ranges found with experimentation
for x in range(0, 300):
    for y in range(ylow-1, 100):
        res = find_intersect(x, y)
        if res is not None:
            count += 1
            found.add((x, y))
            if res[2] > m[2]:
                m = (x, y, res[2])

print("Answer 1:", m[2])
print("Answer 2:", count)
