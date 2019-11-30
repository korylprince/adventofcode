import sys

with open("./input.txt") as f:
    ids = [x.strip() for x in f.read().splitlines()]

idMap = {id: {letter: id.count(letter) for letter in id} for id in ids}

twoCount = 0
threeCount = 0

for id, letterMap in idMap.items():
    for letter, count in letterMap.items():
        if count == 2:
            twoCount += 1
            break

    for letter, count in letterMap.items():
        if count == 3:
            threeCount += 1
            break

print("Twos:", twoCount)
print("Threes:", threeCount)
print("Checksum:", twoCount * threeCount)

for id1 in ids:
    for id2 in ids:
        mismatchCount = 0
        mismatchIDX = 0
        for idx in range(len(id1)):
            if id1[idx] != id2[idx]:
                mismatchCount += 1
                mismatchIDX = idx
                if mismatchCount > 1:
                    break
        if mismatchCount == 1:
            print("Common ID letters:", id1[:idx] + id1[idx+1:])
            sys.exit(0)
