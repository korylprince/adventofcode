import re
from collections import deque

with open("./input.txt") as f:
    players, maxPoints = [int(n) for n in re.findall(r"\d+", f.read())]


def play(players, maxPoints):
    marbles = deque([0])
    scores = {p: 0 for p in range(1, players + 1)}
    player = 1

    for i in range(1, maxPoints + 1):
        if i % 23 == 0:
            scores[player] += i
            marbles.rotate(7)
            scores[player] += marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(i)

        player += 1
        if player > players:
            player = 1

    return max(scores.values())


print("Test High Score:", play(7, 25))
print("1st High Score:", play(players, maxPoints))
print("2nd High Score:", play(players, maxPoints * 100))
