with open("./input.txt") as f:
    inputText = f.read().strip()

def reduce(text):
    newText = []

    for l in text:
        if len(newText) > 0 and l.lower() == newText[-1].lower() and l != newText[-1]:
            del newText[-1]
        else:
            newText.append(l)

    return "".join(newText)

text = reduce(inputText)

print("Answer 1:", len(text))

letters = sorted(list(set([l.lower() for l in inputText])))

lengthMap = {}

for l in letters:
    lengthMap[l] = len(reduce([x for x in inputText if x != l and x != l.upper()]))
    print("{0}: {1}".format(l, lengthMap[l]))

print("Best letter to remove:", [l for l in letters if lengthMap[l] == min(lengthMap.values())][0])
print("Answer 2:", min(lengthMap.values()))
