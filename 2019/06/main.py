from collections import deque

import networkx as nx

with open("./input.txt") as f:
    graph = nx.DiGraph([line.strip().split(")") for line in f.read().strip().splitlines()])

def ans1(graph, root):
    queue = deque([(root, 0)])
    total_depth = 0

    while True:
        if len(queue) == 0:
            break
        head, depth = queue.popleft()
        total_depth += depth
        queue.extend([(c, depth + 1) for c in graph.neighbors(head)])
    return total_depth

def ans2(graph, root, target):
    seen = set(root)
    queue = deque([(root, -1)])

    while True:
        head, depth = queue.popleft()
        children = [n for n in nx.all_neighbors(graph, head) if n not in seen]
        if target in children:
            return depth
        seen.update(children)
        queue.extend([(c, depth + 1) for c in children])


print("Answer 1:", ans1(graph, "COM"))
print("Answer 2:", ans2(graph, "YOU", "SAN"))
