#Donnie Stewart last modified 1/15/21
#Followed the tutorial https://ruslanspivak.com/lsbasi-part7/ from Ruslan's Blog
#All the code below draws from insipration in the tutorial

#tokens become elements derived form raw text


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
                while((self.current_char is not None) and self.current_char.isalpha() ):
                    word = word + self.current_char
                    self.increment()
                    
                if word == "true": 
                    return Token("TRUE", "true")
                if word == "false": 
                    return Token("FALSE", "false")

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

class Parser(object):
    #recieves tokenized texts and parses it into a tree
    def __init__(self, tonkenizer):
        self.tonkenizer = tonkenizer
        # set current token to the first token taken from the input
        self.current_token = self.tonkenizer.create_next_token()

    def bottom(self):
        #most atomic values of the arith language (integers)
        tree = self.current_token
        if tree.value == "-":
            #handles negative numbers
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

        return "unknown"


    def mid(self):
        #handles multiplication of numbers, operations that are here have medium importance.
        tree = self.bottom()
        while self.current_token.value == "*":
            self.current_token = self.tonkenizer.create_next_token()
            tree = ProdExpr(tree, self.bottom())
        return tree

    def top(self):
        #handles plus minus, these operations are easy to separate in math and thus are least important
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
    #recieves a parsed tree and outputs the result
    def __init__(self, tree):
        self.tree = tree

    def recursive_interpret(self, e):
        #simple recursive function to iterate through the tree
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

# #recieves the input from stdin
# while True:
#         try:
#             text = input("")

#         except EOFError:
#             break
# #calls the necessary functions and releases an output
# toke = Tonkenizer(text)
# parse = Parser(toke)
# tree = parse.top()
# print(Interpreter(tree).interpret())


input = "if ( y * 4 < -1 - x ∧ -1 = 0 + y ) then z := ( -1 - -1 ) * -4 else z := 2 * -4 ; if ( y - -3 = y * z ∨ n * y < 1 * 2 ) then skip else if ( 1 < 0 - x ∨ true ) then x := y + -4 else y := -4 * y ⊕ ¬ ;"
tokens = Tonkenizer(input)
for i in range(len(input)):
    current = tokens.create_next_token()
    if(current.type != "EOF"):
        print("Token( {} , '{}')".format(current.type,current.value))