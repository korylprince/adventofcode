MULT = "*"
PLUS = "+"
OPEN = "("
CLOSE = ")"

def tokenize(expr):
    tokens = []
    inter = ""
    for c in expr:
        if c in (MULT, PLUS, OPEN, CLOSE):
            if len(inter) > 0:
                tokens.append(int(inter))
                inter = ""
            tokens.append(c)
        elif c == " ":
            pass
        else:
            inter += c
    if len(inter) > 0:
        tokens.append(int(inter))
    return tokens

def evaluate(tokens):
    val = 0
    op = None
    pos = 0
    while pos < len(tokens):
        if (t := tokens[pos]) in (MULT, PLUS):
            op = t
        elif isinstance(t, int):
            if op is None:
                val = t
            elif op == MULT:
                val *= t
            elif op == PLUS:
                val += t
        elif t == OPEN:
            v, p = evaluate(tokens[pos + 1:])
            if op is None:
                val = v
            elif op == MULT:
                val *= v
            elif op == PLUS:
                val += v
            pos += p + 1
        elif t == CLOSE:
            return val, pos
        pos += 1
    return val

with open("./input.txt") as f:
    exprs = [tokenize(line.strip()) for line in f.read().strip().splitlines()]

print("Answer 1:", sum([evaluate(expr) for expr in exprs]))
