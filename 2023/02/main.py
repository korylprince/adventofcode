limits = {"red": 12, "green": 13, "blue": 14}

with open("./input.txt") as f:
    lines = [line.strip() for line in f.read().strip().splitlines()]
    winning = 0
    minwin = 0
    for line in lines:
        id, games = line.split(":")[0].split(" ")[1], line.split(":")[1].split(";")
        possible = True
        maximum = {"red": 0, "green": 0, "blue": 0}
        for game in games:
            dice = game.split(",")
            for die in dice:
                num, color = die.strip().split(" ")
                if limits[color] < int(num):
                    possible = False
                if (n := int(num)) > maximum[color]:
                    maximum[color] = n
        if possible:
            winning += int(id)
        minwin += maximum["red"] * maximum["green"] * maximum["blue"]

print("Answer 1:", winning)
print("Answer 2:", minwin)
