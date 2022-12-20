import re
from collections import deque, defaultdict

with open("./input.txt") as f:
    # recipe, ore robot (ore), clay robot (ore), obsidian robot(ore, clay), geode robot(ore, obsidian)
    recipes = [[int(n) for n in re.findall(r"\d+", line)] for line in f.read().strip().splitlines()]

def search(recipe, target):
    # (geode, ore, clay, obsidian, minute), ore robot, clay robot, obsidian robot, geode robot
    q = deque([((0, 0, 0, 0, 0), 1, 0, 0, 0)])
    best = defaultdict(lambda:0)
    seen = set()
    most = 0
    while len(q) > 0:
        state = q.popleft()
        (geode, ore, clay, obsidian, minute), ore_robot, clay_robot, obsidian_robot, geode_robot = state
        if minute == target:
            if geode < most:
                most = geode
            continue

        if geode > best[minute]:
            continue
        elif geode < best[minute]:
            best[minute] = geode


        # geode robot
        if ore >= recipe[4] and obsidian >= recipe[5]:
            newstate = ((geode - geode_robot, ore + ore_robot - recipe[4], clay + clay_robot, obsidian + obsidian_robot - recipe[5], minute + 1),
                          ore_robot , clay_robot, obsidian_robot, geode_robot + 1)
            if newstate not in seen:
                seen.add(newstate)
                q.append(newstate)
        else:
            # just generating
            newstate = ((geode - geode_robot, ore + ore_robot, clay + clay_robot, obsidian + obsidian_robot, minute + 1),
                          ore_robot, clay_robot, obsidian_robot, geode_robot)
            if newstate not in seen:
                seen.add(newstate)
                q.append(newstate)

            # ore robot
            if ore >= recipe[0] and ore_robot < max((recipe[0], recipe[1], recipe[2], recipe[4])):
                newstate = ((geode - geode_robot, ore + ore_robot - recipe[0], clay + clay_robot, obsidian + obsidian_robot, minute + 1),
                              ore_robot + 1, clay_robot, obsidian_robot, geode_robot)
                if newstate not in seen:
                    seen.add(newstate)
                    q.append(newstate)

            # clay robot
            if ore >= recipe[1] and clay_robot < recipe[3]:
                newstate = ((geode - geode_robot, ore + ore_robot - recipe[1], clay + clay_robot, obsidian + obsidian_robot, minute + 1),
                              ore_robot , clay_robot + 1, obsidian_robot, geode_robot)
                if newstate not in seen:
                    seen.add(newstate)
                    q.append(newstate)

            # obsidian robot
            if ore >= recipe[2] and clay >= recipe[3] and obsidian_robot < recipe[5]:
                newstate = ((geode - geode_robot, ore + ore_robot - recipe[2], clay + clay_robot - recipe[3], obsidian + obsidian_robot, minute + 1),
                              ore_robot , clay_robot, obsidian_robot + 1, geode_robot)
                if newstate not in seen:
                    seen.add(newstate)
                    q.append(newstate)

    return -most


print("Answer 1:", sum([(id + 1) * search(recipes[id][1:], 24) for id in range(len(recipes))]))

a = search(recipes[0][1:], 32)
b = search(recipes[1][1:], 32)
c = search(recipes[2][1:], 32)

print("Answer 2:", a*b*c)
