#Donnie Stewart and Surya Keswani last modified 1/22/21
#Followed the tutorial https://ruslanspivak.com/lsbasi-part7/ from Ruslan's Blog
#All the code below draws from insipration in the tutorial

#tokens become elements derived form raw text
from collections import OrderedDict

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer():
    #Takes in text and cleans it for individual tokens
    def __init__(self, text):
        # input from test string
        self.text = text
        # index position in the text
        self.i = 0
        self.current_char = self.text[self.i]

    def increment(self):
        #moves to the next character in the text
        self.i += 1
        str_len = len(self.text)
        if self.i >= str_len:
            self.current_char = None
        else:
            self.current_char = self.text[self.i]

    def integer(self):
        #basic form of the numbers (handles multiple digits)
        int1 = ''
        int1 = int1 + self.current_char
        self.increment()
        while self.current_char is not None and self.current_char.isdigit():
            int1 = int1 + self.current_char
            self.increment()

        return int(int1)

    def create_next_token(self):
        #iterates to the following item for evaluation
        while self.current_char is not None:

            # spaces
            if self.current_char.isspace():
                self.increment()
                continue

            if self.current_char == "'":
                self.increment()
                continue

            #math
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

            # brackers and parens
            if self.current_char == "(":
                self.increment()
                return Token("LPAREN", "(")

            if self.current_char == ")":
                self.increment()
                return Token("RPAREN", ")")

            if self.current_char == "{":
                self.increment()
                return Token("LBRAC", "{")

            if self.current_char == "}":
                self.increment()
                return Token("RBRAC", "}")

            # logical operators and, or, not, less than, greater than, assign, equal
            if self.current_char == "¬":
                self.increment()
                return Token("NOT", "¬")

            if self.current_char == "∧":
                self.increment()
                return Token("AND", "∧")

            if self.current_char == "∨":
                self.increment()
                return Token("OR", "∨")

            if self.current_char == "<":
                self.increment()
                return Token("LESS", "<")

            if self.current_char == ">":
                self.increment()
                return Token("MORE", ">")

            if self.current_char == ":": # increment twice to skip :=
                self.increment()
                self.increment()
                return Token("ASSIGN", ":=")

            if self.current_char == "=":
                self.increment()
                self.increment()
                return Token("EQUAL", "=")

            if self.current_char == "⊕":
                self.increment()
                self.increment()
                return Token("XOR", "⊕")

            if self.current_char == ";":
                self.increment()
                self.increment()
                return Token("SEMI", ";")

            if self.current_char.isalpha():
                word = ""
                while((self.current_char is not None) and (self.current_char.isalpha() or self.current_char.isdigit())):
                    word = word + self.current_char
                    self.increment()

                if word == "true":
                    return Token("BOOL", "true")
                if word == "false":
                    return Token("BOOL", "false")

                if word == "if":
                    return Token("IF", "if")
                if word == "then":
                    return Token("THEN", "then")
                if word == "else":
                    return Token("ELSE", "else")

                if word == "while":
                    return Token("WHILE", "while")
                if word == "do":
                    return Token("DO", "do")
                if word == "skip":
                    return Token("SKIP", "skip")

                else:
                    return Token("VAR", word)

            return "Unknown value"
        return Token("EOF", None)

class Expession():
    #basic element of the tree This becomes the basis for the AST for arith
    def __init__(self, e1, type, e2):
        self.e1 = e1
        self.type = type
        self.e2 = e2

class Num():
    #number element of the tree
    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.type = "Num"

class SumExpr(Expession):
    #for adding two expressions
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "PLUS", expr2)

class ProdExpr(Expession):
    #for multiplying two expressions
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "MUL", expr2)

class MinusExpr(Expession):
    #for subtracting two expressions
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "MINUS", expr2)

class BOOL():
    #true/false element of the tree
    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.type = "BOOL"

class AndExpr(Expession):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "AND", expr2)

class OrExpr(Expession):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "OR", expr2)

class EqualExpr(Expession):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "EQUAL", expr2)

class LessExpr(Expession):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "LESS", expr2)

class MoreExpr(Expession):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, "MORE", expr2)

class NotExpr(Expession):
    def __init__(self, expr1):
        super().__init__(expr1, "NOT", "")

class Var():
    #variable element of the tree
    def __init__(self, token):
        self.token = token
        self.name = token.value
        self.value = 0
        self.type = "Var"

class AssignExpr(Expession):
    def __init__(self,expr1, expr2):
        super().__init__(expr1, "ASSIGN", expr2)
class SkipExpr(Expession):
    def __init__(self,expr1, expr2):
        super().__init__(expr1, "SKIP", expr2)

class SemiExpr(Expession):
    def __init__(self,expr1, expr2):
        super().__init__(expr1, "SEMI", expr2)

class WhileExpr(Expession):
    def __init__(self,expr1, expr2):
        self.b = expr1
        self.c = expr2
        self.type = "WHILEExpr"

class IfExpr():
    def __init__(self,expr1, expr2, expr3):
        self.b = expr1
        self.c1 = expr2
        self.c2 = expr3
        self.type = "IFExpr"


class Parser(object):
    #recieves tokenized texts and parses it into a tree
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        # set current token to the first token taken from the input
        self.current_token = self.tokenizer.create_next_token()

    def bottom(self):
        #most atomic values of the arith language (integers)
        tree = self.current_token
        if tree.value == "-":
            #handles negative numbers
            self.current_token = self.tokenizer.create_next_token()
            tree = self.current_token
            tree.value = -tree.value
            #print(tree.value)
            self.current_token = self.tokenizer.create_next_token()
            return Num(tree)

        elif type(tree.value) == int:
            self.current_token = self.tokenizer.create_next_token()
            return Num(tree)

        elif (tree.type) == "BOOL":
            self.current_token = self.tokenizer.create_next_token()
            return BOOL(tree)
        elif (tree.type) == "VAR":
            self.current_token = self.tokenizer.create_next_token()
            return Var(tree)

        elif (tree.value) == "(":
            #for left/right parenthesis
            self.current_token = self.tokenizer.create_next_token()
            tree = self.semi()
            self.current_token = self.tokenizer.create_next_token()
            return tree
        elif (tree.value) == "{":
            #for left/right curly
            self.current_token = self.tokenizer.create_next_token()
            tree = self.semi()
            self.current_token = self.tokenizer.create_next_token()
            return tree

        elif (tree.value) == "¬":
            self.current_token = self.tokenizer.create_next_token()
            if self.current_token.value == "(":
                self.current_token = self.tokenizer.create_next_token()
                tree = self.semi()
                self.current_token = self.tokenizer.create_next_token()

            elif self.current_token.value == "{":
                self.current_token = self.tokenizer.create_next_token()
                tree = self.semi()
            elif self.current_token.type == "BOOL":
                tree = BOOL(self.current_token)
                self.current_token = self.tokenizer.create_next_token()

            tree = NotExpr(tree)
            return tree

        return "unknown"

    def mid(self):
        #handles multiplication of numbers, operations that are here have medium importance.
        tree = self.bottom()
        while self.current_token.value == "*":
            self.current_token = self.tokenizer.create_next_token()
            tree = ProdExpr(tree, self.bottom())

        return tree

    def top(self):
        #handles plus minus, these operations are easy to separate in math and thus are least important
        tree  = self.mid()
        while self.current_token.value in ("+", "-"):
            if self.current_token.value == "+":
                self.current_token = self.tokenizer.create_next_token()
                tree = SumExpr(tree, self.mid())
                #return tree
            if self.current_token.value == "-":
                self.current_token = self.tokenizer.create_next_token()
                tree = MinusExpr(tree, self.mid())

        return tree

    def comparators(self):
        #handles <,>,= which have low priority
        tree  = self.top()
        while self.current_token.value in ("<", ">", "="):
            if self.current_token.value == "<":
                self.current_token = self.tokenizer.create_next_token()
                tree = LessExpr(tree, self.top())
            if self.current_token.value == ">":
                self.current_token = self.tokenizer.create_next_token()
                tree = MoreExpr(tree, self.top())
            if self.current_token.value == "=":
                self.current_token = self.tokenizer.create_next_token()
                tree = EqualExpr(tree, self.top())
        return tree

    def bools(self):
        #bools have super low priority, thus highest in recurssion
        tree  = self.comparators()
        while self.current_token.value in ("∨", "∧"):
            if self.current_token.value == "∧":
                self.current_token = self.tokenizer.create_next_token()
                tree = AndExpr(tree, self.comparators())
            if self.current_token.value == "∨":
                self.current_token = self.tokenizer.create_next_token()
                tree = OrExpr(tree, self.comparators())
        return tree

    def assign(self):
        tree = self.bools()
        while self.current_token.type in ("ASSIGN", "SKIP"):
            if self.current_token.type == "ASSIGN":
                self.current_token = self.tokenizer.create_next_token()
                tree = AssignExpr(tree, self.bools())
            if self.current_token.type == "SKIP":
                self.current_token = self.tokenizer.create_next_token()
                tree = SkipExpr(tree, self.bools())

        return tree
    def commands(self):
        tree = self.assign()
        while self.current_token.type in ("IF","WHILE"):
            if self.current_token.value == "if":
                if(self.current_token.value != "then"):
                    self.current_token = self.tokenizer.create_next_token()
                    b = self.assign()
                    self.current_token = self.tokenizer.create_next_token()
                    #print("curr token", self.current_token.value)

                if(self.current_token.value != "else"):
                    #self.current_token = self.tokenizer.create_next_token()
                    #print("Before c1", self.current_token.value)
                    c1 = self.assign()
                    #print("c1 is ", c1)
                    self.current_token = self.tokenizer.create_next_token()

                c2 = self.assign()
                #print("c2 is", c2.value)
                # print("B List {}".format(b))
                # print("C1 List {}".format(c1))
                # print("C2 List {}".format(c2))
                tree = IfExpr(b,c1,c2)

            if self.current_token.value == "while":
                self.current_token = self.tokenizer.create_next_token()
                b = self.assign()
                self.current_token = self.tokenizer.create_next_token()
                c = self.assign()
                tree = WhileExpr(b,c)


        return tree

    def semi(self):
        tree = self.commands()
        while self.current_token.type in ("SEMI"):
            if self.current_token.value == ";":
                self.current_token = self.tokenizer.create_next_token()
                tree = SemiExpr(tree, self.commands())
        return tree



class Interpreter():
    #recieves a parsed tree and outputs the result
    def __init__(self, tree):
        self.tree = tree
        self.var_dict = {}

    def recursive_interpret(self, e):
        #simple recursive function to iterate through the tree
        #print("E is ", e)
        # print(e.type)
        if e.type == "Num":
            #print(e.value)
            return e.value
        elif e.type == "PLUS":
            x = (e.e1)
            y = (e.e2)
            if self.check_var(x) and self.check_var(y):
                return self.var_dict[x.name][0] + self.var_dict[y.name][0]
            elif self.check_var(x) and  not self.check_var(y):
                return self.var_dict[x.name][0] + self.recursive_interpret(y)
            elif not self.check_var(x) and self.check_var(y):
                return self.recursive_interpret(x) + self.var_dict[y.name][0]
            return self.recursive_interpret(x) + self.recursive_interpret(y)

        elif e.type == "MINUS":
            x = (e.e1)
            y = (e.e2)
            if self.check_var(x) and self.check_var(y):
                return self.var_dict[x.name][0] - self.var_dict[y.name][0]
            elif self.check_var(x) and  not self.check_var(y):
                return self.var_dict[x.name][0] - self.recursive_interpret(y)
            elif not self.check_var(x) and self.check_var(y):
                return self.recursive_interpret(x) - self.var_dict[y.name][0]
            return self.recursive_interpret(x) - self.recursive_interpret(y)

        elif e.type == "MUL":
            x = (e.e1)
            y = (e.e2)
            if self.check_var(x) and self.check_var(y):
                return self.var_dict[x.name][0] * self.var_dict[y.name][0]
            elif self.check_var(x) and  not self.check_var(y):
                return self.var_dict[x.name][0] * self.recursive_interpret(y)
            elif not self.check_var(x) and self.check_var(y):
                return self.recursive_interpret(x) * self.var_dict[y.name][0]
            return self.recursive_interpret(x) * self.recursive_interpret(y)

        elif e.type == "BOOL":
            # print("asdf",e.value)
            return e.value
        elif e.type == "EQUAL":
            x = (e.e1)
            y = (e.e2)
            if self.check_var(x) and self.check_var(y):
                z = self.var_dict[x.name][0] == self.var_dict[y.name][0]
                return z
            elif self.check_var(x) and  not self.check_var(y):
                z = self.var_dict[x.name][0] == self.recursive_interpret(y)
                return z
            elif not self.check_var(x) and self.check_var(y):
                z = self.recursive_interpret(x) == self.var_dict[y.name][0]
                return z
            x = self.recursive_interpret(e.e1)
            y =  self.recursive_interpret(e.e2)
            z = (x == y)
            return z
        elif e.type == "LESS":
            x = (e.e1)
            y = (e.e2)
            if self.check_var(x) and self.check_var(y):
                z = self.var_dict[x.name][0] < self.var_dict[y.name][0]
                return z
            elif self.check_var(x) and  not self.check_var(y):
                z = self.var_dict[x.name][0] < self.recursive_interpret(y)
                return z
            elif not self.check_var(x) and self.check_var(y):
                z = self.recursive_interpret(x) < self.var_dict[y.name][0]
                return z
            x = self.recursive_interpret(e.e1)
            y =  self.recursive_interpret(e.e2)
            z = (x < y)
            return z
        elif e.type == "MORE":
            x = (e.e1)
            y = (e.e2)
            if self.check_var(x) and self.check_var(y):
                z = self.var_dict[x.name][0] > self.var_dict[y.name][0]
                return z
            elif self.check_var(x) and  not self.check_var(y):
                z = self.var_dict[x.name][0] > self.recursive_interpret(y)
                return z
            elif not self.check_var(x) and self.check_var(y):
                z = self.recursive_interpret(x) > self.var_dict[y.name][0]
                return z
            x = self.recursive_interpret(e.e1)
            y =  self.recursive_interpret(e.e2)
            z = (x > y)
            return z
        elif e.type == "AND":
            x = self.recursive_interpret(e.e1)
            y =  self.recursive_interpret(e.e2)
            z = x and y
            return z
        elif e.type == "OR":
            x = self.recursive_interpret(e.e1)
            y =  self.recursive_interpret(e.e2)
            z = x or y
            return z
        elif e.type == "NOT":

            x = (self.recursive_interpret(e.e1))
            if ( x == "true"):
                return False
            elif ( x == "false"):
                return True
            return not x
        elif e.type == "IFExpr":
            a = self.recursive_interpret(e.b)
            if(a == "true"):
                z = self.recursive_interpret(e.c1)
            elif(a == True):
                z = self.recursive_interpret(e.c1)
            else:
                # print("else")
                z = self.recursive_interpret(e.c2)
            return z
        elif e.type == "WHILEExpr":
            # a = self.recursive_interpret(e.b)
            # print("a is", a)
            # while(a == "true" or a == True):
            while (self.recursive_interpret(e.b) == (True or "true")):
                (self.recursive_interpret(e.c))
            return
        elif e.type == "SEMI":
            left = self.recursive_interpret(e.e1)
            right= self.recursive_interpret(e.e2)
            return

        elif e.type == "Var":
            return e
        elif e.type == "ASSIGN":
            x = self.recursive_interpret(e.e1)
            # print(x)
            x.value = self.recursive_interpret(e.e2)
            self.var_dict[x.name] = (x.value,"keep")
            # print(self.var_dict)
            return

        elif e.type == "SKIP":
            return



    def check_var(self, e):
        # print("in check var",e.type)
        #check if the current expression is a variable
        if e.type ==  "Var" and e.name in self.var_dict:
            #do nothing if already in dict
            return True
        elif e.type ==  "Var" and e.name not in self.var_dict:
            # if not in dict add new var and assign 0
            self.var_dict[e.name] = (0,"del")
            return True
        else:
            #other wise not a variable
            return False


    def interpret(self):
        return self.recursive_interpret(self.tree)

#recieves the input from stdin
while True:
        try:
            text = input("")

        except EOFError:
            break

# text = "if ¬ true then x := 1 else Y := 1"
#calls the necessary functions and releases an output
toke = Tokenizer(text)
parse = Parser(toke)
tree = parse.semi()
y = Interpreter(tree)
y.interpret()

# remove zero values
for key,value in dict(y.var_dict).items():
    if value[1] == "del":
        del y.var_dict[key]

# print the variable dictionary in the proper format
variables = OrderedDict(sorted(y.var_dict.items()))


if(len(variables) == 0):
    final = "{" + "}"
    print(final)
else:
    final = "{"
    for key,value in variables.items():
        final = final + str(key) + " → " + str(value[0]) + ", "

    final = final[:-2]
    final = final + "}"
    print(final)

############################################################
#hi surya these are test strings for you to try:
#(false ∨ true) ∧ (true ∨ false)
#(2 * 4 < 100 ∧ -1 = 0 + 1)
#(2 * 4 < 100 ∧ -1 = -2 + 1)
#true = true ∧ -1 < 2
#¬(true ∨ false)
#¬{(2 * 4 < 100 ∧ -1 = -2 + 1)}
#¬true
# if true then true else false
# if 5 > 10 ∧ 3 < 6 then 1 else 0
# while true do 69
#z8 := 5; z8 := z8 + 1
#while x < 5 do x := x + 1; if x > 7 then x := x + 5 else x := x - 1

# input = "while x < 5 do x := x + 1"
# tokens = Tokenizer(input)

# for i in range(len(input)):
#     current = tokens.create_next_token()
#     if(current.type != "EOF"):
#         print("Token( {} , '{}')".format(current.type,current.value))

# parse = Parser(tokens)
# tree = parse.semi()
# y = Interpreter(tree)
# y.interpret()

# # print the variable dictionary in the proper format
# variables = y.var_dict

# if(len(variables) == 0):
#     final = "{" + "}"
#     print(final)
# else:
#     final = "{"
#     for key,value in variables.items():
#         final = final + str(key) + " → " + str(value) + ", "

#     final = final[:-2]
#     final = final + "}"
#     print(final)
