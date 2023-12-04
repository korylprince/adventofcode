import re

cards = dict()
with open("./input.txt") as f:
    lines = [line.strip() for line in f.read().strip().splitlines()]
    for line in lines:
        c, left = line.split(":")
        w, m = left.split("|")
        card = int(re.split(r"\s+", c.strip())[-1]) 
        winning = set([int(i) for i in re.split(r"\s+", w.strip())])
        mine = set([int(i) for i in re.split(r"\s+", m.strip())])
        cards[card] = (winning, mine)

total = 0
for id, (winning, mine) in cards.items():
    if (l := len(winning.intersection(mine))) > 0:
        total += 2 ** (l - 1)

print("Answer 1:", total)

wins = {id: 1 for id in cards}
for id, (winning, mine) in cards.items():
    if (l := len(winning.intersection(mine))) < 1:
        continue
    for dx in range(1, l+1):
        if id+dx not in wins:
            continue
        wins[id+dx] += wins[id]

print("Answer 2:", sum(wins.values()))
