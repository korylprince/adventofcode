import numpy as np

class Tile:
    def __init__(self, id, tile):
        self.id = id
        self.tile = tile
        self.coords = None
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def __repr__(self):
        return f"<Tile ({self.id})>"

    @property
    def is_corner(self):
        return [self.north, self.east, self.south, self.west].count(None) == 2

    def ccw(self):
        if self.coords is not None:
            raise Exception("Can't rotate positioned tile")
        self.tile = np.rot90(self.tile)

    def flip(self):
        if self.coords is not None:
            raise Exception("Can't flip positioned tile")
        self.tile = np.flip(self.tile, 0)

    def image(self):
        return self.tile[1:-1,1:-1]

    def _match(self, other):
        if self.north is None and other.south is None and np.array_equal(self.tile[0,:], other.tile[-1,:]):
            self.north = other
            other.south = self
            other.coords = (self.coords[0], self.coords[1]+1)
            return True
        elif self.east is None and other.west is None and np.array_equal(self.tile[:,-1], other.tile[:,0]):
            self.east = other
            other.west = self
            other.coords = (self.coords[0]+1, self.coords[1])
            return True
        elif self.south is None and other.north is None and np.array_equal(self.tile[-1,:], other.tile[0,:]):
            self.south = other
            other.north = self
            other.coords = (self.coords[0], self.coords[1]-1)
            return True
        elif self.west is None and other.east is None and np.array_equal(self.tile[:,0], other.tile[:,-1]):
            self.west = other
            other.east = self
            other.coords = (self.coords[0]-1, self.coords[1])
            return True
        return False

    def match(self, other):
        if other.coords is not None:
            return self._match(other)
        f = 0
        while other.coords is None:
            if f == 2:
                return False
            r = 0
            while other.coords is None:
                if r == 4:
                    break
                if self._match(other):
                    return True
                other.ccw()
                r += 1
            other.flip()
            f += 1

with open("./input.txt") as f:
    groups = f.read().strip().split("\n\n")
    tiles = [Tile(int(lines[0][5:-1]), np.array([[c for c in l] for l in lines[1:]])) for lines in [g.strip().splitlines() for g in groups]]

tiles[0].coords = (0, 0)
seen = set((tiles[0].id,))
check = [tiles[0]]
while len(check) > 0:
    c = check.pop()
    seen.add(c.id)
    for t in [t for t in tiles if t.id not in seen]:
        if c.match(t):
            check.append(t)

print("Answer 1:", np.product([t.id for t in tiles if t.is_corner]))

coords = {t.coords: t.image() for t in tiles}
rect = (
    min([c[0] for c in coords.keys()]),
    max([c[0] for c in coords.keys()]),
    min([c[1] for c in coords.keys()]),
    max([c[1] for c in coords.keys()]),
)

G = np.empty([tiles[0].image().shape[1]*(rect[1]-rect[0]+1), 0])
for x in range(rect[0], rect[1]+1):
    a = np.empty([0, tiles[0].image().shape[0]])
    for y in range(rect[2], rect[3]+1):
        a = np.append(coords[(x, y)], a, 0)
    G = np.append(G, a, 1)


monster_str = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

monster = set()
for y, line in enumerate(monster_str.splitlines()):
    for x, c in enumerate(line):
        if c == "#" and (x, 1-y) != (0, 0):
            monster.add((x, 1-y))


def printG(G):
    for y in range(G.shape[1]):
        line = []
        for x in range(G.shape[0]):
            line.append(G[y,x])
        print("".join(line))

def solve(G, monster):
    f = 0
    while True:
        if f == 2:
            raise Exception("Unable to find monster")
        r = 0
        while True:
            if r == 4:
                break

            monsters = set()
            hashes = {(x, y) for x in range(G.shape[0]) for y in range(G.shape[1]) if G[x,y] == "#"}
            for x, y in hashes:
                found = True
                for dx, dy in monster:
                    if (x+dx,y+dy) not in hashes:
                        found = False
                        break
                if found:
                    monsters.update({(x+dx, y+dy) for dx, dy in monster}, [(x, y)])

            if len(monsters) > 0:
                return len(hashes) - len(monsters)

            G = np.rot90(G)
            r += 1
        G = np.flip(G, 0)
        f += 1

print("Answer 2:", solve(G, monster))
