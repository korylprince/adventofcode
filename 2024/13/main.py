import re
from fractions import Fraction

with open("./input.txt") as f:
    groups = f.read().strip().split("\n\n")
    claws = [[int(n) for n in re.findall(r"-?\d+", g)] for g in groups]

def solve(a, b, t, limit=False):
    # a0x + b0y = t0
    # a1x + b1y = t1
    # y = -a0 / b0 x + t0/b0
    # y = -a1 / b1 x + t1/b1
    m0 = Fraction(-a[0], b[0])
    m1 = Fraction(-a[1], b[1])
    if m0 == m1:
        return 0
    # y = m0 * x + t0/b0
    # y = m1 * x + t1/b1
    # x = (t1/b1 - t0/b0) / (m0 - m1)
    x = Fraction(Fraction(t[1], b[1]) - Fraction(t[0], b[0]), (m0 - m1))
    if x.denominator != 1:
        return 0
    x = x.numerator

    y = m0 * x + Fraction(t[0], b[0])
    if y.denominator != 1:
        return 0
    y = y.numerator

    if x < 0 or y < 0:
        return 0

    if limit and (x > 100 or y > 100):
        return 0

    return x * 3 + y

print("Answer 1:", sum([solve((c[0], c[1]), (c[2], c[3]), (c[4], c[5]), True) for c in claws]))

extra = 10000000000000
print("Answer 2:", sum([solve((c[0], c[1]), (c[2], c[3]), (c[4]+extra, c[5]+extra), False) for c in claws]))
