# base class for expression
class AST:
    def __init__(self):
        self.type = 'expression'

# basic expression for ARITH
class N(AST):
    def __init__(self, num):
        super().__init__()
        self.name = 'integer expression'
        # only accept integer
        if not isinstance(num, int):
            raise ValueError("only accept integer")
        self.e = num

class SumExpr(AST):
    def __init__(self, expr1, expr2):
        super().__init__()
        self.name = "summation expression"
        self.e1 = expr1
        self.e2 = expr2
class ProdExpr(AST):
    def __init__(self, expr1, expr2):
        super().__init__()
        self.name = "prod expression"
        self.e1 = expr1
        self.e2 = expr2


x = IntExpr()

print(x.type, x.e, x.name)
