import numpy as np

with open("./input.txt") as f:
    textGrids = f.read().strip().split("\n\n")

def to_arr(grid):
    return np.array([[1 if c == "#" else 0 for c in line.strip()] for line in grid.strip().splitlines()], dtype="b")

def check_internal(arr, idx, count, target):
    idx2 = idx + 3
    while idx >= 0 and idx2 < len(arr):
        count += sum(abs(arr[idx] - arr[idx2]))
        if count > target:
            return False
        idx -= 1
        idx2 += 1
    return count == target

def check(arr, target):
    idx = 0
    while idx < len(arr) - 1:
        if (count := sum(abs(arr[idx] - arr[idx+1]))) <= target:
            if check_internal(arr, idx - 1, count, target):
                return idx + 1
        idx += 1

def full_check(arr, target):
    if (n := check(arr, target)) is not None:
        return 100 * n
    # rotate clockwise
    n = check(np.rot90(arr, 1, (1, 0)), target)
    return n

print("Answer 1:", sum([full_check(to_arr(grid), 0) for idx, grid in enumerate(textGrids)]))
print("Answer 2:", sum([full_check(to_arr(grid), 1) for idx, grid in enumerate(textGrids)]))
