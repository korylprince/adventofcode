import re
import math
from collections import defaultdict

class Reaction:
    regexp = "(\d+) ([A-Z]+)"

    def __init__(self, text):
        self.text = text
        ing, r = text.split(" => ")
        ing = [re.match(self.regexp, i).groups() for i in ing.split(", ")]
        self.ingredients = {i[1]: int(i[0]) for i in ing}
        r = re.match(self.regexp, r).groups()
        self.result = (r[1], int(r[0]))
        self.children = []
        self.parents = []

    def __repr__(self):
        return self.text


with open("./input.txt") as f:
    reactions = [Reaction(line.strip()) for line in f.read().strip().splitlines()]

reactionMap = {r.result[0]: r for r in reactions}

def ore_needed(fuel_count):
    needed = defaultdict(lambda:0, {"FUEL": fuel_count})

    while len([k for k, v in needed.items() if v > 0 and k != "ORE"]) > 0:
        _needed = defaultdict(lambda:0)
        for n, needed_amount in needed.items():
            if n == "ORE" or needed_amount < 0:
                _needed[n] += needed_amount
                continue

            reaction = reactionMap[n]
            reaction_amount = reaction.result[1]
            reaction_count = math.ceil(needed_amount / reaction_amount)

            extra = reaction_amount * reaction_count - needed_amount
            if extra > 0:
                _needed[n] -= extra

            for i, ingredient_amount in reaction.ingredients.items():
                _needed[i] += reaction_count * ingredient_amount

        needed = _needed

    return needed["ORE"]

fuel_ore = ore_needed(1)
print("Answer 1:", ore_needed(1))

target = 1_000_000_000_000
bottom = math.ceil(target / fuel_ore)
top = bottom * 2
while bottom <= top:
    mid = math.floor((top + bottom) / 2)
    if ore_needed(mid) > target:
        top = mid - 1
    else:
        bottom = mid + 1

print("Answer 2:", top)
