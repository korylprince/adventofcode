import numpy as np

MULT = "*"
PLUS = "+"
OPEN = "("
CLOSE = ")"

class Parser:
    def __init__(self, expr):
        self.expr = expr
        self.pos = 0

    @property
    def tok(self):
        return self.expr[self.pos]

    def canPeek(self):
        return self.pos < len(self.expr)

    def parseWhitespace(self):
        while self.canPeek():
            if self.tok == " ":
                self.pos += 1
            else:
                break

    def parseExpression(self):
        return self.parseOps()

    def parseOps(self):
        val = self.parseParens(self.parseExpression)
        while self.canPeek():
            self.parseWhitespace()
            if self.tok == PLUS:
                self.pos += 1
                val += self.parseParens(self.parseExpression)
            elif self.tok == MULT:
                self.pos += 1
                val *= self.parseParens(self.parseExpression)
            else:
                break
        return val

    def parseAdvancedExpression(self):
        return self.parseMultiplication()

    def parseMultiplication(self):
        values = [self.parseAddition()]
        while self.canPeek():
            self.parseWhitespace()
            if self.tok == MULT:
                self.pos += 1
                values.append(self.parseAddition())
            else:
                break
        return np.product(values)

    def parseAddition(self):
        values = [self.parseParens(self.parseAdvancedExpression)]
        while self.canPeek():
            self.parseWhitespace()
            if self.tok == PLUS:
                self.pos += 1
                values.append(self.parseParens(self.parseAdvancedExpression))
            else:
                break
        return sum(values)

    def parseParens(self, exprParser):
        self.parseWhitespace()
        if self.tok == OPEN:
            self.pos += 1
            val = exprParser()
            self.parseWhitespace()
            if self.tok != CLOSE:
                raise Exception(f"Expected CLOSE at pos {self.pos}")
            self.pos += 1
            return val
        else:
            return self.parseInt()

    def parseInt(self):
        # yes, I know I only need to parse single-digit ints
        val = ""
        while self.canPeek():
            self.parseWhitespace()
            if (tok := self.tok).isnumeric():
                self.pos += 1
                val += tok
            elif tok in (CLOSE, MULT, PLUS):
                return int(val)
            else:
                raise Exception(f"Unknown token {tok} at pos {self.pos}")
        return int(val)

with open("./input.txt") as f:
    exprs = [line.strip() for line in f.read().strip().splitlines()]

print("Answer 1:", sum([Parser(expr).parseExpression() for expr in exprs]))
print("Answer 2:", sum([Parser(expr).parseAdvancedExpression() for expr in exprs]))
