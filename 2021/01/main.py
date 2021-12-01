def pairwise(items):
   iterator = iter(items)
   a = next(iterator)
   for b in iterator:
       yield a, b
       a = b

def triplewise(items):
   iterator = iter(items)
   a = next(iterator)
   b = next(iterator)
   for c in iterator:
       yield a, b, c
       a = b
       b = c

with open("./input.txt") as f:
    inp = [int(row.strip()) for row in f.read().strip().splitlines()]

count = 0
for a, b in pairwise(inp):
    if b > a:
        count += 1
print("Answer 1:", count)

count = 0
for a, b in pairwise(triplewise(inp)):
    if sum(b) > sum(a):
        count += 1
print("Answer 2:", count)
