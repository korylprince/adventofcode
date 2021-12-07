from collections import defaultdict
import statistics

with open("./input.txt") as f:
    nums = [int(n) for n in f.read().strip().split(",")]

median = int(statistics.median(nums))
print("Answer 1:", sum([abs(n - median) for n in nums]))

triangle = {0: 0}
for n in range(1, max(nums)-min(nums)+1):
    triangle[n] = n + triangle[n - 1]

def cost(x):
    return sum([triangle[abs(x - n)] for n in nums])

print("Answer 2:", min([cost(n) for n in range(min(nums), max(nums) + 1)]))
