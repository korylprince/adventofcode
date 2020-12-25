subject = 7
modulo = 20201227

with open("./input.txt") as f:
    keys = [int(line.strip()) for line in f.read().strip().splitlines()]

def find(key):
    i = 1
    while True:
        if pow(subject, i, modulo)  == key:
            return i
        i += 1

loop1 = find(keys[0])
print("Answer 1:", pow(keys[1], loop1, modulo))
