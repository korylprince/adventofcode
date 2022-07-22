# shamelessly stolen from https://www.reddit.com/r/adventofcode/comments/rnejv5/comment/hpu84cj/?utm_source=share&utm_medium=web2x&context=3

from collections import defaultdict

with open("./input.txt") as f:
    l = [line.split() for line in f.read().splitlines()]

const = []
for i in range(14):
    off = i * 18
    A = int(l[4+off][2])
    B = int(l[5+off][2])
    C = int(l[15+off][2])
    const.append((A,B,C))

levels = {}
def build_deps(i, zl):
    A,B,C = const[i]

    sols = defaultdict(list)
    for w in range(9, 0, -1):
        for z in zl:
            for a in range(A):
                pz = z * A + a
                if pz % 26 + B == w:
                    if pz // A == z:
                        sols[pz].append((w, z))

                pz = round((z - w - C) / 26 * A + a)
                if pz % 26 + B != w:
                    if pz//A * 26 + w + C == z:
                        sols[pz].append((w, z))

    assert sols
    levels[i] = sols

    if i > 0:
        build_deps(i-1, list(sols.keys()))

p1 = None
p2 = None
def solve(i, z, sol, largest=False):
    global p1, p2

    if i == 14:
        if largest:
            p1 = ''.join(str(j) for j in sol)
        else:
            p2 = ''.join(str(j) for j in sol)
        return True

    if z not in levels[i]:
        return False

    for w, nz in sorted(levels[i][z], reverse=largest):
        ts = (*sol, w)
        if solve(i+1, nz, list(ts), largest):
            return True

build_deps(13, [0])
solve(0, 0, [], largest=True)
solve(0, 0, [], largest=False)

print(p1)
print(p2)
