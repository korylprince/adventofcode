with open("./input.txt") as f:
    text = f.read().strip()

idx = 4
found = False
while True:
    if not found and len(set(text[idx-4:idx])) == 4:
        print("Answer 1:", idx)
        found = True
    if len(set(text[idx-14:idx])) == 14:
        print("Answer 2:", idx)
        break
    idx += 1
