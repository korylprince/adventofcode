class ALU:
    def __init__(self, instructions):
        self.r = dict()
        self.instructions = instructions

    def run(self, input):
        self.r = {"w": 0, "x": 0, "y": 0, "z": 0}
        for i in self.instructions:
            if i[0] == "inp":
                self.r[i[1]] = input.pop(0)
                continue

            # parse second argument
            v = None
            if i[2] in self.r:
                v = self.r[i[2]]
            else:
                v = int(i[2])

            if i[0] == "add":
                self.r[i[1]] += v
            elif i[0] == "mul":
                self.r[i[1]] *= v
            elif i[0] == "div":
                if v == 0:
                    raise Exception("divide by zero")
                self.r[i[1]] //= v
            elif i[0] == "mod":
                if self.r[i[1]] < 0 or v <= 0:
                    raise Exception("invalid modulus")
                self.r[i[1]] %= v
            elif i[0] == "eql":
                self.r[i[1]] = 1 if self.r[i[1]] == v else 0

        return self.r["z"]

with open("./input.txt") as f:
    instructions = [i.strip().split(" ") for i in f.read().strip().splitlines()]

alu = ALU(instructions)

a = [
    11111111111111,
    22222222222222,
    33333333333333,
    44444444444444,
    55555555555555,
    66666666666666,
    77777777777777,
    88888888888888,
    99999999999999,
]

for n in range(1111, 10000):
    r = alu.run([int(i) for i in f"{n:1>14}"])
    print(n, r)
    if r == 0:
        break
