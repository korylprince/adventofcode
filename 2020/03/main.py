import numpy as np

class Grid:
    def __init__(self, grid):
        self._grid = grid
        self.max_x = max([x for x, y in grid.keys()])
        self.max_y = max([y for x, y in grid.keys()])

    def __getitem__(self, key):
        x, y = key
        return self._grid[(x % (self.max_x + 1), y)]

g = {}
with open("./input.txt") as f:
    for y, line in enumerate(f.read().splitlines()):
        for x, char in enumerate(line):
            g[(x, y)] = char

grid = Grid(g)

def tree_count(grid, slope):
    pos = (0, 0)
    trees = 0
    while pos[1] < grid.max_y:
        pos = (pos[0] + slope[0], pos[1] + slope[1])
        if grid[pos] == "#":
            trees += 1

    return trees

slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))

print("Answer 1:", tree_count(grid, (3, 1)))
print("Answer 1:", np.prod([tree_count(grid, slope) for slope in slopes]))
