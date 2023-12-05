import re
from itertools import batched

with open("./input.txt") as f:
    sections = [line.strip() for line in f.read().strip().split("\n\n")]
    seeds = [int(m) for m in re.findall(r"\d+", sections[0])]
    maps = [] # [(dest, source, length), ...]
    for section in sections[1:]:
        m = []
        for line in section.splitlines()[1:]:
            m.append(tuple(int(m) for m in re.findall(r"\d+", line)))
        maps.append(m)

def seed_to_location(seed, maps):
    if len(maps) == 0:
        return seed
    for dest, source, length in maps[0]:
        if source <= seed <= source+length - 1:
            return seed_to_location(dest + seed-source, maps[1:])
    return seed_to_location(seed, maps[1:])

print("Answer 1:", min([seed_to_location(seed, maps) for seed in seeds]))

def intersect(a, l1, b, l2):
    return a <= (b + l2-1) and b <= (a + l1-1)

# splits up ranges so that at most one mapping intersects
def split_ranges(ranges, map):
    intersections = dict()
    for dest, source, length in map:
        idx = 0
        while idx < len(ranges):
            if not intersect(ranges[idx][0], ranges[idx][1], source, length):
                idx += 1
                continue
            intersections[ranges[idx]] = (dest, source, length)
            if ranges[idx][0] < source < ranges[idx][0] + ranges[idx][1]:
                ranges.insert(idx+1, (source, ranges[idx][1] - (source - ranges[idx][0])))
                ranges[idx] = (ranges[idx][0], source - ranges[idx][0])
                intersections[ranges[idx+1]] = (dest, source, length)
            if ranges[idx][0] < source + length < ranges[idx][0] + ranges[idx][1]:
                ranges.insert(idx+1, (source+length, ranges[idx][1] - (length - (ranges[idx][0] - source))))
                ranges[idx] = (ranges[idx][0], length - (ranges[idx][0] - source))
                intersections[ranges[idx]] = (dest, source, length)
            idx += 1

    return intersections

# apply all mappings from one x->y map
def range_to_range(ranges, maps):
    if len(maps) == 0:
        return ranges
    intersections = split_ranges(ranges, maps[0])
    nextranges = []
    for range in ranges:
        if range in intersections:
            dest, source, length = intersections[range]
            nextranges.append((dest + (range[0] - source), range[1]))
        else:
            nextranges.append(range)
    return range_to_range(nextranges, maps[1:])

print("Answer 2:", min([start for start, length in range_to_range(list(batched(seeds, n=2)), maps)]))
