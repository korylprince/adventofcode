with open("./input.txt") as f:
    ins = f.read().strip().split(",")

def HASH(s):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256
    return v

print("Answer 1:", sum(HASH(i) for i in ins))

boxes = {idx: [] for idx in range(256)}

for i in ins:
    if "-" in i:
        box = HASH(i[:-1])
        for idx, (label, focal) in enumerate(boxes[box]):
            if label == i[:-1]:
                boxes[box].remove((label, focal))
                break
    else:
        newlabel, newfocal = i.split("=")
        box = HASH(newlabel)
        replaced = False
        for idx, (label, focal) in enumerate(boxes[box]):
            if newlabel == label:
                boxes[box][idx] = (newlabel, int(newfocal))
                replaced = True
                break
        if not replaced:
            boxes[box].append((newlabel, int(newfocal)))

total = 0
for box, lenses in boxes.items():
    for slot, (_, focal) in enumerate(lenses):
        total += (box + 1) * (slot + 1) * focal 

print("Answer 2:", total)
