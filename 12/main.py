state = []
rules = {}

def pad(s):
    offset = 0
    if s[:4] == "....":
        pass
    elif s[:3] == "...":
        s = "." + s
        offset = -1
    elif s[:2] == "..":
        s = ".." + s
        offset = -2
    elif s[:1] == ".":
        s = "..." + s
        offset = -3
    else:
        s = "...." + s
        offset = -4

    if s[-4:] == "....":
        pass
    elif s[-3:] == "...":
        s = s + "."
    elif s[-2:] == "..":
        s = s + ".."
    elif s[-1:] == ".":
        s = s + "..."
    else:
        s = s + "...."

    return s, offset

with open("./input.txt") as f:
    lines = iter([line.strip() for line in f.read().splitlines()])
    state = next(lines)[len("initial state: "):]
    next(lines)
    for line in lines:
        rules[line[:5]] = line[-1]

def generate(state, generations): 
    state, offset = pad(state)

    for i in range(generations):
        new_state = []

        for k in range(0, len(state)):
            new_state.append(rules.get(
                "".join(state[k-2:k+3]),
                "."
            ))

        state, off = pad("".join(new_state))
        offset += off

    return state, offset

def sum(state, offset):
    sum = 0

    for k in range(0, len(state)):
        if state[k] == "#":
            sum += k + offset

    return sum

print("Sum 1:", sum(*generate(state, 20)))

def cheatsum(state, generations):
    i = 1 
    a = sum(*generate(state, i + 1)) - sum(*generate(state, i))
    b = sum(*generate(state, i + 2)) - sum(*generate(state, i + 1))
    count = 0

    while True:
        if count == 50:
            break
        if a == b:
            count += 1
        else:
            count = 0

        i += 1

        a = sum(*generate(state, i + 1)) - sum(*generate(state, i))
        b = sum(*generate(state, i + 2)) - sum(*generate(state, i + 1))

    print("Sum stablizes to increase of", b, "after", i, "generations")
    return sum(*generate(state, i)) + (generations - i) * b

print("Sum 2:", cheatsum(state, 50000000000))

