import copy
from collections import defaultdict, deque
import itertools
import queue
import time

class Computer:
    MODE_POSITION = 0
    MODE_IMMEDIATE = 1
    MODE_RELATIVE = 2

    _opcodes = {}

    def __init__(self, code_file, input_callback=None):
        with open(code_file) as f:
            self.program = [int(code.strip()) for code in f.read().strip().split(",")]
        self.memory = defaultdict(lambda:0)
        self.pc = 0
        self.rel = 0
        self.halted = False
        self.output = None
        self.input_callback = input_callback

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
        inp = self.input_callback(self)
        self.set(target[0], inp, target[1])
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


class Robot(Computer):

    def __init__(self, code_file):
        super().__init__(code_file, Robot.callback)
        self.map = {}
        self.commands = None

    def generate_map(self):
        x, y = 0, 0
        while True:
            if (out := self.run()) is None:
                return
            if chr(out) == "\n":
                x = 0
                y += 1
                continue
            if chr(out) not in [".", "#", "<", ">", "^", "v"]:
                return
            self.map[(x, y)] = chr(out)
            x += 1

    def print_map(self):
        ints = self.find_intersections()
        max_x = max([x for x, y in self.map.keys()])
        max_y = max([y for x, y in self.map.keys()])
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if (x, y) in ints:
                    print("O", end="")
                else:
                    print(self.map[(x, y)], end="")
            print("")

    def find_intersections(self):
        ints = []
        dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))
        for (x, y) in list(self.map.keys()):
            c = self.map[(x, y)]
            if c != "#":
                continue
            num = 0
            for d in dirs:
                if self.map.get((x + d[0], y + d[1]), None) == "#":
                    num += 1
                    if num > 2:
                        ints.append((x, y))
                        break

        return ints

    def find_path(self):
        unseen = set([k for k, v in self.map.items() if v == "#"])
        r = [k for k, v in self.map.items() if v in "<>^v"][0]
        path = ["L"]
        direction = deque([(-1, 0), (0, -1), (1, 0), (0, 1)])
        length = 0
        while len(unseen) > 0:
            unseen.discard(r)
            if self.map.get((r[0] + direction[0][0], r[1] + direction[0][1]), None) == "#":
                length += 1
                r = (r[0] + direction[0][0], r[1] + direction[0][1])
                continue
            if self.map.get((r[0] + direction[1][0], r[1] + direction[1][1]), None) == "#":
                path.append(length)
                length = 0
                direction.rotate(-1)
                path.append("R")
            elif self.map.get((r[0] + direction[-1][0], r[1] + direction[-1][1]), None) == "#":
                path.append(length)
                length = 0
                direction.rotate(1)
                path.append("L")

        path.append(length)
        return path

    def find_routine(self):
        path = self.find_path()
        tokens = [tuple(path[i:i+2]) for i in range(0, len(path), 2)]
        count = defaultdict(lambda:0)

        for i in range(len(tokens)):
            for l in range(2, 10):
                if i+l < len(tokens):
                    count[tuple(tokens[i:i+l])] += 1

        pq = sorted([(c, t) for t, c in count.items() if c >= 3], reverse=True)
        pathtxt = ",".join(str(p) for p in path)
        A, B, C = None, None, None
        for (_, a), (_, b), (_, c) in itertools.combinations(pq, 3):
            A = ",".join("{},{}".format(d, n) for d, n in a)
            B = ",".join("{},{}".format(d, n) for d, n in b)
            C = ",".join("{},{}".format(d, n) for d, n in c)
            if len(pathtxt.replace(A, "").replace(B, "").replace(C, "").replace(",", "")) == 0:
                break

        routine = pathtxt.replace(A, "A").replace(B, "B").replace(C, "C")
        return iter("{}\n{}\n{}\n{}\nn\n".format(routine, A, B, C))

    def callback(self):
        return ord(next(self.commands))

    def run_robot(self, commands):
        self.set(0, 2)
        self.commands = commands
        self.generate_map()
        output = []
        while (out := self.run()) is not None:
            output.append(out)
        return output[-1]


robot = Robot("./input.txt")
robot.generate_map()
ints = robot.find_intersections()
print("Answer 1:", sum([x * y for x, y in ints]))

commands = robot.find_routine()
robot = Robot("./input.txt")
dust = robot.run_robot(commands)
print("Answer 2:", dust)
