
import sys
import ply.lex as lex

# Reserved
reserved = {
    # Reserved words
    'array': 'ARRAY',
    'by': 'BY',
    'chars': 'CHARS',
    'dcl': 'DCL',
    'do': 'DO',
    'down': 'DOWN',
    'else': 'ELSE',
    'elsif': 'ELSIF',
    'end': 'END',
    'exit': 'EXIT',
    'fi': 'FI',
    'for': 'FOR',
    'if': 'IF',
    'in': 'IN',
    'loc': 'LOC',
    'type': 'TYPE',
    'od': 'OD',
    'proc': 'PROC',
    'ref': 'REF',
    'result': 'RESULT',
    'return': 'RETURN',
    'returns': 'RETURNS',
    'syn': 'SYN',
    'then': 'THEN',
    'to': 'TO',
    'while': 'WHILE',

    # Predefined words
    'abs': 'ABS',
    'asc': 'ASC',
    'bool': 'BOOL',
    'char': 'CHAR',
    'false': 'FALSE',
    'int': 'INT',
    'length': 'LENGTH',
    'lower': 'LOWER',
    'null': 'NULL',
    'num': 'NUM',
    'print': 'PRINT',
    'read': 'READ',
    'true': 'TRUE',
    'upper': 'UPPER'
}

# Tokens
tokens = [
        # Identifier
        'ID',

        # Operations and Delimiters
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'ASSIGN', 'COMMA', 'COLON', 'SEMI', 'ARROW',
        'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
        'LESS', 'LESSEQ', 'GREATER', 'GREATEREQ', 'EQUAL',
        'INCREASE', 'DECREASE', 'MULVAL', 'DIVVAL',

        # Literals
        'ICONST', 'CCONST', 'SCONST'
        ] + list(reserved.values())

# Operations and Delimiters
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_COMMA = r','
t_COLON = r':'
t_SEMI = r';'
t_ARROW = r'->'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LESS = r'<'
t_LESSEQ = r'<='
t_GREATER = r'>'
t_GREATEREQ = r'>='
t_EQUAL = r'=='
t_INCREASE = r'\+='
t_DECREASE = r'-='
t_MULVAL = r'\*='
t_DIVVAL = r'/='

# Comments
t_ignore_COMMENNT = r'(/\*(.*\n?)\*/|//.*)'

# Identifier
def t_ID(t):
    r'[A-Za-z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    return t


def t_ICONST(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_CCONST(t):
    r'\'(\\\"|\\\'|[^\'\"])\''
    t.value = chr(t.value)
    return t


def t_SCONST(t):
    r'\'(\\\"|\\\'|[^\'\"])*\''
    t.value = str(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Error
# def t_error(t):
#     print("Error at " + str(t.lexer.lineno))
#     t.lexer.skip(1)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def main():
    file_name = sys.argv[1]

    # Read given file
    file = open(file_name, "r")

    file_content = file.read()

    lexer = lex.lex()

    # Give the lexer some input
    lexer.input(file_content)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break # No more input
        print(tok)

if __name__ == "__main__": main()
