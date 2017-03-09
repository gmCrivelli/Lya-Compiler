
import sys
import ply.lex as lex

tokens = (
        # Reserved words
        'ARRAY', 'BY', 'CHARS', 'DLC', 'DO', 'DOWN',
        'ELSE', 'ELSIF', 'END', 'EXIT', 'FI',
        'FOR', 'IF', 'IN', 'LOC', 'TYPE', 'OD',
        'PROC', 'REF', 'RESULT', 'RETURN', 'RETURNS',
        'SYN', 'THEN', 'TO', 'WHILE'

        # Predefined words
        'ABS', 'ASC', 'BOOL', 'CHAR', 'FALSE',
        'INT', 'LENGTH', 'LOWER', 'NULL', 'NUM', 'PRINT',
        'READ', 'TRUE', 'UPPER',
        )

# Tokens

# Reserved words
t_ARRAY = 'array'
t_BY = 'by'
t_CHARS = 'chars'
t_DLC = r'dlc'
t_DO = 'do'
t_DOWN = 'down'
t_ELSE = 'else'
t_ELSIF = 'elsif'
t_END = 'end'
t_EXIT = 'exit'
t_FI = 'fi'
t_FOR = 'for'
t_IF = 'if'
t_IN = 'in'
t_LOC = 'loc'
t_TYPE = 'type'
t_OD = 'od'
t_PROC = 'proc'
t_REF = 'ref'
t_RESULT = 'result'
t_RETURN = 'return'
t_RETURNS = 'returns'
t_SYN = r'syn'
t_THEN = 'then'
t_TO = 'to'
t_WHILE = 'while'

# Predefined words
t_ABS = r'abs'
t_ASC = r'asc'
t_BOOL = r'bool'
t_CHAR = r'char'
t_FALSE = r'false'
t_INT = r'int'
t_LENGTH = r'length'
t_LOWER = r'lower'
t_NULL = r'null'
t_NUM = r'num'
t_PRINT = r'print'
t_READ = r'read'
t_TRUE = r'true'
t_UPPER = r'upper'


# Comments
t_ignore_COMMENNT = r'(/\*(.*\n?)\*/|//.*)'


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
