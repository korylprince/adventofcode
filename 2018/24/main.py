import re

groupRegexp = "(\d+) units each with (\d+) hit points(?: \((.*)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)"
immuneRegexp = "immune to ((?:\w+(?:, )?)+)"
weakRegexp = "weak to ((?:\w+(?:, )?)+)"


def get_sub_groups(typestr, lines):
    groups = []
    next(lines) #remove header
    for line in lines:
        matches = re.match(groupRegexp, line).groups()
        g = {
            "type": typestr,
            "units": int(matches[0]),
            "hit_points": int(matches[1]),
            "immunities": [],
            "weaknesses": [],
            "damage": int(matches[3]),
            "damage_type": matches[4],
            "initiative": int(matches[5]),
            "target:": None,
        }
        if matches[2] is not None:
            immunities = re.search(immuneRegexp, matches[2])
            if immunities is not None:
                g["immunities"] = immunities.groups()[0].split(", ")

            weaknesses = re.search(weakRegexp, matches[2])
            if weaknesses is not None:
                g["weaknesses"] = weaknesses.groups()[0].split(", ")

        groups.append(g)
    return groups


def get_groups(file):
    with open(file) as f:
        text = f.read().strip()
    immune = iter([line.strip() for line in text.split("\n\n")[0].strip().splitlines()])
    infection = iter([line.strip() for line in text.split("\n\n")[1].strip().splitlines()])
    return get_sub_groups("immune", immune) + get_sub_groups("infection", infection)


def get_damage(attacker, defender):
    if attacker["damage_type"] in defender["immunities"]:
        return 0
    d = attacker["units"] * attacker["damage"]
    if attacker["damage_type"] in defender["weaknesses"]:
        return d*2
    return d


def fight(groups):
    # selection phase
    groups.sort(key=lambda g: (g["units"] * g["damage"], g["initiative"]), reverse=True)
    unattacked = groups[:]
    for g in groups:
        damage = [(g2, get_damage(g, g2)) for g2 in unattacked if g["type"] != g2["type"]]
        damage = [(g2, d) for g2, d in damage if d > 0]
        if len(damage) == 0:
            g["target"] = None
            continue
        g["target"] = sorted(damage, key=lambda g2: (g2[1], g2[0]["units"] * g2[0]["damage"], g2[0]["initiative"]), reverse=True)[0]
        unattacked.remove(g["target"][0])

    # attack phase
    groups.sort(key=lambda g: g["initiative"], reverse=True)
    for g in groups:
        if g["units"] <= 0 or g["target"] is None:
            continue
        target, d = g["target"]
        target["units"] -= get_damage(g, target) // target["hit_points"]


def battle(groups):
    while True:
        fight(groups)
        groups = [g for g in groups if g["units"] > 0]
        if len([g for g in groups if g["type"] == "immune"]) == 0 or len([g for g in groups if g["type"] == "infection"]) == 0:
            return sum([g["units"] for g in groups])

def battle_boosted(file, boost):
    groups = get_groups(file)
    for g in groups:
        if g["type"] == "immune":
            g["damage"] += boost
    i = 0
    while True:
        i += 1
        if i == 10000:
            return "stalemate", 0

        fight(groups)
        groups = [g for g in groups if g["units"] > 0]
        if len([g for g in groups if g["type"] == "immune"]) == 0 or len([g for g in groups if g["type"] == "infection"]) == 0:
            return groups[0]["type"], sum([g["units"] for g in groups])

def find_boost2(file):
    inc = 16
    boost = 32 
    while True:
        print("Trying Boost: {0}, Increment: {1}".format(boost, inc))
        winning_army, units = battle_boosted(file, boost)
        print("Boost: {0}, Increment: {1}, Result: {2}".format(boost, inc, winning_army))
        if winning_army == "infection":
            boost += inc
            continue
        if winning_army == "stalemate":
            boost += 1
            continue
        if inc == 1:
            return units
        inc //= 2
        boost -= inc

def find_boost(file):
    boost = 1
    while True:
        winning_army, units = battle_boosted(file, boost)
        if winning_army == "immune":
            return units
        boost += 1

groups = get_groups("./input.txt")
print("Answer 1:", battle(groups))
print("Answer 2:", find_boost("./input.txt"))
