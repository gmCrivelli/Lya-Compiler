# Yacc example
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
import lexer as lex

#tokens = lex.Lexer.tokens

class Parser:

    def __init__(self):
        self.lexer = lex.Lexer()
        self.tokens = self.lexer.tokens
        self.build()

    def build(self):
        self.parser = yacc.yacc(module=self, start='program')

    def p_program(self, p):
        'program : statement_list'
        p[0] = ('Program', p[1])


    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement_list statement'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 3):
            p[0] = p[1] + [p[2]]


    def p_statement(self,p):
        'statement : declaration_statement'
        p[0] = p[1]


    def p_declaration_statement(self,p):
        'declaration_statement : DCL declaration_list SEMI'
        p[0] = ('Declaration', p[2])

    def p_declaration_list(self,p):
        '''declaration_list : identifier
                            | declaration_list COMMA identifier'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 3):
            p[0] = p[1] + [p[2]]



    def p_identifier(self,p):
        'identifier : ID'
        lineno = p.lineno
        p[0] = ('ID'.p[1], lineno)


    def p_expression_minus(self,p):
        'expression : expression MINUS term'
        p[0] = p[1] - p[3]


    def p_expression_term(self,p):
        'expression : term'
        p[0] = p[1]


    def p_term_times(self,p):
        'term : term TIMES factor'
        p[0] = p[1] * p[3]


    def p_term_div(self,p):
        'term : term DIVIDE factor'
        p[0] = p[1] / p[3]


    def p_term_factor(self,p):
        'term : factor'
        p[0] = p[1]


    def p_factor_num(self,p):
        'factor : ICONST'
        p[0] = p[1]


    def p_factor_expr(self,p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]


    # Error rule for syntax errors
    def p_error(self,p):
        print("Syntax error in input!")

    def parse(self, text):
        self.parser.parse(text, self.lexer)

# Build the parser


while True:
    try:
        s = "dcl x, y = 0"
    except EOFError:
        break
    if not s: continue
    result = Parser()
    result.parse(s)
    print(result)



