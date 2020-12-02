with open("./input") as f:
    nums = [int(row.strip()) for row in f.read().strip().splitlines()]


def prob1(nums):
    for x, a in enumerate(nums):
        for y, b in enumerate(nums):
            if x == y:
                continue
            if a + b == 2020:
                return a * b

def prob2(nums):
    for x, a in enumerate(nums):
        for y, b in enumerate(nums):
            if a + b > 2020 or x == y:
                continue
            for z, c in enumerate(nums):
                if z in (x, y):
                    continue
                if a + b + c == 2020:
                    return a * b * c

print("Answer 1:", prob1(nums))
print("Answer 2:", prob2(nums))
