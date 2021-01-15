
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tonkenizer():
    #Takes in text and cleans it for individual tokens
    def __init__(self, text):
        # input from test string
        self.text = text
        # index position in the text
        self.i = 0
        self.current_char = self.text[self.i]


    def increment(self):
        #in
        self.i += 1
        str_len = len(self.text)
        if self.i >= str_len:
            self.current_char = None
        else:
            self.current_char = self.text[self.i]

    def integer(self):
        int1 = ''
        int1 = int1 + self.current_char
        self.increment()
        while self.current_char is not None and self.current_char.isdigit():
            int1 = int1 + self.current_char
            self.increment()

        return int(int1)

    def create_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.increment()
                continue
            if self.current_char == "'":
                self.increment()
                continue
            if self.current_char.isdigit():
                return Token("INT", self.integer())
            if self.current_char == "+":
                self.increment()
                return Token("PLUS", "+")
            if self.current_char == "-":
                self.increment()
                return Token("MINUS", "-")
            if self.current_char == "*":
                self.increment()
                return Token("MUL", "*")
            return "Unknown value"
        return Token("EOF", None)


class Expession():
    def __init__(self, e1, type, e2):
        self.e1 = e1
        self.type = type
        self.e2 = e2

class Num():
    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.type = "Num"

class SumExpr(Expession):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "PLUS", expr2)

class ProdExpr(Expession):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "MUL", expr2)

class MinusExpr(Expession):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "MINUS", expr2)

class Parser(object):
    def __init__(self, tonkenizer):
        self.tonkenizer = tonkenizer
        # set current token to the first token taken from the input
        self.current_token = self.tonkenizer.create_next_token()

    def bottom(self):
        tree = self.current_token
        if tree.value == "-":
            self.current_token = self.tonkenizer.create_next_token()
            tree = self.current_token
            tree.value = -tree.value
            #print(tree.value)
            self.current_token = self.tonkenizer.create_next_token()
            #print(self.current_token.value)

            return Num(tree)

        elif type(tree.value) == int:
            #print(tree.value)
            self.current_token = self.tonkenizer.create_next_token()
            #print(self.current_token.value)
            return Num(tree)

        return "unknonw"


    def mid(self):
        tree = self.bottom()
        while self.current_token.value == "*":
            self.current_token = self.tonkenizer.create_next_token()
            tree = ProdExpr(tree, self.bottom())
        return tree

    def top(self):
        tree  = self.mid()
        while self.current_token.value in ("+", "-"):
            if self.current_token.value == "+":
                self.current_token = self.tonkenizer.create_next_token()
                tree = SumExpr(tree, self.mid())
                #return tree
            if self.current_token.value == "-":
                self.current_token = self.tonkenizer.create_next_token()
                tree = MinusExpr(tree, self.mid())

        return tree


class Interpreter():
    def __init__(self, tree):
        self.tree = tree

    def recursive_interpret(self, e):
        #print(e.type )
        if e.type == "Num":
            return e.value
        elif e.type == "PLUS":
            return self.recursive_interpret(e.e1) + self.recursive_interpret(e.e2)
        elif e.type == "MINUS":
            return self.recursive_interpret(e.e1) - self.recursive_interpret(e.e2)
        elif e.type == "MUL":
            return self.recursive_interpret(e.e1) * self.recursive_interpret(e.e2)

    def interpret(self):
        return self.recursive_interpret( self.tree)

while True:
        try:
            text = input("")

        except EOFError:
            break
toke = Tonkenizer(text)
parse = Parser(toke)
tree = parse.top()
print(Interpreter(tree).interpret())