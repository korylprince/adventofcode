fish = dict(zip(range(0,9), [0]*9))
with open("./input.txt") as f:
    for f in [int(n) for n in f.read().strip().split(",")]:
        fish[f] += 1

d = 0
while d != 80:
    zero = fish[0]
    for i in range(0, 8):
        fish[i] = fish[i+1]
    fish[8] = zero
    fish[6] += zero
    d += 1

print("Answer 1:", sum(fish.values()))

while d != 256:
    zero = fish[0]
    for i in range(0, 8):
        fish[i] = fish[i+1]
    fish[8] = zero
    fish[6] += zero
    d += 1

print("Answer 2:", sum(fish.values()))
