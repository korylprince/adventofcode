import itertools

with open("./input.txt") as f:
    data = [[int(n) for n in line.split(" ")] for line in f.read().strip().splitlines()]

def is_safe(nums):
    is_positive = nums[1] > nums[0]
    for a, b in itertools.pairwise(nums):
        if not (((b > a) == is_positive) and (1 <= abs(b - a) <= 3)):
            return False
    return True

def other(nums):
    for idx in range(len(nums)):
        yield [x for i, x in enumerate(nums) if i != idx]

def is_really_safe(nums):
    if is_safe(nums):
        return True
    for n in other(nums):
        if is_safe(n):
            return True
    return False

print("Answer 1:", len(list(filter(is_safe, data))))
print("Answer 2:", len(list(filter(is_really_safe, data))))
