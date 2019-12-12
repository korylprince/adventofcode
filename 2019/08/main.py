with open("./input.txt") as f:
    pixels = [int(p) for p in f.read().strip()]

def chunk(l, num):
    i = 0
    while i != len(l):
        yield l[i:i + num]
        i += num

rows = list(chunk(pixels, 25))
layers = list(chunk(rows, 6))

def flat(layer):
    l = []
    for row in layer:
        for p in row:
            l.append(p)
    return l

minc = min([flat(l).count(0) for l in layers])
layer = [l for l in layers if flat(l).count(0) == minc][0]

print("Answer 1:", flat(layer).count(1) * flat(layer).count(2))

def print_image(layers):
    for y in range(6):
        for x in range(25):
            for l in range(len(layers)):
                if layers[l][y][x] == 0:
                    print(" ", end="")
                    break
                if layers[l][y][x] == 1:
                    print("#", end="")
                    break
        print("")

print("Answer 2:")
print_image(layers)
