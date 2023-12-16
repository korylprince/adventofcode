from functools import cache

records = []

with open("./input.txt") as f:
    for line in f.read().strip().splitlines():
        chars, groups = line.split(" ")
        records.append((chars, tuple(int(i) for i in groups.strip().split(","))))

@cache
def solve(chars, groups):
    if len(chars) == 0:
        if len(groups) == 0:
            return 1
        return 0
    if len(groups) == 0:
        for c in chars:
            if c == "#":
                return 0
        return 1
    if chars[0] == ".":
        return solve(chars[1:], groups)
    if chars[0] == "?":
        return solve("." + chars[1:], groups) + solve("#" + chars[1:], groups)
    if chars[0] == "#":
        if len(chars) < groups[0]:
            return 0
        for c in chars[:groups[0]]:
            if c == ".":
                return 0
        if len(chars) == groups[0]:
            return solve(chars[groups[0]:], groups[1:])
        if chars[groups[0]] == "#":
            return 0
        return solve(chars[groups[0]+1:], groups[1:])

print("Answer 1:", sum(solve(*record) for record in records))

records = [("?".join((chars,)*5), groups*5) for chars, groups in records]
print("Answer 2:", sum(solve(*record) for record in records))
