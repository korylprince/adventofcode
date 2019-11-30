import itertools

with open("./input.txt") as f:
    passphrases = [[phrase.strip() for phrase in row.strip().split(" ")] for row in f.read().strip().splitlines()]

print("Answer 1:", len([p for p in passphrases if len(p) == len(set(p))]))

passphrases2 = [[set(p) for p in phrase] for phrase in passphrases]

count = 0
for phrase in passphrases2:
    valid = True
    for x, y in itertools.combinations(phrase, 2):
        if x == y:
            valid = False
            break

    if valid:
        count += 1

print("Answer 2:", count)
