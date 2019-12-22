from collections import deque
import re

def stack(cards):
    return list(reversed(cards))

def cut(cards, n):
    if n > 0:
        return cards[n:] + cards[:n]
    return cards[len(cards) + n:] + cards[:len(cards) + n]

def deal(cards, n):
    c = deque([0] * len(cards))
    c[0] = cards[0]
    for i in range(1, len(cards)):
        c.rotate(-n)
        c[0] = cards[i]

    c.rotate(n*(len(cards) - 1))

    return list(c)

cards = list(range(10007))

with open("./input.txt") as f:
    for line in f.read().strip().splitlines():
        if "stack" in line:
            cards = stack(cards)
        elif "cut" in line:
            n = int(re.search("-?\d+", line).group())
            cards = cut(cards, n)
        elif "increment" in line:
            n = int(re.search("\d+", line).group())
            cards = deal(cards, n)


print("Answer 1:", cards.index(2019))

# here be dragons...
# See here for explanation: https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/

pos = 2020
cards_len = 119315717514047
times = 101741582076661

offset = 0
increment = 1

with open("./input.txt") as f:
    for line in f.read().strip().splitlines():
        if "stack" in line:
            increment *= -1
            offset += increment
            increment %= cards_len
            offset %= cards_len
        elif "cut" in line:
            n = int(re.search("-?\d+", line).group())
            offset += increment * n
            offset %= cards_len
        elif "increment" in line:
            n = int(re.search("\d+", line).group())
            # magic because modinv of prime is a**(p-2); thanks reddit
            increment *= pow(n, cards_len-2, cards_len)
            increment %= cards_len

total_increment = pow(increment, times, cards_len)
# geometric series
total_offset = offset * (1 - total_increment) * pow(1 - increment, cards_len-2, cards_len)

print("Answer 2:", (total_offset + total_increment * pos) % cards_len)
