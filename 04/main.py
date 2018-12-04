import re
import statistics

dateRegexp = "^\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})"
guardRegexp = "Guard #(\d+)"

sleepMap = {}

with open("./input.txt") as f:
    id = ""
    asleep = 0
    awake = 0
    for line in sorted([x.strip() for x in f.read().splitlines()]):
        if "Guard" in line:
            id = int(re.search(guardRegexp, line).groups()[0])
        if "asleep" in line:
            asleep = int(re.match(dateRegexp, line).groups()[0])
        if "wakes" in line:
            awake = int(re.match(dateRegexp, line).groups()[0])
            if id not in sleepMap:
                sleepMap[id] = []
            sleepMap[id].append((asleep, awake))

sleepSums = {}

for id, sleeps in sleepMap.items():
    sleepSums[id] = sum([s[1] - s[0] for s in sleeps])

maxID = [id for id in sleepSums if sleepSums[id] == max(sleepSums.values())][0]

print("Sleepiest Guard:", maxID)

minutes = sum([list(range(s[0], s[1])) for s in sleepMap[maxID]], [])

maxMinute = statistics.mode(minutes)

print("Sleepiest Minute:", maxMinute)
print("Answer 1:", maxID * maxMinute)

minutesMap = {id: sum([list(range(s[0], s[1])) for s in sleeps], []) for id, sleeps in sleepMap.items()}

minutesModeMap = {}

for id, minutes in minutesMap.items():
    try:
        mode = statistics.mode(minutes)
        minutesModeMap[id] = (mode, minutes.count(mode))
    except:
        pass

maxID, maxMinute = [(id, res[0]) for id, res in minutesModeMap.items() if res[1] == max([r[1] for r in minutesModeMap.values()])][0]

print("Sleepiest Guard:", maxID)
print("Sleepiest Minute:", maxMinute)
print("Answer 2:", maxID * maxMinute)
