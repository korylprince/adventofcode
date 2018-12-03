import sys

with open("./input.txt") as f:
    numbers = [x.strip() for x in f.read().splitlines()]

signMap = {"+": 1, "-": -1}
sum = 0
for n in numbers:
    sum += signMap[n[0]] * int(n[1:])

print("Answer 1:", sum)

freqs = set()


def loop(freq):
    for n in numbers:
        freq += signMap[n[0]] * int(n[1:])
        if freq in freqs:
            return freq
            sys.exit(0)
        freqs.add(freq)
    return loop(freq)


print("Answer 2:", loop(0))
