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
        '''program : statement_list'''
        p[0] = ('Program', p[1])

    def p_statement_list(self, p):
        '''statement_list : statement
                          | statement_list statement'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 3):
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        '''statement : declaration_statement'''
        p[0] = p[1]

    def p_declaration_statement(self, p):
        '''declaration_statement : DCL declaration_list SEMI'''
        p[0] = ('Declaration', p[2])

    def p_declaration_list(self, p):
        ''''declaration_list : identifier
                            | declaration_list COMMA identifier'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 4):
            p[0] = p[1] + [p[2]]

    def p_identifier(self, p):
        '''identifier : ID'''
        lineno = p.lineno
        p[0] = ('ID'.p[1], lineno)

    def p_expression_minus(self, p):
        '''expression : expression MINUS term'''
        p[0] = p[1] - p[3]

    def p_expression_term(self, p):
        '''expression : term'''
        p[0] = p[1]

    def p_term_times(self, p):
        '''term : term TIMES factor'''
        p[0] = p[1] * p[3]

    def p_term_div(self, p):
        '''term : term DIVIDE factor'''
        p[0] = p[1] / p[3]

    def p_term_factor(self, p):
        '''term : factor'''
        p[0] = p[1]

    def p_factor_num(self, p):
        '''factor : ICONST'''
        p[0] = p[1]

    def p_factor_expr(self, p):
        '''factor : LPAREN expression RPAREN'''
        p[0] = p[2]

    def p_operand0(self, p):
        '''operand0 :  operand1
            | operand0 operator1 operand1'''
        p[0] = ("operand0", p[1], p[2], p[3], p.lineno)

    def p_operator1(self, p):
        '''operator1 :  relational_operator
            | membership_operator'''
        p[0] = ("operator1", p[1], p.lineno)

    def p_relational_operator(self, p):
        '''relational_operator :  &&
            | ||
            | ==
            | !=
            | >
            | >=
            | <
            | <='''
        p[0] = ("relational_operator", p[1], p.lineno)

    def p_membership_operator(self, p):
        '''membership_operator :  IN'''
        p[0] = ("membership_operator", p[1], p.lineno)

    def p_operand1(self, p):
        '''operand1 :  operand2
            | operand1 operator2 operand2'''
        p[0] = ("operand1", p[1], p[2], p[3], p.lineno)

    def p_operator2(self, p):
        '''operator2 :  arithmetic_additive_operator
            | string_concatenation_operator'''
        p[0] = ("operator2", p[1], p.lineno)

    def p_arithmetic_additive_operator(self, p):
        '''arithmetic_additive_operator :  PLUS
            | MINUS'''
        p[0] = ("arithmetic_additive_operator", p[1], p.lineno)

    def p_string_concatenation_operator(self, p):
        '''string_concatenation_operator :  STRCAT'''
        p[0] = ("string_concatenation_operator", p[1], p.lineno)

    def p_operand2(self, p):
        '''operand2 :  operand3
            | operand2 arithmetic_multiplicative_operator operand3'''
        p[0] = ("operand2", p[1], p[2], p[3], p.lineno)

    def p_arithmetic_multiplicative_operator(self, p):
        '''arithmetic_multiplicative_operator :  TIMES
            | DIVIDE
            | MOD'''
        p[0] = ("arithmetic_multiplicative_operator", p[1], p.lineno)

    def p_operand3(self, p):
        '''operand3 :  [ monadic_operator ] operand4
            | integer_literal'''
        p[0] = ("operand3", p[1], p.lineno)

    def p_monadic_operator(self, p):
        '''monadic_operator :  MINUS
            | NOT'''
        p[0] = ("monadic_operator", p[1], p.lineno)

    def p_operand4(self, p):
        '''operand4 :  location
            | referenced_location
            | primitive_value'''
        p[0] = ("operand4", p[1], p.lineno)

    def p_referenced_location(self, p):
        '''referenced_location :  ARROW location'''
        p[0] = ("referenced_location", p[1], p[2], p.lineno)

    def p_action_statement(self, p):
        '''action_statement :  [ label_id COLON ] action SEMI
            | action SEMI'''
        p[0] = ("action_statement", p[1], p[2], p[3], p[4], p[5], p[6], p.lineno)

    def p_label_id(self, p):
        '''label_id :  identifier'''
        p[0] = ("label_id", p[1], p.lineno)

    def p_action(self, p):
        '''action :  bracketed_action
            | assignment_action
            | call_action
            | exit_action
            | return_action
            | result_action'''
        p[0] = ("action", p[1], p.lineno)

    def p_bracketed_action(self, p):
        '''bracketed_action :  if_action
            | do_action'''
        p[0] = ("bracketed_action", p[1], p.lineno)

    def p_assignment_action(self, p):
        '''assignment_action :  location assigning_operator expression'''
        p[0] = ("assignment_action", p[1], p[2], p[3], p.lineno)

    def p_assigning_operator(self, p):
        '''assigning_operator :  [ closed_dyadic_operator ] assignment_symbol'''
        p[0] = ("assigning_operator", p[1], p[2], p[3], p[4], p.lineno)

    def p_closed_dyadic_operator(self, p):
        '''closed_dyadic_operator :  arithmetic_additive_operator
            | arithmetic_multiplicative_operator
            | string_concatenation_operator'''
        p[0] = ("closed_dyadic_operator", p[1], p.lineno)

    def p_assignment_symbol(self, p):
        '''assignment_symbol :  ASSIGN'''
        p[0] = ("assignment_symbol", p[1], p.lineno)

    def p_if_action(self, p):
        '''if_action :  IF boolean_expression then_clause [ else_clause ] FI'''
        p[0] = ("if_action", p[1], p[2], p[3], p[4], p[5], p[6], p[7], p.lineno)

    def p_then_clause(self, p):
        '''then_clause :  THEN { action_statement }*'''
        p[0] = ("then_clause", p[1], p[2], p[3], p[4], p.lineno)

    def p_else_clause(self, p):
        '''else_clause :  ELSE { action_statement }*
            | ELSIF boolean_expression then_clause [ else_clause ]'''
        p[0] = ("else_clause", p[1], p[2], p[3], p[4], p[5], p[6], p.lineno)

    def p_do_action(self, p):
        '''do_action :  DO [ control_part SEMI ] { action_statement }* OD'''
        p[0] = ("do_action", p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p.lineno)

    def p_control_part(self, p):
        '''control_part :  for_control [ while_control ]
            | while_control'''
        p[0] = ("control_part", p[1], p.lineno)

    def p_for_control(self, p):
        '''for_control :  FOR iteration'''
        p[0] = ("for_control", p[1], p[2], p.lineno)

    def p_iteration(self, p):
        '''iteration :  step_enumeration
            | range_enumeration'''
        p[0] = ("iteration", p[1], p.lineno)

    def p_step_enumeration(self, p):
        '''step_enumeration :  loop_counter assignment_symbol start_value [ step_value ] [ DOWN ] end_value'''
        p[0] = ("step_enumeration", p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p.lineno)

    def p_loop_counter(self, p):
        '''loop_counter :  identifier'''
        p[0] = ("loop_counter", p[1], p.lineno)

    def p_start_value(self, p):
        '''start_value :  discrete_expression'''
        p[0] = ("start_value", p[1], p.lineno)

    def p_step_value(self, p):
        '''step_value :  BY integer_expression'''
        p[0] = ("step_value", p[1], p[2], p.lineno)

    def p_end_value(self, p):
        '''end_value :  TO discrete_expression'''
        p[0] = ("end_value", p[1], p[2], p.lineno)

    def p_discrete_expression(self, p):
        '''discrete_expression :  expression'''
        p[0] = ("discrete_expression", p[1], p.lineno)

    def p_range_enumeration(self, p):
        '''range_enumeration :  loop_counter [ DOWN ] IN discrete_mode'''
        p[0] = ("range_enumeration", p[1], p[2], p[3], p[4], p[5], p[6], p.lineno)

    def p_while_control(self, p):
        '''while_control :  WHILE boolean_expression'''
        p[0] = ("while_control", p[1], p[2], p.lineno)

    def p_call_action(self, p):
        '''call_action :  procedure_call
            | builtin_call'''
        p[0] = ("call_action", p[1], p.lineno)

    def p_procedure_call(self, p):
        '''procedure_call :  procedure_name ( [ parameter_list ] )'''
        p[0] = ("procedure_call", p[1], p[2], p[3], p[4], p[5], p[6], p.lineno)

    def p_parameter_list(self, p):
        '''parameter_list :  parameter { COMMA parameter }*'''
        p[0] = ("parameter_list", p[1], p[2], p[3], p[4], p[5], p.lineno)

    def p_parameter(self, p):
        '''parameter :  expression'''
        p[0] = ("parameter", p[1], p.lineno)

    def p_procedure_name(self, p):
        '''procedure_name :  identifier'''
        p[0] = ("procedure_name", p[1], p.lineno)

    def p_exit_actiom(self, p):
        '''exit_actiom :  EXIT label_id'''
        p[0] = ("exit_actiom", p[1], p[2], p.lineno)

    def p_return_action(self, p):
        '''return_action :  RETURN [ result ]'''
        p[0] = ("return_action", p[1], p[2], p[3], p[4], p.lineno)

    def p_result_action(self, p):
        '''result_action :  RESULT result'''
        p[0] = ("result_action", p[1], p[2], p.lineno)

    def p_result(self, p):
        '''result :  expression'''
        p[0] = ("result", p[1], p.lineno)

    def p_builtin_call(self, p):
        '''builtin_call :  builtin_name LPAREN [ parameter_list ] RPAREN'''
        p[0] = ("builtin_call", p[1], p[2], p[3], p[4], p[5], p[6], p.lineno)

    def p_builtin_name(self, p):
        '''builtin_name :  ABS
            | ASC
            | NUM
            | UPPER
            | LOWER
            | LENGTH
            | READ
            | PRINT'''
        p[0] = ("builtin_name", p[1], p.lineno)

    def p_procedure_statement(self, p):
        '''procedure_statement :  label_id COLON procedure_definition SEMI'''
        p[0] = ("procedure_statement", p[1], p[2], p[3], p[4], p.lineno)

    def p_procedure_definition(self, p):
        '''procedure_definition :      PROC ( [ formal_parameter_list ] ) [ result_spec ]SEMI     { statement }* END'''
        p[0] = ("procedure_definition", p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p.lineno)

    def p_formal_parameter_list(self, p):
        '''formal_parameter_list :  formal_parameter { , formal_parameter }*'''
        p[0] = ("formal_parameter_list", p[1], p[2], p[3], p[4], p[5], p.lineno)

    def p_formal_parameter(self, p):
        '''formal_parameter :  identifier_list parameter_spec'''
        p[0] = ("formal_parameter", p[1], p[2], p.lineno)

    def p_parameter_spec(self, p):
        '''parameter_spec :  mode [ parameter_attribute ]'''
        p[0] = ("parameter_spec", p[1], p[2], p[3], p[4], p.lineno)

    def p_parameter_attribute(self, p):
        '''parameter_attribute :  LOC'''
        p[0] = ("parameter_attribute", p[1], p.lineno)

    def p_result_spec(self, p):
        '''result_spec :  RETURNS LPAREN mode [ result_attribute ] RPAREN'''
        p[0] = ("result_spec", p[1], p[2], p[3], p[4], p[5], p[6], p[7], p.lineno)

    def p_result_attribute(self, p):
        '''result_attribute :  LOC'''
        p[0] = ("result_attribute", p[1], p.lineno)

    def p_comment(self, p):
        '''comment :  bracketed_comment
            | line_end_comment'''
        p[0] = ("comment", p[1], p.lineno)

    # def p_bracketed_comment(self, p):
    #     '''bracketed_comment :  /* character_string */'''
    #     p[0] = ("bracketed_comment", p[1], p[2], p[3], p.lineno)
    #
    # def p_line_end_comment(self, p):
    #     '''line_end_comment :  // character_string end_of_line'''
    #     p[0] = ("line_end_comment", p[1], p[2], p[3], p.lineno)

    def p_character_string(self, p):
        '''character_string :  { character }*'''
        p[0] = ("character_string", p[1], p[2], p[3], p.lineno)

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



