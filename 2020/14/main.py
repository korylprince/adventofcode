import re
from collections import defaultdict, deque

maskRegexp = r"^mask = ([X10]{36})$"
memRegexp = r"^mem\[(\d+)\] = (\d+)$"

mem = defaultdict(lambda:0)

with open("./input.txt") as f:
    lines = f.read().strip().splitlines()
    mask = None
    for l in lines:
        if "mask" in l:
            mask = (
                eval(f"0b{re.match(maskRegexp, l).groups()[0].replace('X', '1')}"), # AND
                eval(f"0b{re.match(maskRegexp, l).groups()[0].replace('X', '0')}"), # OR
            )

        else:
            addr, val = re.match(memRegexp, l).groups()
            mem[int(addr)] = int(val) & int(mask[0]) | int(mask[1])

print("Answer 1:", sum(mem.values()))


def masks(mask):
    q = deque(((mask.replace("0", "1"), mask),))
    while len(q) > 0:
        mand, mor = q.popleft()
        if "X" not in mand:
            yield eval(f"0b{mand}"), eval(f"0b{mor}")
            continue
        q.append((mand.replace("X", "0", 1), mor.replace("X", "0", 1)))
        q.append((mand.replace("X", "1", 1), mor.replace("X", "1", 1)))


mem = defaultdict(lambda:0)

with open("./input.txt") as f:
    lines = f.read().strip().splitlines()
    mask = None
    for l in lines:
        if "mask" in l:
            mask = re.match(maskRegexp, l).groups()[0]
        else:
            addr, val = re.match(memRegexp, l).groups()
            for mand, mor in masks(mask):
                mem[int(addr) & mand | mor] = int(val)


print("Answer 2:", sum(mem.values()))
