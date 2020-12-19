import re
from collections import defaultdict

with open("./input.txt") as f:
    sections = f.read().strip().split("\n\n")
    rules = {int(n): tuple(tuple(int(i.strip()) if i.strip().isnumeric() else i[1:2] for i in g.strip().split(" ")) for g in r.strip().split("|")) for n, r in [line.strip().split(": ") for line in sections[0].strip().splitlines()]}
    tests = [line.strip() for line in sections[1].strip().splitlines()]

maxTest = max([len(t) for t in tests])

def buildRegexp(rules, root=0):
    vals = []
    for r in rules[root]:
        if isinstance(r[0], str):
            return r[0]
        vals.append("".join(buildRegexp(rules, i) for i in r))
    ret = "(?:" + "|".join(vals) + ")" if len(vals) > 1 else vals[0]
    if root == 0:
        return "^" + ret + "$"
    return ret

regexp = buildRegexp(rules)

print("Answer 1:", len([None for test in tests if re.match(regexp, test) is not None]))

reg31 = buildRegexp(rules, 31)
reg42 = buildRegexp(rules, 42)
m = min((max([len(re.findall(reg31, t)) for t in tests]), max([len(re.findall(reg42, t)) for t in tests])))

def buildRegexpTricky(rules, root=0):
    vals = []
    for r in rules[root]:
        if isinstance(r[0], str):
            return r[0]
        vals.append("".join(buildRegexpTricky(rules, i) for i in r))
    ret = "(?:" + "|".join(vals) + ")" if len(vals) > 1 else vals[0]
    if root == 0:
        return "^" + ret + "$"
    elif root == 8:
        return ret + "+"
    elif root == 11:
        vals = []
        for i in range(1, m + 1):
            vals.append(reg42 + f"{{{i}}}" + reg31 + f"{{{i}}}")
        ret = "(?:" + "|".join(vals) + ")"
    return ret

regexp = buildRegexpTricky(rules)

print("Answer 2:", len([None for test in tests if re.match(regexp, test) is not None]))
