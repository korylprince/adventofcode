from collections import Counter

with open("./input.txt") as f:
    lines = f.read().strip().splitlines()
    hands = [(line.split(" ")[0].strip(), int(line.split(" ")[1].strip())) for line in lines]

def classify(cards):
    c = Counter(cards)
    if len(c) == 1:
        return 6 # five of a kind
    if 4 in (vals := list(c.values())):
        return 5 # four of a kind
    if 3 in vals and 2 in vals:
        return 4 # full house
    if 3 in vals:
        return 3 # 3 of a kind
    if vals.count(2) == 2:
        return 2 # two pair
    if 2 in vals:
        return 1 # one pair
    return 0 # high card

value_map = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
def value(c):
    if (v := value_map.get(c, None)) is not None:
        return v
    return int(c)

hands.sort(key=lambda h: (classify(h[0]), tuple(value(c) for c in h[0])))
print("Answer 1:", sum([(idx+1) * bid for idx, (hand, bid) in enumerate(hands)]))

value_map["J"] = 1
possibilities = ("A", "K", "Q", "T") + tuple(str(i) for i in range(2, 10))

def choices(cards):
    if "J" not in cards:
        return [cards]
    return sum([choices(cards.replace("J", p, 1)) for p in possibilities], [])

def classify_with_joker(cards):
    m = 0
    for c in choices(cards):
        if (cls := classify(c)) == 6:
            return 6
        elif cls > m:
            m = cls
    return m

hands.sort(key=lambda h: (classify_with_joker(h[0]), tuple(value(c) for c in h[0])))
print("Answer 2:", sum([(idx+1) * bid for idx, (hand, bid) in enumerate(hands)]))
