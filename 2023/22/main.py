import re

with open("./input.txt") as f:
    ins = [tuple(int(i) for i in re.findall(r"\d+", line.strip())) for line in f.read().strip().splitlines()]

blocks = []
for x1, y1, z1, x2, y2, z2 in ins:
    b = set()
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            for z in range(z1, z2+1):
                # no need to add inner blocks
                if z == z1 or z == z2:
                    b.add((x, y, z))
    # points, bottom z, top z
    blocks.append((b, z1, z2))

blocks.sort(key=lambda b: min(z for _, _, z in b[0]))

# this is a really slow brute force ¯\_(ツ)_/¯ 

def down(b):
    return set((x, y, z-1) for x, y, z, in b)

def fall(blocks):
    changed = set()
    for idx in range(len(blocks)):
        conflict = False
        while not conflict:
            b, bz, tz = blocks[idx]
            if bz == 1:
                break
            d = down(b)
            for jdx in range(len(blocks)):
                if idx == jdx:
                    continue
                if bz - 1 > blocks[jdx][2]:
                    continue
                if tz - 1 < blocks[jdx][1]:
                    continue
                if not d.isdisjoint(blocks[jdx][0]):
                    conflict = True
                    break
            if not conflict:
                blocks[idx] = (d, bz-1, tz-1)
                changed.add(idx)
    return changed

changed = [1]
while len(changed) != 0:
    changed = fall(blocks)

count = 0
total = 0
for idx in range(len(blocks)):
    newblocks = blocks.copy()
    newblocks.pop(idx)

    fallen = fall(newblocks)
    if len(fallen) == 0:
        count += 1
        continue
    changed = [1]
    while len(changed) != 0:
        changed = fall(newblocks)
        fallen.update(changed)
    total += len(fallen)

print("Answer 1:", count)
print("Answer 2:", total)
