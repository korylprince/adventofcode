from functools import cmp_to_key

def parse(text):
    items = []
    num = ""
    idx = 0
    while idx < len(text):
        if text[idx] == "[":
            v, l = parse(text[idx+1:])
            items.append(v)
            idx += l
        elif text[idx].isnumeric():
            num += text[idx]
        elif text[idx] == ",":
            if num != "":
                items.append(int(num))
                num = ""
        elif text[idx] == "]":
            if num != "":
                items.append(int(num))
            return items, idx + 1
        idx += 1
    return items

with open("./input.txt") as f:
    pairs = [[parse(line) for line in group.strip().splitlines()] for group in f.read().strip().split("\n\n")]

def ordered(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif right < left:
            return False
    elif isinstance(left, list) and isinstance(right, list):
        idx = 0
        while idx < len(left) and idx < len(right):
            if (ret := ordered(left[idx], right[idx])) is not None:
                return ret
            else:
                idx += 1
        if len(left) < len(right):
            return True
        elif len(left) > len(right):
            return False
    elif isinstance(left, int):
        return ordered([left], right)
    elif isinstance(right, int):
        return ordered(left, [right])

print("Answer 1:", sum([idx+1 for idx, pair in enumerate(pairs) if ordered(*pair)]))

pairs = sum(pairs, []) + [[[2]], [[6]]]

pairs.sort(key=cmp_to_key(lambda a, b: -1 if ordered(a, b) else 1))
print("Answer 2:", (pairs.index([[2]]) + 1) * (pairs.index([[6]]) + 1))
