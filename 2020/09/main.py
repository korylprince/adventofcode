PREAMBLE = 25

with open("./input.txt") as f:
    numbers = [int(line.strip()) for line in f.read().strip().splitlines()]

def check(numbers, idx, num):
    for x in numbers[idx-PREAMBLE:idx]:
        for y in numbers[idx-PREAMBLE:idx]:
            if num == x + y:
                return True
    return False

def prob1(numbers):
    idx = PREAMBLE
    while idx < len(numbers):
        num = numbers[idx]
        if not check(numbers, idx, num):
            return num
        idx += 1


def prob2(numbers, target):
    r = 2
    while True:
        for idx in range(0, len(numbers)-r + 2):
            ran = numbers[idx:idx+r]
            if sum(ran) == target:
                return max(ran) + min(ran)
        r += 1


target = prob1(numbers)
print("Answer 1:", target)
print("Answer 2:", prob2(numbers, target))
