from operator import add, mul


class Expression:
    def __init__(self):
        self.operators = []
        self.tokens = []

    def add_token(self, token):
        if token is '+':
            self.operators.append(add)
        elif token is '*':
            self.operators.append(mul)
        else:
            self.tokens.append(int(token))

    def evaluate(self):
        val = self.tokens.pop(0)
        while self.tokens:
            op = self.operators.pop(0)
            val = op(val, self.tokens.pop(0))
        return val

    def __int__(self):
        return self.evaluate()


def resolve_expression(raw_expression):
    tokens = raw_expression.replace(" ", "")
    expression_queue = []
    expression_queue.append(Expression())

    for token in tokens:
        if token == '(':
            expression_queue.append(Expression())
            continue
        if token == ')':
            token = expression_queue.pop()
        expression_queue[-1].add_token(token)
    return expression_queue[0].evaluate()


def solve1(puzzle_input):
    results = []
    for line in puzzle_input:
        if not line:
            continue
        results.append(resolve_expression(line))
    return sum(results)


class Int(int):
    def __add__(self, other):
        return Int(super().__mul__(other))

    def __mul__(self, other):
        return Int(super().__add__(other))


def solve2(puzzle_input):
    results = []
    for iline in puzzle_input:
        line = iline.replace(" ", "")
        line = line.replace('+', '.')
        line = line.replace('*', '+')
        line = line.replace('.', '*')
        tokens = []
        for token in line:
            if token not in '+*()':
                token = 'Int({})'.format(token)
            tokens.append(token)
        results.append(eval("".join(tokens)))
    return sum(results)
