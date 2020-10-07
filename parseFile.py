import sys
from lexer import scan_tokens, find_column

'''
P -- program with expressions
E -- expression
V -- variable (I know, bad name, but I can't create other)
D -- disjunction
C -- conjunction
I -- ID

P -> EP | E | \epsilon
E -> I. | I:-D.
I -> string
D -> C,D | C
C -> V;C | V
V -> I | (D)
'''

class Node:
    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name

def pr(node):
    a = "("
    if node.left != None:
        a += pr(node.left)
    a += " " + node.name + " "
    if node.right != None:
        a += pr(node.right)
    a += ')'
    return a

def lexer(s):
    for c in s:
        #print("IN LEXER", c)
        yield c
    while True:
        yield '\0'

class Parser:
    def __init__(self, tokens):
        self.lex = tokens
        self.current = next(self.lex)

    def make_error_msg(self, wanted_token):
        if self.current == '\0':
            print("PARSER ERROR: expected token with type '%s', but got EOF")
        else:
            print("PARSER ERROR: Unexpected token '%s' with type '%s', expected token with type '%s'"
                  ": line %i, colon %i" % (self.current.value, self.current.type, wanted_token,
                                           self.current.lineno, find_column(self.current)))
        raise ValueError()

    def accept(self, accepted_token):
        if self.current.type == accepted_token:
            self.current = next(self.lex)
            return True
        return False

    def expect(self, expected_token):
        if self.current.type == expected_token:
            self.current = next(self.lex)
            return True
        self.make_error_msg(expected_token)
        return False

    # I -> string
    def id(self):
        if self.current.type != 'ID':
            self.make_error_msg('ID')
            return None
        token = self.current
        self.current = next(self.lex)
        return Node(None, None, token.value)

    # V -> I | (D)
    def var(self):
        if self.accept('OPEN'):
            node = self.disj()
            if self.expect('CLOSE'):
                return node
            return None
        return self.id()

    # C -> V;C | V
    def conj(self):
        left = self.var()
        if self.accept('AND'):
            right = self.conj()
            return Node(left, right, 'conj')
        return left

    # D -> C,D | C
    def disj(self):
        left = self.conj()
        if self.accept('OR'):
            right = self.disj()
            return Node(left, right, 'disj')
        return left

    # E -> I. | I:-D.
    def exp(self):
        left = self.id()
        if self.accept('CORK'):
            right = self.disj()
            if self.expect('DEL'):
                return Node(left, right, 'exp')
            return None
        if self.expect('DEL'):
            return left
        return None

    # P -> EP | E | \epsilon
    def prog(self):
        if self.current == '\0':
            return Node(None, None, "empty")
        left = self.exp()
        if self.current == '\0':
            return left
        right = self.prog()
        return Node(left, right, 'prog')

def parse_file(file_name):
    no_error, tokens = scan_tokens(file_name)
    if not no_error:
        print("Error in scanner")
        return False
    print("Scanner worked correct")
    parser = Parser(lexer(tokens))
    try:
        save = parser.prog()
    except:
        print("Catch error in parsing")
        return False

    # print(pr(save))
    print("Correct program")
    return True

if __name__ == "__main__":
    parse_file(sys.argv[1])



