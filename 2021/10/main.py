from collections import deque
from statistics import median

class CorruptedException(Exception):
    pass
class IncompleteException(Exception):
    pass

with open("./input.txt") as f:
    chains = [row.strip() for row in f.read().strip().splitlines()]

brackets = {
    "{": "}",
    "(": ")",
    "[": "]",
    "<": ">",
}

def parse(chain):
    stack = deque([chain[0]])
    idx = 1
    while idx < len(chain):
        if (s := chain[idx]) == brackets[stack[-1]]:
            stack.pop()
            if len(stack) == 0 and idx == len(chain) - 1:
                return
        elif s in brackets:
            stack.append(s)
        else:
            raise CorruptedException(s)
        idx += 1
    raise IncompleteException(reversed(stack))

scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

score = 0
score2 = []
for c in chains:
    try:
        parse(c)

    except IncompleteException as e:
        completion = e.args[0]
        s = 0
        for b in completion:
            s *= 5
            s += scores[b]
        score2.append(s)

    except CorruptedException as e:
        score += scores[str(e)]

print("Answer 1:", score)
print("Answer 2:", median(score2))
