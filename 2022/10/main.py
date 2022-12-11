import io

with open("./input.txt") as f:
    instructions = [line.strip().split(" ") for line in f.read().strip().splitlines()]

X = 1
cycles = 0
pc = 0
flag = 0

strength = 0
screen = io.StringIO()

while pc < len(instructions):
    cycles += 1
    ins = instructions[pc]

    if (cycles + 20) % 40 == 0:
        strength += cycles * X 

    screenidx = cycles - 1
    if screenidx % 40 == 0:
        screen.write("\n")
    if X - 1 <= screenidx % 40 <= X + 1:
        screen.write("#")
    else:
        screen.write(" ")

    if ins[0] == "noop":
        pc += 1
        continue

    if flag == 0:
        flag += 1
        continue
    elif flag == 1:
        flag = 0
        pc += 1
        X += int(ins[1])

print("Answer 1:", strength)
print("Answer 2:", screen.getvalue())
