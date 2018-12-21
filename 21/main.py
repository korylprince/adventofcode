import sys
import ops


def get_instructions(file):
    with open(file) as f:
        lines = iter([line.strip() for line in f.read().strip().splitlines()])
        ipr = int(next(lines)[4:])
        inst = []
        for line in lines:
            inst.append((eval("ops." + line.split(" ")[0].strip()), [int(n.strip()) for n in line.split(" ")[1:]]))

    return ipr, inst


def run1(ipr, registers, instructions):
    ip = 0
    while ip < len(instructions):
        registers[ipr] = ip
        if ip == 28:
            registers[0] = registers[1]
        inst = instructions[ip]
        inst[0](registers, *inst[1])
        ip = registers[ipr] + 1
    return registers[0]


def naive(ipr, registers, instructions):
    ip = 0
    valid = set()
    last = 0
    i = 0
    while ip < len(instructions):
        registers[ipr] = ip
        if ip == 28:
            i += 1
            sys.stdout.write(str(i) + "\r")
            if registers[1] in valid:
                return last
            valid.add(registers[1])
            last = registers[1]
        inst = instructions[ip]
        inst[0](registers, *inst[1])
        ip = registers[ipr] + 1
    return registers[0]

def optimized():
    inc = 0
    seen = set()
    last = 0
    while True:
        mod = inc | 65536
        inc = 8586263

        while True:
            inc += mod & 255
            inc &= 16777215
            inc *= 65899
            inc &= 16777215

            if 256 > mod:
                if inc in seen:
                    return last
                seen.add(inc)
                last = inc
                break

            mod //= 256


ipr, instructions = get_instructions("./input.txt")
print("Answer 1:", run1(ipr, [0] * 6, instructions))
print("Answer 2:", optimized())
