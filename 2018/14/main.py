with open("./input.txt") as f:
    recipeCount = int(f.read())

recipes = [3, 7]
elves = {1: 0, 2: 1}

def bake(recipes, elves):
    sum = 0
    for i, idx in elves.items():
        sum += recipes[idx]
    recipes += [int(n) for n in str(sum)]

    for i, idx in elves.items():
        elves[i] = (idx + 1 + recipes[idx]) % (len(recipes))

def bakeOff(start, count):
    recipes = [3, 7]
    elves = {1: 0, 2: 1}
    while len(recipes) < start + count:
        bake(recipes, elves)

    return "".join([str(n) for n in recipes[start:start + 1 + count]])

def bakeUntil(last):
    recipes = [3, 7]
    elves = {1: 0, 2: 1}
    last = [int(n) for n in last]
    while True:
        bake(recipes, elves)
        if recipes[-len(last):] == last:
            return len(recipes) - len(last)

        elif recipes[-1 - len(last):-1] == last:
            return len(recipes) - len(last) - 1


print("Next 10:", bakeOff(recipeCount, 10))
print("Recipe Count:", bakeUntil(str(recipeCount)))
