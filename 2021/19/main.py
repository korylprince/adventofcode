from itertools import combinations, pairwise, product
import networkx as nx

with open("./input.txt") as f:
    blocks = [b.strip().splitlines()[1:] for b in f.read().split("\n\n")]
    scanners = {idx: set(s) for idx, s in enumerate([[tuple(int(n) for n in beacon.split(",")) for beacon in b] for b in blocks])}

def dis(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1]) + abs(b[2] - a[2])

# also contains mirror transforms, but not worried about it
transforms = [(lambda x, y, z, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1)) for x1, y1, z1 in product((-1, 1), repeat=3)]
transforms += [(lambda x, z, y, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1)) for x1, y1, z1 in product((-1, 1), repeat=3)]
transforms += [(lambda y, x, z, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1)) for x1, y1, z1 in product((-1, 1), repeat=3)]
transforms += [(lambda y, z, x, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1)) for x1, y1, z1 in product((-1, 1), repeat=3)]
transforms += [(lambda z, x, y, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1)) for x1, y1, z1 in product((-1, 1), repeat=3)]
transforms += [(lambda z, y, x, x1=x1, y1=y1, z1=z1: (x*x1, y*y1, z*z1)) for x1, y1, z1 in product((-1, 1), repeat=3)]

# determine matching order
distances = {idx: set([dis(a, b) for a, b in combinations(s, 2)]) for idx, s in scanners.items()}
min_distances = len(list(combinations(range(12), 2)))
G = nx.Graph()
for a, b in combinations(range(len(scanners)), 2):
    if len(distances[a].intersection(distances[b])) >= min_distances:
        G.add_edge(a, b)

merged = scanners[0]
locations = [(0, 0, 0)]
for idx in list(nx.bfs_tree(G, 0))[1:]:
    # find matched points
    a = {p: set([dis(p, p1) for p1 in merged]) for p in merged}
    b = {p: set([dis(p, p1) for p1 in scanners[idx]]) for p in scanners[idx]}
    matched = []
    for p1, d1 in a.items():
        for p2, d2 in b.items():
            if len(d1.intersection(d2)) >= 11:
                matched.append((p1, p2))

    # find working transform
    transform = None
    for t in transforms:
        count = 0
        for (a1, b1), (a2, b2) in pairwise(matched):
            tb1, tb2 = t(*b1), t(*b2)
            if (a1[0] - a2[0], a1[1] - a2[1], a1[2] - a2[2]) != (tb1[0] - tb2[0], tb1[1] - tb2[1], tb1[2] - tb2[2]):
                break
            count += 1
        if count >= 11:
            transform = t
            break

    # transform and merge
    p = transform(*matched[0][1])
    transformed = set()
    for x, y, z in [p for p in scanners[idx] if p not in [m[1] for m in matched]]:
        x1, y1, z1 = transform(x, y, z)
        # translation (match point difference) + orientation (transform function)
        transformed.add((matched[0][0][0] - p[0] + x1, matched[0][0][1] - p[1] + y1, matched[0][0][2] - p[2] + z1))

    merged.update(transformed)
    locations.append((matched[0][0][0] - p[0], matched[0][0][1] - p[1], matched[0][0][2] - p[2]))

print("Answer 1:", len(merged))

max = 0
for l1, l2 in combinations(locations, 2):
    if (d := dis(l1, l2)) > max:
        max = d
print("Answer 2:", max)
