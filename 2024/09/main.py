EMPTY_ID = -1
ID_IDX = 0
START_IDX = 1
LENGTH_IDX = 2
# (id, start, length)
disk = []

with open("./input.txt") as f:
    nums = [int(n) for n in f.read().strip()]
    block = True
    block_id = 0
    idx = 0
    for length in nums:
        if block:
            disk.append((block_id, idx, length))
            block_id += 1
        else:
            disk.append((EMPTY_ID, idx, length))
        block = not block
        idx += length

if disk[-1][0] == EMPTY_ID:
    disk = disk[:-1]

diskcopy = disk[:]

block_idx = len(disk) - 1
empty_idx = 1
while empty_idx < block_idx:
    block = disk[block_idx]
    empty = disk[empty_idx]
    if block[LENGTH_IDX] == empty[LENGTH_IDX]:
        disk[empty_idx] = (block[ID_IDX], empty[START_IDX], empty[LENGTH_IDX])
        disk[block_idx] = (EMPTY_ID, block[START_IDX], block[LENGTH_IDX])
        block_idx -= 2
        empty_idx += 2
    elif block[LENGTH_IDX] > empty[LENGTH_IDX]:
        disk[empty_idx] = (block[ID_IDX], empty[START_IDX], empty[LENGTH_IDX])
        disk[block_idx] = (block[ID_IDX], block[START_IDX], block[LENGTH_IDX] - empty[LENGTH_IDX])
        # note: this leaves a hole after block_idx, but it doesn't matter
        empty_idx += 2
    elif block[LENGTH_IDX] < empty[LENGTH_IDX]:
        disk[block_idx] = (EMPTY_ID, block[START_IDX], block[LENGTH_IDX])
        disk[empty_idx] = (block[ID_IDX], empty[START_IDX], block[LENGTH_IDX])
        disk.insert(empty_idx+1, (EMPTY_ID, empty[START_IDX] + block[LENGTH_IDX], empty[LENGTH_IDX] - block[LENGTH_IDX]))
        empty_idx += 1
        block_idx -= 1


def checksum(disk):
    return sum([sum([id * idx for idx in range(start, start+length)]) for id, start, length in disk if id != EMPTY_ID])

print("Answer 1:", checksum(disk))

disk = diskcopy
block_idx = len(disk) - 1
for block_id in range(disk[-1][ID_IDX], -1, -1):
    while disk[block_idx][ID_IDX] != block_id:
        block_idx -= 1

    block = disk[block_idx]
    empty_idx = 1
    while empty_idx < block_idx:
        if disk[empty_idx][ID_IDX] != EMPTY_ID:
            empty_idx += 1
            continue

        empty = disk[empty_idx]
        if block[LENGTH_IDX] == empty[LENGTH_IDX]:
            disk[empty_idx] = (block[ID_IDX], empty[START_IDX], empty[LENGTH_IDX])
            disk[block_idx] = (EMPTY_ID, block[START_IDX], block[LENGTH_IDX])
            break
        elif block[LENGTH_IDX] > empty[LENGTH_IDX]:
            empty_idx += 1
        elif block[LENGTH_IDX] < empty[LENGTH_IDX]:
            disk[block_idx] = (EMPTY_ID, block[START_IDX], block[LENGTH_IDX])
            disk[empty_idx] = (block[ID_IDX], empty[START_IDX], block[LENGTH_IDX])
            disk.insert(empty_idx+1, (EMPTY_ID, empty[START_IDX] + block[LENGTH_IDX], empty[LENGTH_IDX] - block[LENGTH_IDX]))
            break

    block_idx -= 1

print("Answer 2:", checksum(disk))
