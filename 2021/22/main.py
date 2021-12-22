import re
from functools import cache
from itertools import combinations

with open("./input.txt") as f:
    lines = [l.strip() for l in f.read().strip().splitlines()]
    rules = []
    for l in lines:
        rules.append((1 if l[:3] == "on " else -1, *[int(i) for i in re.findall(r"\-?\d+", l)]))

def intersect1d(a1, a2, b1, b2):
    return max(a1, b1), min(a2, b2)

@cache
def intersect3d(A, B):
    # if any of the planes don't intersect
    if A[2] < B[1] or B[2] < A[1] or A[4] < B[3] or B[4] < A[3] or A[6] < B[5] or B[6] < A[5]:
        return None
    return (
        max(A[1], B[1]), min(A[2], B[2]),
        max(A[3], B[3]), min(A[4], B[4]),
        max(A[5], B[5]), min(A[6], B[6]),
    )

@cache
def size(A):
    return (A[1]-A[0]+1) * (A[3]-A[2]+1) * (A[5]-A[4]+1)

def compile(rules):
    newrules = [rules[0]]
    count = size(newrules[0][1:])
    for r1 in rules[1:]:
        for idx in range(len(newrules)):
            r2 = newrules[idx]
            C = intersect3d(r1, r2)
            if C is None:
                continue

            # old rule is addition, so subtract intersection
            if r2[0] == 1:
                count -= size(C)
                newrules.append((-1, *C))
            # old rule is subtraction, so add intersection
            else:
                count += size(C)
                newrules.append((1, *C))

        if r1[0] == 1:
            count += size(r1[1:])
            newrules.append(r1)

    return count

print("Answer 1:", compile([r for r in rules if max([abs(n) for n in r]) <= 50]))
print("Answer 2:", compile(rules))
