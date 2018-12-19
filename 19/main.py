def generate(registers):
    #instructions 17 - 26
    registers[3] = ((registers[3]+ 2)**2 * 19 * 11)
    registers[1] = ((registers[1] + 6) * 22) + 6
    registers[3] = registers[3] + registers[1]
    if registers[0] == 0:
        return registers[3]
    else:
        return generate_more(registers)


def generate_more(registers):
    #instructions 27 - 35
    registers[1] = ((27 * 28) + 29) * 30 * 14 * 32
    registers[3] = registers[3] + registers[1]
    registers[0] = 0
    return registers[3]


def iterate(registers, reset4=True, reset5=True):
    #instructions 1 - 16
    if reset4:
        registers[4] = 1
    if reset5:
        registers[5] = 1
        
    if registers[3] == registers[4] * registers[5]:
        registers[0] += registers[4]

    registers[5] += 1
    if registers[5] <= registers[3]:
        return iterate(registers, False, False)

    registers[4] += 1
    if registers[4] > registers[3]:
        return registers[0]
    return iterate(registers, False, True)


def iterate_optimized(start):
    # simple optimatization
    ret = 0
    first = 1
    second = 1
    while True:
        if start == first * second:
            ret += first

        second += 1
        if second <= start:
            continue

        first += 1
        if first > start:
            return ret
        second = 1


def iterate_really_optimized(start):
    # use maths
    ret = start
    for first in range(1, (start // 2) + 1):
        for second in range(1, (start // first) + 1):
            if first * second == start:
                ret += first
                continue
    return ret

def iterate_understand_optimized(start):
    # it's factors
    ret = start
    for n in range(1, (start // 2) + 1):
        if start % n == 0:
            ret += n
    return ret


starting_value = generate([0, 0, 0, 0, 0, 0])
print("Answer 1:", iterate_understand_optimized(starting_value))

starting_value = generate([1, 0, 0, 0, 0, 0])
print("Answer 2:", iterate_understand_optimized(starting_value))
