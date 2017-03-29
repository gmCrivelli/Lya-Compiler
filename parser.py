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
        p[0] = ('Program', p[1], p.lineno)

    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement_list statement'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 3):
            p[0] = p[1] + [p[2]]


    def p_statement(self,p):
        '''statement : declaration_statement
                     | synonym_statement
                     | newmode_statement
                     | procedure_statement
                     | action_statement'''
        p[0] = ('Statement', p[1], p.lineno)

    def p_declaration_statement(self,p):
        'declaration_statement : DCL declaration_list SEMI'
        p[0] = ('Declaration_Statement', p[1], p[2], p[3], p.lineno)

    def p_declaration_list(self,p):
        '''declaration_list : declaration
                            | declaration_list COMMA declaration'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 4):
            p[0] = p[1] + [p[3]]

    def p_declaration(self, p):
        '''declaration : identifier_list mode
                       | identifier_list mode initialization'''
        if (len(p) == 3):
            p[0] = ('Declaration', p[1], p[2], p.lineno)
        elif (len(p) == 4):
            p[0] = ('Declaration', p[1], p[2], p[3], p.lineno)

    def p_initialization(self,p):
        'initialization : assignment_symbol expression'
        p[0] = ('Initialization', p[1], p[2], p.lineno)

    def p_identifier_list(self, p):
        '''identifier_list : identifier
                           | identifier_list identifier'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 3):
            p[0] = p[1] + [p[2]]

    def p_identifier(self,p):
        'identifier : ID'
        lineno = p.lineno
        p[0] = ('ID'.p[1], lineno)

    def p_synonym_statement(self, p):
        'synonym_statement : SYN synonym_list'
        p[0] = ('Synonym_statement', p[1], p.lineno)

    def p_synonym_list(self, p):
        '''synonym_list : synonym_definition
                        | synonym_list synonym_definition'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 3):
            p[0] = p[1] + [p[2]]

    def p_synonym_definition(self, p):
        '''synonym_definition : identifier_list ASSIGN constant_expression
                              | identifier_list mode ASSIGN constant_expression'''
        if (len(p) == 4):
            p[0] = ('Synonym Definition', p[1], p[2], p[3], p.lineno)
        elif (len(p) == 5):
            p[0] = ('Synonym Definition', p[1], p[2], p[3], p[4], p.lineno)

    def p_constant_expression(self, p):
        'constant_expression : expression'
        p[0] = ('Constant Expression', p[1], p.lineno)

    def p_newmode_statement(self, p):
        'newmode_statement : TYPE newmode_list SEMI'
        p[0] = ('Newmode Statement', p[1], p[2], p[3], p.lineno)

    def p_newmode_list(self, p):
        '''newmode_list : mode_definition
                        | newmode_list mode_definition'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 3):
            p[0] = p[1] + [p[2]]

    def p_mode_definition(self, p):
        'mode_definition : identifier_list ASSIGN mode'
        p[0] = ('Mode Definition', p[1], p[2], p[3], p.lineno)

    def p_mode(self, p):
        '''mode : mode_name
                | discrete_mode
                | reference_mode
                | composite_mode'''
        p[0] = ('Mode', p[1], p.lineno)

    def p_discrete_mode(self, p):
        '''discrete_mode : integer_mode
                | boolean_mode
                | character_mode
                | discrete_range_mode'''
        p[0] = ('Discrete Mode', p[1], p.lineno)

    def p_integer_mode(self, p):
        '''integer_mode : INT'''
        p[0] = ('integer_mode', p[1], p.lineno)

    def p_boolean_mode(self, p):
        '''boolean_mode : BOOL'''
        p[0] = ('boolean_mode', p[1], p.lineno)

    def p_character_mode(self, p):
        '''character_mode : CHAR'''
        p[0] = ('character_mode', p[1], p.lineno)

    def p_discrete_range_mode(self, p):
        '''discrete_range_mode : discrete_mode_name LPAREN literal_range RPAREN
                               | discrete_mode LPAREN literal_range RPAREN '''
        p[0] = ('discrete_range_mode', p[1], p[2], p[3], p[4], p.lineno)

    def p_mode_name(self, p):
        '''mode_name : identifier'''
        p[0] = ('mode_name', p[1], p.lineno)

    def p_discrete_mode_name(self, p):
        '''discrete_mode_name : identifier'''
        p[0] = ('discrete_mode_name', p[1], p.lineno)

    def p_literal_range(self, p):
        '''literal_range : lower_bound COLON upper_bound'''
        p[0] = ('literal_range', p[1], p[2], p[3], p.lineno)

    def p_lower_bound(self, p):
        '''lower_bound : expression'''
        p[0] = ('lower_bound', p[1], p.lineno)

    def p_upper_bound(self, p):
        '''upper_bound : expression'''
        p[0] = ('upper_bound', p[1], p.lineno)

    def p_reference_mode(self, p):
        '''reference_mode : REF mode'''
        p[0] = ('reference_mode', p[1], p[2], p.lineno)

    def p_composite_mode(self, p):
        '''composite_mode : string_mode
                          | array_mode'''
        p[0] = ('composite_mode', p[1], p.lineno)

    def p_string_mode(self, p):
        '''string_mode : CHARS LBRACKET string_length RBRACKET'''
        p[0] = ('string_mode', p[1], p[2], p[3], p[4], p.lineno)

    def p_string_length(self, p):
        '''string_length : integer_literal'''
        p[0] = ('string_length', p[1], p.lineno)

    def p_array_mode(self, p):
        '''array_mode : ARRAY LBRACKET index_mode { , index_mode }* RBRACKET element_mode'''
        p[0] = ('array_mode', p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p.lineno)

    def p_index_mode(self, p):
        '''index_mode : discrete_mode | literal_range'''
        p[0] = ('index_mode', p[1], p.lineno)

    def p_element_mode(self, p):
        '''element_mode : mode'''
        p[0] = ('element_mode', p[1], p.lineno)

    def p_location(self, p):
        '''location : location_name
        | dereferenced_reference
        | string_element
        | string_slice
        | array_element
        | array_slice
        | call_action '''
        p[0] = ('location', p[1], p.lineno)

    def p_dereferenced_reference(self, p):
        '''dereferenced_reference : location ARROW'''
        p[0] = ('dereferenced_reference', p[1], p[2], p.lineno)

    def p_string_element(self, p):
        '''string_element : string_location LBRACKET start_element RBRACKET'''
        p[0] = ('string_element', p[1], p[2], p[3], p[4], p.lineno)

    def p_start_element(self, p):
        '''start_element : integer_expression'''
        p[0] = ('start_element', p[1], p.lineno)

    def p_string_slice(self, p):
        '''string_slice : string_location LBRACKET left_element : right_element RBRACKET'''
        p[0] = ('string_slice', p[1], p[2], p[3], p[4], p[5], p[6], p.lineno)

    def p_string_location(self, p):
        '''string_location : identifier'''
        p[0] = ('string_location', p[1], p.lineno)

    def p_left_element(self, p):
        '''left_element : integer_expression'''
        p[0] = ('left_element', p[1], p.lineno)

    def p_right_element(self, p):
        '''right_element : integer_expression'''
        p[0] = ('right_element', p[1], p.lineno)

    def p_array_element(self, p):
        '''array_element : array_location LBRACKET expression_list RBRACKET'''
        p[0] = ('array_element', p[1], p[2], p[3], p[4], p.lineno)

    def p_expression_list(self, p):
        '''expression_list : expression { , expression }*'''
        p[0] = ('expression_list', p[1], p[2], p[3], p[4], p[5], p.lineno)

    def p_array_slice(self, p):
        '''array_slice : array_location LBRACKET lower_bound : upper_bound RBRACKET'''
        p[0] = ('array_slice', p[1], p[2], p[3], p[4], p[5], p[6], p.lineno)

    def p_array_location(self, p):
        '''array_location : location'''
        p[0] = ('array_location', p[1], p.lineno)

    def p_value_array_element(self, p):
        '''value_array_element : array_primitive_value LBRACKET expression_list RBRACKET'''
        p[0] = ('value_array_element', p[1], p[2], p[3], p[4], p.lineno)

    def p_value_array_slice(self, p):
        '''value_array_slice : array_primitive_value LBRACKET lower_element : upper_element RBRACKET'''
        p[0] = ('value_array_slice', p[1], p[2], p[3], p[4], p[5], p[6], p.lineno)

    def p_array_primitive_value(self, p):
        '''array_primitive_value : primitive_value'''
        p[0] = ('array_primitive_value', p[1], p.lineno)

    def p_parenthesized_expression(self, p):
        '''parenthesized_expression : ( expression )'''
        p[0] = ('parenthesized_expression', p[1], p[2], p[3], p.lineno)

    def p_expression(self, p):
        '''expression : operand0 | conditional_expression'''
        p[0] = ('expression', p[1], p[2], p[3], p.lineno)

    def p_conditional_expression(self, p):
        '''conditional_expression : IF boolean_expression then_expression else_expression FI
        | IF boolean_expression then_expression elsif_expression else_expression FI '''
        p[0] = ('conditional_expression', p[1], p[2], p[3], p[4], p[5], p.lineno)

    def p_boolean_expression(self, p):
        '''boolean_expression : expression'''
        p[0] = ('boolean_expression', p[1], p.lineno)

    def p_then_expression(self, p):
        '''then_expression : THEN expression'''
        p[0] = ('then_expression', p[1], p[2], p.lineno)

    def p_else_expression(self, p):
        '''else_expression : ELSE expression'''
        p[0] = ('else_expression', p[1], p[2], p.lineno)


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



