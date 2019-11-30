import re
from collections import defaultdict

insRegexp = "(?P<reg>[a-z]+) (?P<mod>(inc|dec)) (?P<amount>\-?\d+) if (?P<creg>[a-z]+) (?P<cop>[!<>=]+) (?P<cam>\-?\d+)"

registers = defaultdict(lambda:0)

with open("./input.txt") as f:
    insRe = [re.match(insRegexp, line.strip()).groupdict() for line in f.read().strip().splitlines()]

maxes = []

for ins in insRe:
    if eval("registers['{}'] {} {}".format(ins["creg"], ins["cop"], ins["cam"])):
        mod = 1 if ins["mod"] == "inc" else -1
        registers[ins["reg"]] += mod * int(ins["amount"])
    maxes.append(max(registers.values()))

print("Answer 1:", max(registers.values()))
print("Answer 2:", max(maxes))
