import sys
import ply.yacc as yacc
from lexer import tokens, find_column

'''
seq -- sequence of definitions  
def -- expression
disj -- disjunction
conj -- conjunction
oper -- operand
atom -- atom
tail -- tail of atom
id -- identifier

seq -> def | def seq
def -> atom. | atom:-disj.
disj -> conj | conj,disj
conj -> oper | oper;conj
oper -> atom | (disj)
atom -> id | id tail
tail -> atom | (tail) | (tail) A
I -> string
'''

class Node:
    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name

def pr(node):
    a = ""
    a += node.name
    if node.left != None:
        if node.name == "SEQ":
            a += '\n'
        a += ' (' + pr(node.left) + ')'
    if node.right != None:
        if node.name == "SEQ":
            a += '\n'
        a += ' (' + pr(node.right) + ')'
    return a

def p_seq(p):
    '''seq : def
           | def seq '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[1], p[2], "SEQ")

def p_def(p):
    '''def : atom DEL
           | atom CORK disj DEL '''
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = Node(p[1], p[3], "DEF")

def p_disj(p):
    '''disj : conj
            | conj OR disj '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[1], p[3], "OR")

def p_conj(p):
    '''conj : oper
            | oper AND conj '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[1], p[3], "AND")


def p_oper(p):
    '''oper : atom
            | OPEN disj CLOSE '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_atom(p):
    '''atom : ID
            | ID tail '''
    if len(p) == 2:
        p[0] = Node(None, None, 'ID ' + p[1])
    else:
        p[0] = Node(Node(None, None, 'ID ' + p[1]), p[2], "ATOM")

def p_tail(p):
    '''tail : atom
            | OPEN tail CLOSE
            | OPEN tail CLOSE tail '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = Node(p[2], p[4], "TAIL")

def p_error(p):
    if p == None:
        print("No delimiter at the end of defenition")
    else:
        print("Something wrong on position: line %s, column %s" % (p.lineno, find_column(p)))
    raise ValueError("Parse error")


parser = yacc.yacc()

sys.stdout = open(sys.argv[1] + '.out', 'w')
'''
while True:
  try:
    s = input("calc> ")
  except EOFError:
    break
  if not s:
    continue
  result=parser.parse(s)
  print(result)
'''
sys.stdout = open(sys.argv[1] + '.out', 'w')

with open(sys.argv[1], 'r') as inf:
  try:
    result = parser.parse(inf.read())
    print(pr(result))
  except ValueError:
    pass


