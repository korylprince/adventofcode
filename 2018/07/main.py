import re

stepRegexp = "^Step ([A-Z]) must be finished before step ([A-Z]) can begin\.$"

stepInstructions = []

with open("./input.txt") as f:
    for line in [l.strip() for l in f.read().splitlines()]:
        stepInstructions.append(re.match(stepRegexp, line).groups())

steps = set([s[0] for s in stepInstructions] + [s[1] for s in stepInstructions])

requirements = {s: set() for s in steps}

for r, s in stepInstructions:
    requirements[s].add(r)

stepOrder = ""
completedSteps = set()

while True:
    try:
        step = sorted([s for s, r in requirements.items() if len(r.difference(completedSteps)) == 0])[0]
    except IndexError:
        break

    del requirements[step]
    stepOrder += step
    completedSteps.add(step)

print("Step Order:", stepOrder)

# Part 2

requirements = {s: set() for s in steps}

for r, s in stepInstructions:
    requirements[s].add(r)

def work(letter):
    return 61 + ord(letter) - ord("A")

stepOrder = ""
completedSteps = set()
stepWork = {}
workers = 5
i = 0

while True:
    # get current steps
    steps = list(stepWork.keys())
    steps += sorted([s for s, r in requirements.items() if len(r.difference(completedSteps)) == 0 and s not in steps])[:workers-len(steps)]

    # break if done
    if len(steps) == 0:
        break

    for s in steps:
        # add one second
        if s not in stepWork:
            stepWork[s] = 0

        stepWork[s] += 1

        # completed
        if stepWork[s] == work(s):
            stepOrder += s
            completedSteps.add(s)
            del stepWork[s]
            del requirements[s]

    i += 1

print("Total Time:", i)
