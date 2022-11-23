from ply.lex import lex
from ply.yacc import yacc

#keywords
reserved = {
    'var' : 'KVAR',
    'int' : 'KINT',
    'bool' : 'KBOOL'
}

# All tokens must be named in advance.
tokens = ( 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULAR', 'LT','LE','GT','GE','EQ','NE',
            #'DOUBLEPLUS','DOUBLEMINUS',
            'LOGAND',
            'LOGOR',
            'LOGNOT',
            'LPAREN', 'RPAREN',
             'INTEGER','STRING','BOOLEAN' ) + tuple(reserved.values())
#주석처리 한 애들 -> 넣으면 LEX가 안됨

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_MODULAR = r'\%'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
#t_DOUBLEPLUS = r'++'
#t_DOUBLEMINUS = r'--'
t_LOGAND = r'&&'
t_LOGOR = r'\|\|'
t_LOGNOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
#t_UPLUS = r'\+'
#t_UMINUS = r'\-'

#주석처리 한 애들 -> 넣으면 LEX가 안됨


precedence = (
    ('left','LOGOR', 'LOGAND'),
    ('right','LOGNOT'),
    ('left','EQ','NE','LT',"LE","GT","GE"),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MODULAR'),
    #('right','UPLUS','UMINUS'),
    #('left','LPAREN','RPAREN')
)


# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'STRING')
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t


literals = [
    '=', '+', '-', '*', '/',  # arithmetic(except '=')
    '(', ')',  # parenthesis
    '!'  # logical
]

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
    
lexer = lex()

lexer.input("2 * 3 + 4 * (5 - 1)")
while(True):
    token = lexer.token()
    if not token:
        break
    print(token, token.value)

# --- Parser


# Write functions for each grammar rule which is
# specified in the docstring.

#def p_unary_integer(p):
#    '''integer -> PLUS integer %prec UPLUS
#                | MINUS integer  %prec UMINUS'''
#    if p[1] == '+':
#        p[0] = p[2]
#    elif p[2] == '-':
#        p[0] = -p[2]


def p_integer_arthimetric(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULAR expression'''  
    if p[2] == '+':
        p[0] = p[1] + p[3] 
    elif p[2] == '-':
        p[0] = p[1] - p[3] 
    elif p[2] == '*':
        p[0] = p[1] * p[3] 
    elif p[2] == '/':
        p[0] = p[1] / p[3] 
    elif p[2] == '%':
        p[0] = p[1] % p[3]

def p_integer_compare(p):
    '''condition : expression EQ expression
                 | expression NE expression
                 | expression LT expression
                 | expression LE expression
                 | expression GT expression
                 | expression GE expression'''
    if p[2] == '==':
        p[0] = (p[1] == p[3])  
    elif p[2] == '!=':
        p[0] = (p[1] != p[3])  
    elif p[2] == '<':
        p[0] = (p[1] < p[3])  
    elif p[2] == '<':
        p[0] = (p[1] <= p[3])  
    elif p[2] == '>':
        p[0] = (p[1] > p[3])  
    elif p[2] == '>=':
        p[0] = (p[1] >= p[3])

#def p_string_compare(p):
#    """statement : statement EQ statement
#                 | statement NE statement
#    """
#    if p[2] == '==':
#        p[0] = (p[1] == p[3])
#    elif p[2] == '!=':
#        p[0] = (p[1] != p[3])


def p_integer_logical(p):
    '''condition : condition LOGAND condition
                 | condition LOGOR condition
    '''   
    if p[2] == '&&':
        p[0] = (p[1] and p[3])
    elif p[2] == '||':
        p[0] = (p[1] or p[3])
        
 
def p_statement_expr(p):
    """
    statement : expression
              | condition
    """
    p[0] = p[1]

def p_expr_integer(p):
    """
    expression : INTEGER   
    """
    p[0]=p[1]
    
def p_expr_string(p):
    '''
    expression : STRING
    '''
    p[0] = p[1]

def p_condition_boolean(p):
    '''
    condition : BOOLEAN
    '''
    p[0] =  p[1]

def p_condition_grouped(p):
    "condition : LPAREN condition RPAREN"
    p[0] = p[2]
    
def p_expression_grouped(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]
    
def p_error(p):
    print(f'Syntax error at {p.value!r}')
    
def p_empty(p):
    """empty :"""
    pass

# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('(3%2)*3')
print(ast) 