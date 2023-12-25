import re
from itertools import combinations
import z3

with open("./input.txt") as f:
    lines = [tuple(int(n) for n in re.findall(r"-?\d+", line.strip())) for line in f.read().strip().splitlines()]

# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
def intersection(
        x1, y1, _z1, dx1, dy1, _dz1,
        x3, y3, _z2, dx2, dy2, _dz2,
):
    x2, y2 = x1+dx1, y1+dy1
    x4, y4 = x3+dx2, y3+dy2
 
    Px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)) 
 
    Py = ((x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4)) / \
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
 
    return Px, Py

total = 0
bounds = (200000000000000, 400000000000000)
for x_0_, y_0_ in combinations(lines, 2):
    try:
        x, y = intersection(*x_0_, *y_0_)
        if not (bounds[0] <= x <= bounds[1]) or not (bounds[0] <= y <= bounds[1]):
            continue
        if (x < x_0_[0] and x_0_[3] > 0) or (x > x_0_[0] and x_0_[3] < 0):
            continue
        if (x < y_0_[0] and y_0_[3] > 0) or (x > y_0_[0] and y_0_[3] < 0):
            continue
        total += 1
    except ZeroDivisionError:
        pass

print("Answer 1:", total)

solver = z3.Solver()
x0, y0, z0, dx, dy, dz = z3.Real("x0"), z3.Real("y0"), z3.Real("z0"), z3.Real("dx"), z3.Real("dy"), z3.Real("dz")

for idx, (x0_, y0_, z0_, dx_, dy_, dz_) in enumerate(lines[:3]):
    t_ = z3.Real(f"t_{idx}")
    solver.add(x0 + t_ * dx == x0_ + t_ * dx_)
    solver.add(y0 + t_ * dy == y0_ + t_ * dy_)
    solver.add(z0 + t_ * dz == z0_ + t_ * dz_)
    solver.add(t_ > 0)

solver.check()
solved = solver.model()
print("Answer 2:", solved.eval(x0 + y0 + z0))
