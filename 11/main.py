with open("./input.txt") as f:
    serial = int(f.read())


def power(x, y, serial):
    rack = x + 10
    power = rack * y
    power += serial
    power *= rack
    power = (power // 100) % 10
    return power - 5


def generateGrid(serial, xsize, ysize):
    grid = [[0 for x in range(xsize)] for x in range(ysize)]
    for y in range(1, ysize + 1):
        for x in range(1, xsize + 1):
            grid[y-1][x-1] = power(x, y, serial)

    return grid


def powerring(grid, x, y, size):
    sum = 0
    for x1 in range(x, x + size - 1):
        sum += grid[y + (size - 1) - 1][x1 - 1]

    for y1 in range(y, y + size - 1):
        sum += grid[y1 - 1][x + (size - 1) - 1]

    sum += grid[y + (size - 1) - 1][x + (size - 1) - 1]

    return sum


def powersum(grid, x, y, size):
    sum = 0
    sums = []
    for s in range(1, size + 1):
        sum += powerring(grid, x, y, s)
        sums.append((s, sum))

    return sums


best = (0, 0)
bestPower = 0
grid = generateGrid(serial, 300, 300)

for y in range(1, 299):
    for x in range(1, 299):
        sums = powersum(grid, x, y, 3)
        p = sums[-1][1]
        if p > bestPower:
            best = (x, y)
            bestPower = p

print("Best Power:", bestPower)
print("Best Coordinates:", best)

best = (0, 0, 0)
bestPower = 0

for y in range(1, 301):
    for x in range(1, 301):
        s = min(301 - y, 301 - x)
        sums = powersum(grid, x, y, s)
        for size, p in sums:
            if p > bestPower:
                best = (x, y, size)
                bestPower = p

print("Best Power:", bestPower)
print("Best Coordinates/Size:", best)
