import ops

rules = []

with open("./input.txt") as f:
    data = f.read()

for group in data.split("\n\n\n")[0].strip().split("\n\n"):
    before, input, after = group.splitlines()

    rules.append({
        "before": eval(before[len("Before: "):]),
        "op": [int(n) for n in input.split(" ")][0],
        "args": [int(n) for n in input.split(" ")][1:],
        "after": eval(after[len("After: "):]),
        "instructions": set(),
    })

instructions = [i for i in dir(ops) if "_" not in i]
opCodes = {i: set() for i in instructions}

for rule in rules:
    for i in instructions:
        registers = rule["before"][:]
        eval("ops." + i)(registers, *rule["args"])
        if registers == rule["after"]:
            rule["instructions"].add(i)
            opCodes[i].add(rule["op"])

print("Answer 1:", len([r for r in rules if len(r["instructions"]) >= 3]))

def converge(opCodes):
    newOpCodes = {}
    while max([len(codes) for codes in opCodes.values()]) > 0:
        for op in set([op for op in opCodes if len(opCodes[op]) == 1]):
            newOpCodes[op] = list(opCodes[op])[0]
        for op in opCodes:
            opCodes[op] -= set(newOpCodes.values())

    return newOpCodes


opCodes = converge(opCodes)

codeMap = {code: eval("ops." + op) for op, code in opCodes.items()}

instructions = [[int(n) for n in line.strip().split(" ")] for line in data.split("\n\n\n")[1].strip().splitlines()]
registers = [0, 0, 0, 0]
for i in instructions:
    codeMap[i[0]](registers, *i[1:])

print("Answer 2:", registers[0])
