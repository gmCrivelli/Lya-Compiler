# Yacc example
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens

def p_program(self, p):
    'program : statement_list'
    p[0] = Program(p[1])

def p_statement_list(self, p):
    '''statement_list : statement
                      | statement statement_list'''
    #if(len(p) == 2)
        p[0] = Statement_List(p[1])
    #elif(len(p) == 3)

def p_statement(self, p):
    '''statement : declaration_statement
                | synonym_statement
                | newmode_statement
                | procedure_statement
                | action_statement'''
    p[0] = Statement(p[1])

def p_declaration_statement(self, p):
    '''declaration_statement : DCL declaration_list ;'
                | synonym_statement
                | newmode_statement
                | procedure_statement
                | action_statement'''
    p[0] = Statement(p[1])


def p_identifier(self, p):
    'identifier : ID'
    p[0] = ID(p[1], lineno=p.lineno)


def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
        s = 1 #raw_input('calc > ')
   except EOFError:
        break
   if not s: continue
   result = parser.parse(s)
   print(result)

