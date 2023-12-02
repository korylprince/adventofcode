with open("./input.txt") as f:
    vals = [line.strip() for line in f.read().strip().splitlines()]
    digits = [[d for d in v if d.isdigit()] for v in vals]

print("Answer 1:", sum([int(d[0] + d[-1]) for d in digits]))

nums = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

def digits(s):
    d = []
    for idx in range(len(s)):
        if s[idx].isdigit():
            d.append(s[idx])
            continue
        for num in nums:
            if idx + len(num) > len(s):
                continue
            if s[idx:idx+len(num)] == num:
                d.append(str(nums.index(num)+1))
    return d

digits2 = [digits(v) for v in vals]
print("Answer 2:", sum([int(d[0] + d[-1]) for d in digits2]))
