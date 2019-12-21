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


class SpringScript(Computer):

    def __init__(self, code_file, script):
        super().__init__(code_file, SpringScript.callback)
        self.script = iter(script)

    def callback(self):
        o = next(self.script)
        #print(o, end="")
        return ord(o)

    def run_script(self):
        while True:
            output = self.run()
            if output is None:
                break
            if output > 255:
                return output
            #print(chr(output), end="")


script = """
# J = False
NOT J T
AND T J

# if !B: J = True
NOT B T
OR T J

# if !C: J = True
NOT C T
OR T J

# if !D: J = False
AND D J

# if !A: J = True
NOT A T
OR T J

WALK
"""

script = "\n".join([line for line in script.strip().splitlines() if "#" not in line and line.strip() != ""]) + "\n"

spring = SpringScript("./input.txt", script)
damage = spring.run_script()
print("Answer 1:", damage)

script = """
# J = False
NOT J T
AND T J

# if !B: J = True
NOT B T
OR T J

# if !C: J = True
NOT C T
OR T J

# if !D: J = False
AND D J

# if !H: J = False
AND H J

# if !A: J = True
NOT A T
OR T J

RUN
"""

script = "\n".join([line for line in script.strip().splitlines() if "#" not in line and line.strip() != ""]) + "\n"

spring = SpringScript("./input.txt", script)
damage = spring.run_script()
print("Answer 2:", damage)
