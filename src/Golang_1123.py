import ply.lex as lex
import ply.yacc as yacc

# keywords
reserved = {
    'var': 'KVAR',
    'int': 'KINT',
    'bool': 'KBOOL',
    'string': 'KSTRING',
    'for': 'KFOR',
    'break': 'KBREAK',
    'default':'KDEFAULT',
    'func':'KFUNC',
    'select':'KSELECT',
    'case': 'KCASE',
    'else': 'KELSE',
    'package': 'KPACKAGE',
    'switch': 'KSWITCH',
    'const': 'KCONST',
    'if': 'KIF',
    'type': 'KTYPE',
    'continue': 'KCONTINUE',
    'import': 'KIMPORT',
    'return': 'KRETURN',
    'Println': 'KPRINT',
    'main': 'KMAIN' #Actually, main is not keywords
}

# tokens
tokens = (
             'LOR', 'LAND',  # logical
             'LE', 'LT', 'GE', 'GT', 'EQ', 'NE',  # relational

             'ID', 'INT', 'BOOL'  # identifier
         ) + tuple(reserved.values())

t_LOR = r'\|\|'
t_LAND = r'&&'

t_LE = r'<='
t_LT = r'<'
t_GE = r'>'
t_GT = r'>='
t_EQ = r'=='
t_NE = r'!='

#t_BLANK = r'( |\t)*'
#t_NEWLINE = r'\n'

def t_BOOL(t):
    r'false|true'
    t.value = True if t.value == 'true' else False
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # keyword check
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


literals = [
    '=', '+', '-', '*', '/',  # arithmetic(except '=')
    '(', ')',  # parenthesis
    '!',  # logical
    ':', ',', '{', '}','"'
]

# Ignored characters
t_ignore = ' \t'


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)


lex.lex()

# lexer.input("1+2+345")
# while True:
#     token = lexer.token()
#     if not token:
#         break
#     print(token)


# Parsing rules

precedence = (
    ('left', 'LAND', 'LOR'),
    ('right', '!'),

    ('nonassoc', 'LE', 'LT', 'GE', 'GT'),  # do not allow expanding
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS')
)

names = {}
global_names = {}
start = 'start'

#USED variables
#start : start symbol
#statement : N line code
#expression : returns integer
#condition : returns bool
#string : returns string
#function 
#blank : single or multiple blank ( |\t)*
#newline : single new line with blank (blank \n blank)
#multiline : multi new line
#empty : NOTHING

def p_start(p):
    """
    start : KPACKAGE KMAIN KIMPORT string main_statement
    """
    if p[4] != "fmt":
        print("Import Error: Unable to find package")

def p_main_statement(p):
    """
    main_statement : global_statement KFUNC KMAIN '(' ')' '{' statement '}' global_statement
    """

def p_global_statement_extension(p):
    """
    global_statement : func_statement global_statement
                     | global_assign_statement global_statement
                     | empty
    """
    
def func_statement(p):
    pass


def p_global_assign_statement_extension(p):
    """
    global_assign_statement : KVAR ID type '=' expression
                            | KVAR ID type '=' string
    """
    if p[2] in global_names:
        print("DO not support redeclaration")

    elif p[3] == 'bool' and type(p[5]) != bool:
        print("TypeError: non bool type assigned to bool")
        global_names[p[2]] = False

    elif p[3] == 'int' and type(p[5]) != int:
        print("TypeError: not int type assigned to int")
        global_names[p[2]] = 0

    elif p[3] == 'string' and type(p[5]) != str:
        print("TypeError: not string type assigned to string")
        global_names[p[2]] = ""

    else:
        global_names[p[2]] = p[5]

def p_global_statement_declaration(p):
    """
    global_assign_statement : KVAR ID type
    """
    if p[2] in global_names:
        print("DO not support redeclaration")

    elif p[3] == 'bool':
        global_names[p[2]] = True #default value
    
    elif p[3] == 'int':
        global_names[p[3]] = 0 #default value
    
    elif p[3] == 'string':
        global_names[p[3]] = "" #default value

        


def p_statement_var_assign(p):
    """
    statement : KVAR ID type '=' expression
              | KVAR ID type '=' string
    """
    if p[2] in names:
        print("DO not support redeclaration")

    elif p[3] == 'bool' and type(p[5]) != bool:
        print("TypeError: non bool type assigned to bool")
        names[p[2]] = False

    elif p[3] == 'int' and type(p[5]) != int:
        print("TypeError: not int type assigned to int")
        names[p[2]] = 0

    elif p[3] == 'string' and type(p[5]) != str:
        print("TypeError: not string type assigned to string")
        names[p[2]] = ""

    else:
        names[p[2]] = p[5]

def p_statement_declaration(p):
    """
    statement : KVAR ID type
    """
    if p[2] in names:
        print("DO not support redeclaration")

    elif p[3] == 'bool':
        names[p[2]] = True #default value
    
    elif p[3] == 'int':
        names[p[3]] = 0 #default value
    
    elif p[3] == 'string':
        names[p[3]] = "" #default value

        
def p_statement_bool_assign(p):
    """
    type : KINT
         | KBOOL
         | KSTRING
         | empty
    """
    p[0] = p[1]

def p_statement_string_assign(p):
    """
    string : '"' statement '"'
    """
    p[0] = p[2]

def p_statement_reassign(p):
    """statement : ID "=" expression"""
    if p[1] in names:
        names[p[1]] = p[3]
    else:
        print("Undefined identifier '%s'" % p[1])
        p[0] = 0

#def p_blank_assign(p):
#    """
#    blank : t_BLANK
#    """
#    p[0] = p[1]

        
#def p_newline_assign(p):
#    """
#    newline : blank t_NEWLINE blank
#    """
#    p[0] = p[2]

#def p_multi_newline(p):
#    """
#    multiline : newline newline
#              | multiline newline
#    """
#    p[0] = p[1] > 무한루프 나옴.


def p_empty(p):
    """empty :"""
    pass


def p_statement_expr(p):
    """
    statement : expression
              | condition
    """
    # print(names)
    print(p[1])

    
def p_if_statement(p):
    """
    statement : KIF condition '{' statement '}' else_statement
    """
    #How to return?
    #condition 과 '{'가 같은 줄에 위치해야 함 > 처리방법 고민필요

def p_else_staement_extension(p):
    """
    else_statement : KELSE KIF condition '{' statement '}' else_statement
                   | KELSE condition '{' statement '}'
    """
    #How to return?

def p_switch_statement(p):
    """
    statement : KSWITCH '{' case_statement '}'
              | KSWITCH ID '{' case_var_statement '}'
    """

def p_case_statement_extension(p):
    """
    case_statement : KCASE condition ':' statement case_statement
                   | KDEFAULT ':' statement case_without_default_statement
                   | empty
    """

def p_case_without_default_statement_extention(p):
    """
    case_without_default_statement : KCASE condition ':' statement case_without_default_statement
                                   | empty
    """
    

def p_case_var_statment_extension(p):
    """
    case_var_statement : KCASE var_statement ':' statement case_var_statement
                       | KDEFAULT ':' statement case_var_without_default_statement
                       | empty
    """

def p_case_var_without_default_statement_extension(p):
    """
    case_var_without_default_statement : KCASE var_statement ':' statement case_var_without_default_statement
                                       | empty
    """

def p_var_statement_extention(p):
    """
    var_statement : INT ',' var_statement
                  | ID ',' var_statement
                  | empty
    """
#TYPE ISSUE!
    
def p_for_statement(p):
    """
    statement : KFOR single_line_statement ';' condition ';' single_line_statement '{' for_statement '}'
              | KFOR condition '{' for_statement '}'
              | KFOR range_statement '{' for_statement '}'
              | KFOR '{' for_statement '}'
    """
    #range_statement에서 range처리!

def p_single_line_statement_extention(p):
    """
    single_line_statement : empty
    """

def p_range_statement_extension(p):
    """
    range_statement : empty
    """

def p_for_statement_extension(p):
    """
    for_statement : statement KCONTINUE for_statement
                  | statement KBREAK for_statement
                  | statement
    """

def p_expression_binop(p):
    """
    expression : expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
    """

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_int(p):
    "expression : INT"
    p[0] = p[1]


def p_expression_name(p):
    "expression : ID"
    try:
        p[0] = global_names[p[1]]
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined identifier '%s'" % p[1])
        p[0] = 0


def p_condition_binop(p):
    """
    condition : condition LAND condition
              | condition LOR condition
    """

    if p[2] == '&&':
        p[0] = p[1] and p[3]
    elif p[2] == '||':
        p[0] = p[1] or p[3]


def p_condition_group(p):
    """condition : '(' condition ')'"""
    p[0] = p[2]


def p_condition_unot(p):
    """condition : '!' condition"""
    p[0] = not p[2]


def p_condition_bool(p):
    """condition : BOOL"""
    p[0] = p[1]


def p_condition_relop(p):
    """
    condition : expression LT expression
              | expression LE expression
              | expression GT expression
              | expression GE expression
              | expression EQ expression
              | expression NE expression
    """
    if p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


yacc.yacc()

import logging

logging.basicConfig(
    level=logging.INFO,
    filename="parse_log.txt"
)

while True:
    try:
        s = input('stmt > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s, debug=logging.getLogger())



"""
결론적으로, 이번에 구현하기로 했었던 연산자들에 대해서 대부분 구현하는데 성공한 것 같습니다.

우선 데이터 타입을 int와 bool로 한정했고, 
int op에 대해는 expression을 grammer의 variable로 사용했으며 bool op에는 condition을 사용했습니다.

할당 연산자 '='에 대하여 var a = 3, var a int = 3을 모두 허용하도록 구현했으며,
뒤에 타입 keyword가 있을 경우에는 type check를 하도록 임시로 조치해놓았습니다.

현재는 python shell같이 구현을 해놓아서 입력한 stmt의 value를 반환하지만, 
추후에 parse 구조를 반환하게 바꾸는 등의 방법을 사용할 수 있을 것 같습니다.


어제 주신 코드에서의 이슈에 대해서도 생각해 보았는데,
lex에 관해서는 prefix가 문제가 된 것으로 보입니다. 
ply 공식 document(http://www.dabeaz.com/ply/ply.html)를 조금 읽어보니 token의 선언 순서가 길이가 긴 것 부터 되지 않으면
예를 들어, '+' 와 '+='을 구분할 때 항상 '+'로 구분하게 된다고 하네요...
저도 코드 작성해보면서 이런 형태의 오류가 자주 나왔던 것 같습니다.

parser에서는 우선 grammer를 선언할 때 colon 대신 화살표를 쓴게 문제 될 수 도 있을 것 같습니다.
그리고 말씀하신 p sequence에 type을 따로따로 assign하는 것에 대하여 
저는 앞서 말씀드린 variable을 분리하는 방식을 사용했습니다.

grammer는 임시로 짠거라서 precedence나 conflict에 대해서 아직 검증하지는 않았습니다.
이 문제는 추후에 또 논의해 보면 좋을 것 같습니다.
"""


"""
전역변수와 지역변수 : main함수 밖에서 선언하는 전역변수와 main함수 안에서 선언하는 지역변수 두 가지로 나누었습니다.
이 외의 새로운 지역변수를 선언하는 경우는 일단 막았습니다.
전역변수를 선언할 때 var x int = 2의 형태로 선언과 동시에 값을 입력할 수 있으나, var x int \n x = 2와 같이 변수를 선언하고, 다른 줄에서 값을 할당할 수는 없습니다.
이는 Golang 문법상 이렇게 구현되는 것이 맞습니다.

시작변수 start를 도입하여 package main import "fmt"를 사용하지 않으면 main함수를 호출할 수 없도록 하였습니다.

구현한 것: if문, for문의 뼈대, switch문, 시작변수의 도입, 전역변수와 지역변수

구현해야할 것: for문 내부에서 작동하는 range, for문 초기, 끝나는 조건, := 문법, 함수의 선언과 리턴, BLANK처리
"""