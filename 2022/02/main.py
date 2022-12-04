ROCK = "r"
PAPER = "p"
SCISSORS = "s"
LOSE = "X"
DRAW = "Y"
WIN = "Z"

scores = {ROCK: 1, PAPER: 2, SCISSORS: 3}
sym = {"A": ROCK, "B": PAPER, "C": SCISSORS, "X": ROCK, "Y": PAPER, "Z": SCISSORS}
win = {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}
lose = {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER}

def game(them, me):
    score = scores[me]
    if them == me:
        score += 3
    elif win[them] == me:
        score += 6

    return score

with open("./input.txt") as f:
    rounds = [line.strip().split(" ") for line in f.read().strip().splitlines()]

games = [game(sym[r[0]], sym[r[1]]) for r in rounds]

print("Answer 1:", sum(games))

def strat(them, me):
    if me == LOSE:
        return game(them, lose[them])
    if me == DRAW:
        return game(them, them)
    return  game(them, win[them])

games = [strat(sym[r[0]], r[1]) for r in rounds]

print("Answer 2:", sum(games))
