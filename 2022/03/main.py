from itertools import groupby

def p(l):
    if l.upper() == l:
        return ord(l) - ord("A") + 27
    return ord(l) - ord("a") + 1

with open("./input.txt") as f:
    rucks = [line.strip() for line in f.read().strip().splitlines()]
    rucks = [(set(line[:len(line)//2]), set(line[len(line)//2:])) for line in rucks]

print("Answer 1:", sum([sum(map(p, r[0].intersection(r[1]))) for r in rucks]))

score = 0
for k, v in groupby(rucks, lambda r: rucks.index(r)//3): # chunk in 3s
    score += p(list(set.intersection(*[r[0].union(r[1]) for r in v]))[0])

print("Answer 2:", score)
