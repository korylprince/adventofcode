tests = []

with open("./input.txt") as f:
    for line in f.read().strip().splitlines():
        tests.append((int(line.split(":")[0].strip()), [int(n) for n in line.split(":")[1].strip().split(" ")]))


def run(nums):
    if len(nums) == 2:
        return [nums[0] + nums[1], nums[0] * nums[1]]
    return (run([nums[0] + nums[1]] + nums[2:]) +
            run([nums[0] * nums[1]] + nums[2:]))


print("Answer 1:", sum([t for t, nums in tests if t in run(nums)]))

def concat(a, b):
    return a * (10 ** len(str(b))) + b

def run2(nums):
    if len(nums) == 2:
        return [nums[0] + nums[1], nums[0] * nums[1], concat(nums[0], nums[1])]
    return (run2([nums[0] + nums[1]] + nums[2:]) +
            run2([nums[0] * nums[1]] + nums[2:]) +
            run2([concat(nums[0], nums[1])] + nums[2:]))

print("Answer 2:", sum([t for t, nums in tests if t in run2(nums)]))
