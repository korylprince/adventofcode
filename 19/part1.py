import ops


def get_instructions(file):
    with open(file) as f:
        lines = iter([line.strip() for line in f.read().strip().splitlines()])
        ipr = int(next(lines)[4:])
        inst = []
        for line in lines:
            inst.append((eval("ops." + line.split(" ")[0].strip()), [int(n.strip()) for n in line.split(" ")[1:]]))

    return ipr, inst


def run(ipr, registers, instructions):
    ip = 0
    while ip < len(instructions):
        registers[ipr] = ip
        inst = instructions[ip]
        inst[0](registers, *inst[1])
        ip = registers[ipr] + 1
    return registers[0]    


ipr, instructions = get_instructions("./input.txt")
print("Answer 1:", run(ipr, [0] * 6, instructions))
