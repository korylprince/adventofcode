with open("./input.txt") as f:
    start, end = [int(n.strip()) for n in f.read().strip().split("-")]

def valid(num):
    if not (start < num < end):
        return False
    dig = list(str(num))

    double = False
    for idx in range(len(dig) - 1):
        if dig[idx] > dig[idx+1]:
            return False
        if dig[idx] == dig[idx+1]:
            double = True

    return double

def valid2(num):
    dig = list(str(num))
    cur = None
    count = 0

    for d in dig:
        if cur == d:
            count += 1
            continue
        if count == 2:
            return True
        cur = d
        count = 1

    if count == 2:
        return True

    return False

valid_nums = []
valid2_nums = []

for num in range(start, end):
    if valid(num):
        valid_nums.append(num)
        if valid2(num):
            valid2_nums.append(num)

print("Answer 1:", len(valid_nums))
print("Answer 2:", len(valid2_nums))
