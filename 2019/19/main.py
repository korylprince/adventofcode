from collections import defaultdict, deque
import itertools
import queue
import math

class Computer:
    MODE_POSITION = 0
    MODE_IMMEDIATE = 1
    MODE_RELATIVE = 2

    _opcodes = {}

    def __init__(self, code_file, input_callback=None):
        with open(code_file) as f:
            self._program = [int(code.strip()) for code in f.read().strip().split(",")]
        self._memory = defaultdict(lambda:0)
        self.input_callback = input_callback
        self.reset()

    def reset(self):
        self.program = self._program[:]
        self.memory = self._memory.copy()
        self.pc = 0
        self.rel = 0
        self.halted = False
        self.output = None

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
        self.commands = queue.Queue()

    def callback(self):
        i = self.commands.get()
        return i

    def check_coords(self, x, y):
        self.commands.put(x)
        self.commands.put(y)
        return self.run()

    def generate_map(self):
        for x in range(50):
            for y in range(50):
                self.map[(x, y)] = "#" if self.check_coords(x, y) else "."
                self.reset()

    def print_map(self):
        max_x = max([x for x, y in self.map.keys()])
        max_y = max([y for x, y in self.map.keys()])
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                print(self.map[(x, y)], end="")
            print("")

    def get_square(self, x_start):
        y = 0
        v = 0
        while v == 0:
            y += 1
            v = self.check_coords(x_start, y)
            self.reset()
        y_start = y
        while v == 1:
            y += 1
            v = self.check_coords(x_start, y)
            self.reset()
        y_end = y - 1
        self.reset()
        x = x_start
        y = y - 1
        v = 1
        while v == 1:
            x += 1
            y -= 1
            v = self.check_coords(x, y)
            self.reset()
        x_end = x - 1
        y_end = y + 1

        return (x_start, y_end), x_end - x_start + 1

    def find_closest(self, target):
        low = 0
        high = target * 20
        p = None
        while low <= high:
            mid = math.floor((high + low) / 2)
            p, res = self.get_square(mid)
            if res < target:
                low = mid + 1
            else:
                high = mid - 1

        p, res = self.get_square(low)
        return p

robot = Robot("./input.txt")
robot.generate_map()
print("Answer 1:", len([p for p in robot.map.values() if p == "#"]))


robot.reset()
corner = robot.find_closest(100)
print("Answer 2:", corner[0] * 10_000 + corner[1])
