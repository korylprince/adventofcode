import re

mul_re = r"mul\((\d+),(\d+)\)"

with open("./input.txt") as f:
    mults = re.findall(mul_re, f.read().strip())

print("Answer 1:", sum([int(m[0]) * int(m[1]) for m in mults]))

all_re = r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))"

with open("./input.txt") as f:
    ins = re.findall(all_re, f.read().strip())

do = True
total = 0
for i in ins:
    if i[0] == "do()":
        do = True
    elif i[0] == "don't()":
        do = False
    elif "mul" in i[0] and do:
        total += int(i[1]) * int(i[2])

print("Answer 2:", total)
