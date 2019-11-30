from collections import deque

with open("./input.txt") as f:
    text = f.read().strip()

ring = deque(text)
total = 0
total2 = 0

for i in range(0, len(ring)):
    if ring[0] == ring[1]:
        total += int(ring[0])
    if ring[0] == ring[len(ring)//2]:
        total2 += int(ring[0])
    ring.rotate(-1)

print("Answer 1:", total)
print("Answer 2:", total2)
