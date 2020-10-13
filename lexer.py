import ply.lex as lex

tokens = ['CORK', 'ID', 'DEL', 'AND', 'OR', 'OPEN', 'CLOSE']

t_AND = ','
t_OR = ';'
t_ID = r'[a-zA-Z][a-zA-Z_0-9]*'
t_CORK = r':-'
t_DEL = r'[.]'
t_OPEN = r'\('
t_CLOSE = r'\)'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

input_for_scan = "abc"

def find_column(token):
    line_start = input_for_scan.rfind('\n', 0, token.lexpos + 1) + 1
    return (token.lexpos - line_start) + 1

no_errors = True
def t_error(t):
    global no_errors
    no_errors = False
    print("SCANNER ERROR: illegal character '%s': line %i, colon %i" % (t.value[0], t.lineno, find_column(t)))
    t.lexer.skip(1)
    raise ValueError("")

def scan_tokens(file_name):
    lexer = lex.lex()
    global  input_for_scan
    input_for_scan = open(file_name).read()
    lexer.input(input_for_scan)
    read_tokens = []
    global no_errors
    while True:
        r'\+'
        tok = lexer.token()
        if not tok:
            break
        read_tokens.append(tok)

    return no_errors, read_tokens

lexer = lex.lex()

