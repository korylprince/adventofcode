from functools import cache

with open("./input.txt") as f:
    nums = [int(n) for n in f.read().strip().split(" ")]

@cache
def process(n, count):
    if count == 0:
        return 1
    if n == 0:
        return process(1, count - 1)
    elif len(s := str(n)) % 2 == 0:
        return process(int(s[:len(s)//2]), count - 1) + process(int(s[len(s)//2:]), count - 1)
    else:
        return process(n * 2024, count - 1)
    
print("Answer 1:", sum([process(n, 25) for n in nums]))
print("Answer 2:", sum([process(n, 75) for n in nums]))
