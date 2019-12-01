import math

with open("./input.txt") as f:
    nums = [int(line.strip()) for line in f.read().strip().splitlines()]

def op(num):
    return math.floor(num/3) - 2

def op2(num):
    f = math.floor(num/3) - 2
    if f > 0:
        return f + op2(f)
    return 0

print("Answer 1:", sum([op(num) for num in nums]))
print("Answer 2:", sum([op2(num) for num in nums]))
