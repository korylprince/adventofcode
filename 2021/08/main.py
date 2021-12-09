ALL = {*"abcdefg"}

segments = {
    0: {*"abcefg"}, # 6
    1: {*"cf"},     # 2*
    2: {*"acdeg"},  # 5
    3: {*"acdfg"},  # 5
    4: {*"bcdf"},   # 4*
    5: {*"abdfg"},  # 5
    6: {*"abdefg"}, # 6
    7: {*"acf"},    # 3*
    8: {*"abcdefg"},# 7*
    9: {*"abcdfg"}, # 6
}

with open("./input.txt") as f:
    codes = [(lambda f, s: ([{*c} for c in f.split(" ")], [{*c} for c in s.split(" ")]))(*row.split(" | ")) for row in f.read().strip().splitlines()]

count = 0
for c in codes:
    for o in c[1]:
        if len(o) in (2, 4, 3, 7):
            count += 1

print("Answer 1:", count)


def solve(unique, output):
    nums = {
        # unique number of segments
        1: [u for u in unique if len(u) == 2][0],
        4: [u for u in unique if len(u) == 4][0],
        7: [u for u in unique if len(u) == 3][0],
        8: [u for u in unique if len(u) == 7][0],
    }

    solved = {
        "a": min(nums[7].difference(nums[1])),
    }

    nums[9] = [u for u in unique if len(u) == 6 and len(u.difference(nums[4]).difference({solved["a"]})) == 1][0]
    solved["e"] = min(ALL.difference(nums[9]))
    solved["g"] = min(nums[9].difference(nums[4]).difference({solved["a"]}))

    nums[0] = [u for u in unique if len(u) == 6 and len(u.difference(nums[7]).difference({solved["e"]}).difference({solved["g"]})) == 1][0]
    solved["d"] = min(ALL.difference(nums[0]))
    solved["b"] = min(nums[0].difference(nums[7]).difference({solved["e"]}).difference({solved["g"]}))

    nums[6] = [u for u in unique if len(u) == 6 and u not in nums.values()][0]
    solved["c"] = min(ALL.difference(nums[6]))
    solved["f"] = min(nums[1].difference({solved["c"]}))

    translate = {v: k for k, v in solved.items()}

    nums = [[n for n, s in segments.items() if s == {translate[n] for n in o}][0] for o in output]
    return int("".join([str(n) for n in nums]))

total = 0
i = 0
for unique, output in codes:
    total += solve(unique, output)
    i += 1

print("Answer 2:", total)
