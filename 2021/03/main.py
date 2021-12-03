from collections import Counter
from copy import deepcopy

with open("./input.txt") as f:
    nums = [[int(b) for b in row.strip()] for row in f.read().strip().splitlines()]


gamma = 0
epsilon = 0
bits = len(nums[0])
for i in range(bits):
    b = Counter([n[i] for n in nums]).most_common(1)[0][0]
    gamma += b << (bits - i - 1)
    epsilon += (b ^ 1) << (bits - i - 1)

print("Answer 1:", gamma * epsilon)

def bitcount(nums, i):
    zero, one = 0, 0
    for n in nums:
        if n[i] == 0:
            zero += 1
        else:
            one += 1
    return zero, one

onums = deepcopy(nums)
for i in range(bits-1):
    ob = 1
    zero, one = bitcount(onums, i)
    if one > zero:
        ob = 1
    elif zero > one:
        ob = 0
    onums = [n for n in onums if n[i] == ob]
    if len(onums) == 1:
        break

cnums = deepcopy(nums)
for i in range(bits-1):
    cb = 0
    zero, one = bitcount(cnums, i)
    if one < zero:
        cb = 1
    elif zero < one:
        cb = 0

    cnums = [n for n in cnums if n[i] == cb]
    if len(cnums) == 1:
        break
    
o2 = 0
co2 = 0
for i in range(bits):
    o2 += onums[0][i] << (bits - i - 1)
    co2 += cnums[0][i] << (bits - i - 1)

print("Answer 2:", o2 * co2)
