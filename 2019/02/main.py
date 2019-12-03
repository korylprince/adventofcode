def get_codes():
    with open("./input.txt") as f:
        return [int(i.strip()) for i in f.read().strip().split(",")]

def run(a1, b1):
    codes = get_codes()
    codes[1] = a1
    codes[2] = b1

    idx = 0
    while True:
        code = codes[idx]
        if code == 99:
            break
        if code == 1:
            a, b, c = codes[idx+1], codes[idx+2], codes[idx+3]
            codes[c] = codes[a] + codes[b]
        if code == 2:
            a, b, c = codes[idx+1], codes[idx+2], codes[idx+3]
            codes[c] = codes[a] * codes[b]

        idx += 4
    return codes[0]

print("Answer 1:", run(12, 2))

def run_target(t):
    for x in range(99):
        for y in range(99):
            if run(x, y) == t:
                return (x, y)

noun, verb = run_target(19690720)

print("Answer 2:", (100 * noun) + verb)
