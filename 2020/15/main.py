with open("./input.txt") as f:
    nums = [int(n.strip()) for n in f.read().strip().split(",")]

last = {n: i for i, n in enumerate(nums[:-1])}

i = len(nums) - 1
n = nums[-1]

while True:
    if i == 2020 - 1:
        print("Answer 1:", n)
    elif i == 30000000 - 1:
        print("Answer 2:", n)
        break

    if n not in last:
        last[n] = i
        n = 0
    else:
        d = i - last[n]
        last[n] = i
        n = d

    i += 1
