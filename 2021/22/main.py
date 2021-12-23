import re

with open("./input.txt") as f:
    lines = [l.strip() for l in f.read().strip().splitlines()]
    rules = []
    for l in lines:
        rules.append((l[:3].strip(), *[int(i) for i in re.findall(r"\-?\d+", l)]))

def intersect3d(A, B):
    # if any of the planes don't intersect
    if A[2] < B[1] or B[2] < A[1] or A[4] < B[3] or B[4] < A[3] or A[6] < B[5] or B[6] < A[5]:
        return None
    return (
        max(A[1], B[1]), min(A[2], B[2]),
        max(A[3], B[3]), min(A[4], B[4]),
        max(A[5], B[5]), min(A[6], B[6]),
    )

def size(A):
    return (A[1]-A[0]+1) * (A[3]-A[2]+1) * (A[5]-A[4]+1)

def count(rules):
    if len(rules) == 0:
        return 0

    if rules[0][0] == "off":
        return count(rules[1:])

    intersections = [intersect3d(rules[0], r) for r in rules[1:]]
    return size(rules[0][1:]) + count(rules[1:]) - count([(None, *r) for r in intersections if r is not None])

print("Answer 1:", count([r for r in rules if max([abs(n) for n in r[1:]]) <= 50]))
print("Answer 2:", count(rules))
