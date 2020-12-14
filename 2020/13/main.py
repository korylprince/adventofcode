with open("./input.txt") as f:
    lines = f.read().strip().splitlines()
    time = int(lines[0].strip())
    buses = [int(b.strip()) if b != "x" else "x" for b in lines[1].strip().split(",")]


mint = None
minb = None

for b in buses:
    if b == "x":
        continue
    first = b * ((time // b) + 1)
    if mint is None or first < mint:
        mint = first
        minb = b


print("Answer 1:", (mint-time) * minb)

guess = 0
factor = 1

for i, b in [(i, b) for i, b in enumerate(buses) if b != "x"]:
    while (guess + i) % b != 0:
        guess += factor
    factor *= b

print("Answer 2:", guess)
