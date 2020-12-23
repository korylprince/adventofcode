import networkx as nx

with open("./input.txt") as f:
    cups = [int(n) for n in f.read().strip()]

llist = {n1: n2 for n1, n2 in nx.utils.pairwise(cups)}
llist[cups[-1]] = cups[0]


def run(cur, llist, iterations):
    mcups = max(cups)

    for l in range(iterations):
        pickup = (llist[cur], llist[llist[cur]], llist[llist[llist[cur]]])
        llist[cur] = llist[pickup[2]]

        dest = cur - 1
        while dest in pickup or dest == 0:
            dest = dest - 1
            if dest <= 0:
                dest = mcups

        llist[pickup[2]] = llist[dest]
        llist[dest] = pickup[0]
        cur = llist[cur]

run(cups[0], llist, 100)
print("Answer 1: ", end="")
cur = 1
while llist[cur] != 1:
    print(llist[cur], end="")
    cur = llist[cur]
print()
    

with open("./input.txt") as f:
    cups = [int(n) for n in f.read().strip()]

cups.extend(range(10, 1_000_001))

llist = {n1: n2 for n1, n2 in nx.utils.pairwise(cups)}
llist[cups[-1]] = cups[0]
run(cups[0], llist, 10_000_000)

print("Answer 2:", llist[1] * llist[llist[1]])
