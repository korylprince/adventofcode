import re
from collections import defaultdict, deque
import copy
import queue
import itertools

class Computer:
    MODE_POSITION = 0
    MODE_IMMEDIATE = 1
    MODE_RELATIVE = 2

    _opcodes = {}

    def __init__(self, code_file):
        with open(code_file) as f:
            self._program = [int(code.strip()) for code in f.read().strip().split(",")]
        self._memory = defaultdict(lambda:0)
        self.reset()

    def reset(self):
        self.program = self._program[:]
        self.memory = self._memory.copy()
        self.pc = 0
        self.rel = 0
        self.halted = False
        self.output = None
        self.inputs = deque()

    def get(self, idx, mode=MODE_POSITION):
        if mode == Computer.MODE_IMMEDIATE:
            return idx
        if mode == Computer.MODE_RELATIVE:
            idx += self.rel
        if idx < len(self.program):
            return self.program[idx]
        return self.memory[idx]

    def set(self, idx, val, mode=MODE_POSITION):
        if mode == Computer.MODE_RELATIVE:
            idx += self.rel
        if idx < len(self.program):
            self.program[idx] = val
            return
        self.memory[idx] = val

    def _op_halt(self):
        self.halted = True 
    _opcodes[99] = _op_halt
    _op_halt.arguments = 0


    def _op_add(self, a, b, target):
        self.set(target[0], self.get(*a) + self.get(*b), target[1])
        self.pc += 4

    _opcodes[1] = _op_add
    _op_add.arguments = 3


    def _op_multiply(self, a, b, target):
        self.set(target[0], self.get(*a) * self.get(*b), target[1])
        self.pc += 4

    _opcodes[2] = _op_multiply
    _op_multiply.arguments = 3


    def _op_input(self, target):
        self.set(target[0], self.inputs.popleft(), target[1])
        self.pc += 2

    _opcodes[3] = _op_input
    _op_input.arguments = 1


    def _op_output(self, a):
        self.output = self.get(*a)
        self.pc += 2

    _opcodes[4] = _op_output
    _op_output.arguments = 1


    def _op_jump_if_true(self, a, b):
        if self.get(*a) != 0:
            self.pc = self.get(*b)
        else:
            self.pc += 3

    _opcodes[5] = _op_jump_if_true
    _op_jump_if_true.arguments = 2


    def _op_jump_if_false(self, a, b):
        if self.get(*a) == 0:
            self.pc = self.get(*b)
        else:
            self.pc += 3

    _opcodes[6] = _op_jump_if_false
    _op_jump_if_false.arguments = 2

    def _op_less_than(self, a, b, target):
        self.set(target[0], int(self.get(*a) < self.get(*b)), target[1])
        self.pc += 4

    _opcodes[7] = _op_less_than
    _op_less_than.arguments = 3


    def _op_equals(self, a, b, target):
        self.set(target[0], int(self.get(*a) == self.get(*b)), target[1])
        self.pc += 4

    _opcodes[8] = _op_equals
    _op_equals.arguments = 3


    def _op_add_relative(self, a):
        self.rel += self.get(*a)
        self.pc += 2

    _opcodes[9] = _op_add_relative
    _op_add_relative.arguments = 1


    def run(self):
        while True:
            if self.halted:
                return
            if self.output is not None:
                out = self.output
                self.output = None
                return out

            code = "{:0>5}".format(self.get(self.pc))
            op = self._opcodes[int(code[3:])]
            arguments = []
            for i in range(self.pc + 1, self.pc + 1 + op.arguments):
                arguments.append(self.get(i))
            arguments = zip(arguments, [int(m) for m in reversed(code)][2:2+op.arguments])
            op(self, *arguments)


class TextAdventure(Computer):
    def __init__(self, code_file):
        super().__init__(code_file)

    def command(self, cmd):
        for c in cmd:
            self.inputs.append(ord(c))
        self.inputs.append(ord("\n"))

    def interactive(self):
        while True:
            line = ""
            while (c := chr(self.run())) != "\n":
                line += c
            print(line)
            if line == "Command?":
                self.command(input())

    def take(self, item):
        self.command("take " + item)
        while True:
            line = ""
            while (c := chr(self.run())) != "\n":
                line += c
            if line == "Command?":
                return

    def drop(self, item):
        self.command("drop " + item)
        while True:
            line = ""
            while (c := chr(self.run())) != "\n":
                line += c
            if line == "Command?":
                return

    def parse(self):
        room = None
        doors = []
        items = []
        extra = []
        door = False
        item = False

        while True:
            line = ""
            while (o := self.run()) is not None and (c := chr(o)) != "\n":
                line += c
            if line == "Command?" or o is None:
                break
            elif (match := re.search("== (.*) ==", line)) is not None:
                room = match.group(1)
                continue
            elif line == "Doors here lead:":
                door = True
                item = False
            elif line == "Items here:":
                item = True
                door = False
            elif (match := re.search("- (.*)", line)) is not None:
                if door:
                    doors.append(match.group(1))
                elif item:
                    items.append(match.group(1))
            elif line.strip() != "":
                extra.append(line)

        return room, doors, items, extra


    def run_path(self, path):
        for p in path:
            self.command(p)
            self.parse()


bad_items = set(["molten lava", "photons", "infinite loop", "escape pod", "giant electromagnet"])


def bfs():
    seen = set()
    loc_paths = {}
    item_paths = {}
    q = queue.Queue()
    # ta, path, locations, items
    q.put((TextAdventure("./input.txt"), []))

    while not q.empty():
        ta, path = q.get()
        try:
            loc, dirs, here_items, _ = ta.parse()
        # halted
        except (IndexError, TypeError):
            continue

        if loc in seen:
            continue
        seen.add(loc)
        loc_paths[loc] = path

        for i in here_items:
            if i not in item_paths and i not in bad_items:
                item_paths[i] = path

        for d in dirs:
            new_ta = copy.deepcopy(ta)
            new_ta.command(d)

            q.put((new_ta, path + [d]))

    return loc_paths, item_paths


def rewind(path):
    r = {"east": "west", "west": "east", "north": "south", "south": "north"}
    return list(reversed([r[p] for p in path]))


def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def get_items(loc_paths, item_paths):
    ta = TextAdventure("./input.txt")
    for item, path in item_paths.items():
        ta.run_path(path)
        ta.take(item)
        ta.run_path(rewind(path))

    ta.run_path(loc_paths["Security Checkpoint"])
    ta.parse()

    for items in powerset(item_paths.keys()):
        print("trying:", items, " " * 20, end="\r")
        for r in item_paths.keys():
            ta.drop(r)
        for i in items:
            ta.take(i)
        ta.command("south")
        loc, dirs, items, extra = ta.parse()
        if loc != "Security Checkpoint":
            return extra


loc_paths, item_paths = bfs()
extra = get_items(loc_paths, item_paths)
for line in extra:
    print(line)
