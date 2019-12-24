from collections import defaultdict, deque
import queue
import threading

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
        self.inputs = queue.Queue()

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
        self.set(target[0], self.inputs.get_nowait(), target[1])
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


class NetworkComputer(Computer):
    STATE_RUNNING = 0
    STATE_RECEIVING = 1

    def __init__(self, code_file, id):
        super().__init__(code_file)
        self.id = id
        self.inputs.put(id)
        self.state = None

    def run_computer(self):
        self.state = self.STATE_RUNNING
        try:
            dest, x, y = self.run(), self.run(), self.run()
            return dest, x, y
        except queue.Empty:
            self.STATE_RECEIVING
            self.inputs.put(-1)
        return None, None, None


def NAT(computers):
    my_x = None
    my_y = None
    seen = set()
    while True:
        idle = True
        for c in computers.values():
            dest, x, y = c.run_computer()
            if dest is None:
                continue
            idle = False
            if dest == 255:
                my_x, my_y = x, y
                continue
            computers[dest].inputs.put(x)
            computers[dest].inputs.put(y)

        if idle and my_y is not None:
            if len(seen) == 0:
                print("Answer 1:", my_y)
            if my_y in seen:
                print("Answer 2:", my_y)
                return
            seen.add(my_y)
            computers[0].inputs.put(my_x)
            computers[0].inputs.put(my_y)


computers = {}
for id in range(50):
    computers[id] = NetworkComputer("./input.txt", id)

NAT(computers)
