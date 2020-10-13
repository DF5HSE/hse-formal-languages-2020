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
atombr -- atom in braces
tail -- tail of atom
ID -- identifier

seq -> def | def seq
def -> atom. | atom:-disj.
disj -> conj | conj;disj
conj -> oper | oper,conj
oper -> atom | (disj)
atom -> ID | ID tail
tail -> atom | atombr | atombr tail
atombr -> (atom) | (atombr)
ID -> string
'''

def p_seq(p):
    '''seq : def
           | def seq '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + '\n' + p[2]

def p_def(p):
    '''def : atom DEL
           | atom CORK disj DEL '''
    if len(p) == 3:
        p[0] = 'DEF (' + p[1] + ')'
    else:
        p[0] = 'DEF (' + p[1] + ') (' + p[3] + ')'

def p_disj(p):
    '''disj : conj
            | conj OR disj '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = 'DISJ (' + p[1] + ') (' + p[3] + ')'

def p_conj(p):
    '''conj : oper
            | oper AND conj '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = 'CONJ (' + p[1] + ') (' + p[3] + ')'

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
        p[0] = 'ATOM (' + p[1] + ')'
    else:
        p[0] = 'ATOM (' + p[1] + ' ' + p[2] + ')'

def p_tail_atom(p):
    '''tail : atom'''
    p[0] = p[1]

def p_tail_atombr(p):
    '''tail : atombr
            | atombr tail '''
    if len(p) == 2:
        p[0] = '(' + p[1] + ')'
    elif len(p) == 3:
        p[0] = '(' + p[1] + ')' + ' ' + p[2]

def p_atombr_atom(p):
    '''atombr : OPEN atom CLOSE '''
    p[0] = '(' + p[2] + ')'

def p_atombr_atombr(p):
    '''atombr : OPEN atombr CLOSE '''
    p[0] = '(' + p[2] + ')'

def p_error(p):
    if p == None:
        print("No delimiter at the end of defenition")
    else:
        print("Something wrong on position: line %s, column %s" % (p.lineno, find_column(p)))
    raise ValueError("Parse error")

parser = yacc.yacc()

sys.stdout = open(sys.argv[1] + '.out', 'w')

with open(sys.argv[1], 'r') as inf:
  try:
    result = parser.parse(inf.read())
    print(result)
  except ValueError:
    pass


