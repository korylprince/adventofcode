import numpy as np

with open("./input.txt") as f:
    dots, folds = f.read().strip().split("\n\n")
    dots = [(lambda row: (int(row[0]), int(row[1])))(row.split(",")) for row in dots.strip().splitlines()]
    folds = [(lambda row: (row[0][-1], int(row[1])))(row.split("=")) for row in folds.strip().splitlines()]

rows = [n for a, n in folds if a == "y"][0] * 2 + 1
cols = [n for a, n in folds if a == "x"][0] * 2 + 1

M = np.zeros((rows, cols), int)
M[[y for x, y in dots], [x for x, y in dots]] = 1

def fold(M, axis, n):
    m = None
    if axis == "x":
        m = M[:, 0:n] + np.fliplr(M[:, n+1:])
    elif axis == "y":
        m = M[0:n, :] + np.flipud(M[n+1:, :])

    return m

print("Answer 1:", np.count_nonzero(fold(M, *folds[0])))

for f in folds:
    M = fold(M, *f)

print("Answer 2:")
for y in range(len(M)):
    for x in range(len(M[0])):
        if M[y, x] > 0:
            print("#", end="")
        else:
            print(" ", end="")
    print()
