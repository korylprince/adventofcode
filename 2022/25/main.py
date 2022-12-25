def parse(s):
    n = 0
    for idx, c in enumerate(reversed(s)):
        if c.isdigit():
            n += int(c) * (5**idx)
        elif c == "-":
            n += -1 * (5**idx)
        elif c == "=":
            n += -2 * (5**idx)
    return n

def tob5(n):
    digits = []
    while n:
        digits.append(int(n % 5))
        n //= 5
    return digits[::-1]

mapping = {3: "=", 4: "-", 5: 0}

def marshal(n):
    digits = tob5(n)
    for idx in range(len(digits)-1, -1, -1):
        if digits[idx] in (3, 4, 5):
            digits[idx] = mapping[digits[idx]]
            if idx == 0:
                digits = [1] + digits
            else:
                digits[idx-1] += 1

    return "".join([str(n) for n in digits])


with open("./input.txt") as f:
    total = sum([parse(s.strip()) for s in f.read().strip().splitlines()])

print("Answer 1:", marshal(total))
