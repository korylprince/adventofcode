import math

with open("./input.txt") as f:
    nums = [line.strip() for line in f.read().strip().splitlines()]

def red(n):
    # check for explodes
    level = 0
    idx = 0
    while idx < len(n):
        if (c := n[idx]) == "[":
            level += 1
            if level > 4 and isinstance(n[idx+1], int) and isinstance(n[idx+3], int):
                # explode left
                i = idx - 1
                while i >= 0:
                    if isinstance(n[i], int):
                        n[i] += n[idx+1]
                        break
                    i -= 1
                # explode right
                i = idx + 4
                while i < len(n):
                    if isinstance(n[i], int):
                        n[i] += n[idx+3]
                        break
                    i += 1
                # replace with 0
                n = n[:idx] + [0] + n[idx+5:]
                return n, True
        elif c == "]":
            level -= 1
        idx += 1

    # check for splits
    idx = 0
    while idx < len(n):
        if isinstance((c := n[idx]), int) and c >= 10:
            n = n[:idx] + ["[",math.floor(c/2),",",math.ceil(c/2),"]"] + n[idx+1:]
            return n, True
        idx += 1

    return n, False

def reduce(n):
    chars = [int(c) if c.isdigit() else c for c in n]
    changed = True
    while changed:
        chars, changed = red(chars)
    return "".join([str(c) for c in chars])

def magnitude(n):
    if isinstance(n, int):
        return n
    return 3 * magnitude(n[0]) + 2 * magnitude(n[1])

total = nums[0]
for num in nums[1:]:
    total = reduce(f"[{total},{num}]")

print("Answer 1:", magnitude(eval(total)))

best = 0
for n1 in nums:
    for n2 in nums:
        if n1 == n2:
            continue
        m = magnitude(eval(reduce(f"[{n1},{n2}]")))
        if m > best:
            best = m

print("Answer 2:", best)
