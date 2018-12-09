with open("./input.txt") as f:
    license = f.read()

def read_number(input):
    n = ""
    while True:
        try:
            l = next(input)
        except StopIteration:
            return int(n)
        if l != " ":
            n += l
            break

    while True:
        try:
            l = next(input)
        except StopIteration:
            return int(n)
        if l == " ":
            return int(n)
        n += l

def read_node(input):
    childCount = read_number(input)
    metaCount = read_number(input)
    node = {"children": [], "metadata": []}
    for i in range(0, childCount):
        node["children"].append(read_node(input))

    for i in range(0, metaCount):
        node["metadata"].append(read_number(input))

    return node

root = read_node(iter(license))

def count(node):
    c = 0
    c += sum(node["metadata"])
    c += sum([count(n) for n in node["children"]])
    return c

print("Metadata sum:", count(root))

def value(node):
    if len(node["children"]) == 0:
        return sum(node["metadata"])
    v = 0
    for m in node["metadata"]:
        try:
            v += value(node["children"][m-1])
        except IndexError:
            pass
    return v

print("Root Value:", value(root))
