with open("./input.txt") as f:
    text = f.read().strip()

pos = 0
total = 0
score = 0
garbage = 0
garbage_total = 0

while pos < len(text):
    char = text[pos]
    if char == "!":
        pos += 2
        continue
    elif char == ">":
        garbage = False
    elif garbage:
        garbage_total += 1
    elif char == "<":
        garbage = True
    elif char == "{":
        score += 1
    elif char == "}":
        total += score
        score -= 1

    pos += 1

print("Answer 1:", total)
print("Answer 2:", garbage_total)
