#Addition:
#addr (add register) stores into register C the result of adding register A and register B.
def addr(registers, a, b, c):
    registers[c] = registers[a] + registers[b]
#addi (add immediate) stores into register C the result of adding register A and value B.
def addi(registers, a, b, c):
    registers[c] = registers[a] + b

#Multiplication:
#mulr (multiply register) stores into register C the result of multiplying register A and register B.
def mulr(registers, a, b, c):
    registers[c] = registers[a] * registers[b]
#muli (multiply immediate) stores into register C the result of multiplying register A and value B.
def muli(registers, a, b, c):
    registers[c] = registers[a] * b

#Bitwise AND:
#banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
def banr(registers, a, b, c):
    registers[c] = registers[a] & registers[b]
#bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
def bani(registers, a, b, c):
    registers[c] = registers[a] & b

#Bitwise OR:
#borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
def borr(registers, a, b, c):
    registers[c] = registers[a] | registers[b]
#bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
def bori(registers, a, b, c):
    registers[c] = registers[a] | b

# Assignment:
# setr (set register) copies the contents of register A into register C. (Input B is ignored.)
def setr(registers, a, b, c):
    registers[c] = registers[a]
# seti (set immediate) stores value A into register C. (Input B is ignored.)
def seti(registers, a, b, c):
    registers[c] = a

# Greater-than testing:
# gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
def gtir(registers, a, b, c):
    registers[c] = 1 if a > registers[b] else 0
# gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
def gtri(registers, a, b, c):
    registers[c] = 1 if registers[a] > b else 0
# gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
def gtrr(registers, a, b, c):
    registers[c] = 1 if registers[a] > registers[b] else 0

# Equality testing:
# eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
def eqir(registers, a, b, c):
    registers[c] = 1 if a == registers[b] else 0
# eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
def eqri(registers, a, b, c):
    registers[c] = 1 if registers[a] == b else 0
# eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
def eqrr(registers, a, b, c):
    registers[c] = 1 if registers[a] == registers[b] else 0
