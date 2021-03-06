# Yacc example
import ply.yacc as yacc

from lya_vm import VirtualMachine

from ast import *
from semantic import *

# Get the token map from the lexer.  This is required.
import lexer as lex

class Parser:

    def __init__(self):
        self.lexer = lex.Lexer()
        self.tokens = self.lexer.tokens
        self.build()

    def build(self):
        self.parser = yacc.yacc(module=self, start='program')

    def p_program(self, p):
        'program : statement_list'

        p[0] = Program(p[1], lineno = p[1][0].lineno)

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

        p[0] = p[1]

    def p_declaration_statement(self,p):
        'declaration_statement : DCL declaration_list SEMI'

        p[0] = Declaration_Statement(p[2], lineno = p[2][0].lineno)

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
            p[0] = Declaration(p[1], p[2], None, lineno = p[1][0].lineno)
        elif (len(p) == 4):
            p[0] = Declaration(p[1], p[2], p[3], lineno = p[1][0].lineno)

    def p_initialization(self,p):
        'initialization : ASSIGN expression'

        p[0] = p[2]

    def p_identifier_list(self, p):
        '''identifier_list : identifier
                           | identifier_list COMMA identifier'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 4):
            p[0] = p[1] + [p[3]]

    def p_identifier(self,p):
        'identifier : ID'

        p[0] = Identifier(p[1], lineno = p.lineno(1))

    def p_synonym_statement(self, p):
        'synonym_statement : SYN synonym_list SEMI'

        p[0] = Synonym_Statement(p[2], lineno = p.lineno(1))

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
            p[0] = Synonym_Definition(p[1], None, p[3], lineno = p[1][0].lineno)
        elif (len(p) == 5):
            p[0] = Synonym_Definition(p[1], p[2], p[4], lineno = p[1][0].lineno)

    def p_constant_expression(self, p):
        'constant_expression : expression'

        p[0] = Constant_Expression(p[1], lineno = p[1].lineno)

    def p_newmode_statement(self, p):
        'newmode_statement : TYPE newmode_list SEMI'

        p[0] = Newmode_Statement(p[2], lineno = p.lineno(1))

    def p_newmode_list(self, p):
        '''newmode_list : mode_definition
                        | newmode_list COMMA mode_definition'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 4):
            p[0] = p[1] + [p[3]]

    def p_mode_definition(self, p):
        'mode_definition : identifier_list ASSIGN mode'

        p[0] = Mode_Definition(p[1], p[3], lineno = p[1][0].lineno)

    def p_mode(self, p):
        '''mode : mode_name
                | discrete_mode
                | reference_mode
                | composite_mode'''

        p[0] = p[1]

    def p_discrete_mode(self, p):
        '''discrete_mode : integer_mode
                | boolean_mode
                | character_mode
                | discrete_range_mode'''

        p[0] = p[1]

    def p_integer_mode(self, p):
        '''integer_mode : INT'''

        p[0] = Integer_Mode(p[1], lineno = p.lineno(1))

    def p_boolean_mode(self, p):
        '''boolean_mode : BOOL'''

        p[0] = Boolean_Mode(p[1], lineno = p.lineno(1))

    def p_character_mode(self, p):
        '''character_mode : CHAR'''

        p[0] = Character_Mode(p[1], lineno = p.lineno(1))

    def p_discrete_range_mode(self, p):
        '''discrete_range_mode : identifier LPAREN literal_range RPAREN
                               | discrete_mode LPAREN literal_range RPAREN '''
        if isinstance(p[1], Identifier):
            p[0] = Discrete_Range_Mode(p[1], p[3], None, lineno = p[1].lineno)
        else:
            p[0] = Discrete_Range_Mode(None, p[3], p[1], lineno = p[1].lineno)

    def p_mode_name(self, p):
        '''mode_name : identifier'''

        p[0] = Mode_Name(p[1], lineno = p[1].lineno)

    def p_literal_range(self, p):
        '''literal_range : lower_bound COLON upper_bound'''

        p[0] = Literal_Range(p[1], p[3], lineno = p[1].lineno)

    def p_lower_bound(self, p):
        '''lower_bound : expression'''

        p[0] = Lower_Bound(p[1], lineno = p[1].lineno)

    def p_upper_bound(self, p):
        '''upper_bound : expression'''

        p[0] = Upper_Bound(p[1], lineno = p[1].lineno)

    def p_reference_mode(self, p):
        '''reference_mode : REF mode'''

        p[0] = Reference_Mode(p[2], lineno = p.lineno(1))

    def p_composite_mode(self, p):
        '''composite_mode : string_mode
                          | array_mode'''

        p[0] = p[1]

    def p_string_mode(self, p):
        '''string_mode : CHARS LBRACKET ICONST RBRACKET'''

        p[0] = String_Mode(p[3], lineno = p.lineno(1))

    def p_array_mode(self, p):
        '''array_mode : ARRAY LBRACKET index_mode_list RBRACKET element_mode'''

        p[0] = Array_Mode(p[3], p[5], lineno = p.lineno(1))

    def p_index_mode_list(self, p):
        '''index_mode_list : index_mode
                           | index_mode_list COMMA index_mode'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 4):
            p[0] = p[1] + [p[3]]

    def p_index_mode(self, p):
        '''index_mode : discrete_mode
                      | literal_range'''

        p[0] = p[1]

    def p_element_mode(self, p):
        '''element_mode : mode'''

        p[0] = p[1]

    def p_integer_expression(self, p):
        '''integer_expression : expression'''

        p[0] = Integer_Expression(p[1], lineno = p[1].lineno)

    def p_location(self, p):
        '''location : identifier
                    | dereferenced_reference
                    | array_element
                    | array_slice
                    | call_action '''

        #Removing the following because they can be resolved semantically
        #| string_element
        #| string_slice

        p[0] = p[1]

    def p_dereferenced_reference(self, p):
        '''dereferenced_reference : location ARROW'''

        p[0] = Dereferenced_Reference(p[1], lineno = p[1].lineno)

    def p_array_element(self, p):
        '''array_element : array_location LBRACKET expression_list RBRACKET'''

        p[0] = Array_Element(p[1], p[3], lineno = p[1].lineno)

    def p_expression_list(self, p):
        '''expression_list : expression
                           | expression_list COMMA expression'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 4):
            p[0] = p[1] + [p[3]]

    def p_array_slice(self, p):
        '''array_slice : array_location LBRACKET lower_bound COLON upper_bound RBRACKET'''

        p[0] = Array_Slice(p[1], p[3], p[5], lineno = p[1].lineno)

    def p_array_location(self, p):
        '''array_location : location'''

        p[0] = Array_Location(p[1], lineno = p[1].lineno)

    def p_primitive_value(self, p):
        '''primitive_value : literal
                           | value_array_element
                           | value_array_slice
                           | parenthesized_expression '''

        p[0] = p[1]


    def p_literal(self, p):
        '''literal : integer_literal
                   | boolean_literal
                   | character_literal
                   | empty_literal
                   | character_string_literal '''

        p[0] = p[1]

    def p_integer_literal(self, p):
        '''integer_literal : ICONST'''

        p[0] = Integer_Literal(p[1], lineno = p.lineno(1))

    def p_boolean_literal(self, p):
        '''boolean_literal : FALSE
                           | TRUE'''

        p[0] = Boolean_Literal(p[1], lineno = p.lineno(1))

    def p_character_literal(self, p):
        '''character_literal : CCONST '''

        p[0] = Character_Literal(p[1], lineno = p.lineno(1))

    def p_empty_literal(self, p):
        '''empty_literal : NULL'''

        p[0] = Empty_Literal(p[1], lineno = p.lineno(1))

    def p_character_string_literal(self, p):
        '''character_string_literal : SCONST'''

        p[0] = Character_String_Literal(p[1], lineno = p.lineno(1))

    def p_value_array_element(self, p):
        '''value_array_element : array_primitive_value LBRACKET integer_expression RBRACKET'''

        p[0] = Value_Array_Element(p[1], p[3], lineno = p[1].lineno)

    def p_value_array_slice(self, p):
        '''value_array_slice : array_primitive_value LBRACKET lower_bound COLON upper_bound RBRACKET'''

        p[0] = Value_Array_Slice(p[1], p[3], p[5], lineno = p[1].lineno)

    def p_array_primitive_value(self, p):
        '''array_primitive_value : primitive_value'''

        p[0] = Array_Primitive_Value(p[1], lineno = p[1].lineno)

    def p_parenthesized_expression(self, p):
        '''parenthesized_expression : LPAREN expression RPAREN'''

        p[0] = p[2]

    def p_expression(self, p):
        '''expression : operand0
                      | conditional_expression'''

        p[0] = p[1]

    def p_conditional_expression(self, p):
        '''conditional_expression : IF boolean_expression then_expression else_expression FI
                                  | IF boolean_expression then_expression elsif_expression else_expression FI '''
        if (len(p) == 6):
            p[0] = Conditional_Expression(p[2], p[3], None, p[4], lineno = p.lineno(1))
        elif (len(p) == 7):
            p[0] = Conditional_Expression(p[2], p[3], p[4], p[5], lineno = p.lineno(1))

    def p_boolean_expression(self, p):
        '''boolean_expression : expression'''

        p[0] = Boolean_Expression(p[1], lineno = p[1].lineno)

    def p_then_expression(self, p):
        '''then_expression : THEN expression'''

        p[0] = Then_Expression(p[2], lineno = p.lineno(1))

    def p_else_expression(self, p):
        '''else_expression : ELSE expression'''

        p[0] = Else_Expression(p[2], lineno = p.lineno(1))

    def p_elsif_expression(self, p):
        '''elsif_expression : ELSIF boolean_expression then_expression
                            | elsif_expression ELSIF boolean_expression then_expression '''
        if(len(p) == 4):
            p[0] = Elsif_Expression(None, p[2], p[3], lineno = p.lineno(1))
        elif(len(p) == 5):
            p[0] = Elsif_Expression(p[1], p[3], p[4], lineno = p[1].lineno)

    def p_operand0(self, p):
        '''operand0 :  operand1
            | operand0 operator1 operand1'''
        if(len(p) == 2):
            p[0] = p[1]
        elif(len(p) == 4):
            p[0] = Rel_Mem_Expression(p[1], p[2], p[3], lineno = p[1].lineno)

    def p_operator1(self, p):
        '''operator1 :  relational_operator
            | membership_operator'''
        p[0] = p[1]

    def p_relational_operator(self, p):
        '''relational_operator :  AND
            | OR
            | EQUAL
            | DIFF
            | GREATER
            | GREATEREQ
            | LESS
            | LESSEQ'''

        p[0] = p[1]

    def p_membership_operator(self, p):
        '''membership_operator :  IN'''

        p[0] = p[1]

    def p_operand1(self, p):
        '''operand1 :  operand2
            | operand1 operator2 operand2'''
        if(len(p) == 2):
            p[0] = p[1]
        elif(len(p) == 4):
            p[0] = Binary_Expression(p[1], p[2], p[3], lineno = p[1].lineno)

    def p_operator2(self, p):
        '''operator2 :  arithmetic_additive_operator
                     | string_concatenation_operator'''
        p[0] = p[1]

    def p_arithmetic_additive_operator(self, p):
        '''arithmetic_additive_operator :  PLUS
            | MINUS'''

        p[0] = p[1]

    def p_string_concatenation_operator(self, p):
        '''string_concatenation_operator :  STRCAT'''
        p[0] = p[1]

    def p_operand2(self, p):
        '''operand2 :  operand3
            | operand2 arithmetic_multiplicative_operator operand3'''
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 4):
            p[0] = Binary_Expression(p[1], p[2], p[3], lineno = p[1].lineno)

    def p_arithmetic_multiplicative_operator(self, p):
        '''arithmetic_multiplicative_operator :  TIMES
            | DIVIDE
            | MOD'''

        p[0] = p[1]

    def p_operand3(self, p):
        '''operand3 : operand4
            | monadic_operator operand4'''
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 3):
            p[0] = Unary_Expression(p[1], p[2], lineno = p[2].lineno)

    def p_monadic_operator(self, p):
        '''monadic_operator :  MINUS
            | NOT'''

        p[0] = p[1]

    def p_operand4(self, p):
        '''operand4 :  location
            | referenced_location
            | primitive_value'''

        p[0] = p[1]

    def p_referenced_location(self, p):
        '''referenced_location :  ARROW location'''

        p[0] = Referenced_Location(p[2], lineno = p.lineno(1))

    def p_action_statement(self, p):
        '''action_statement :  action SEMI
            | label_id COLON action SEMI'''
        if (len(p) == 3):
            p[0] = Action_Statement(None, p[1], lineno = p[1].lineno)
        elif (len(p) == 5):
            p[0] = Action_Statement(p[1], p[3], lineno = p[1].lineno)

    def p_label_id(self, p):
        '''label_id :  identifier'''

        p[0] = Label_Id(p[1], lineno = p[1].lineno)

    def p_action(self, p):
        '''action :  bracketed_action
            | assignment_action
            | call_action
            | exit_action
            | return_action
            | result_action'''

        p[0] = p[1]

    def p_bracketed_action(self, p):
        '''bracketed_action :  if_action
            | do_action'''

        p[0] = p[1]

    def p_assignment_action(self, p):
        '''assignment_action :  location assigning_operator expression'''

        p[0] = Assignment_Action(p[1], p[2], p[3], lineno = p[1].lineno)

    def p_assigning_operator(self, p):
        '''assigning_operator : ASSIGN
                              | closed_dyadic_operator'''

        p[0] = p[1]

    def p_closed_dyadic_operator(self, p):
        '''closed_dyadic_operator : INCREASE
                                  | DECREASE
                                  | MULCREASE
                                  | DIVCREASE
                                  | MODCREASE'''

        p[0] = p[1]

    def p_if_action(self, p):
        '''if_action :  IF boolean_expression then_clause FI
                     | IF boolean_expression then_clause else_clause FI'''
        if (len(p) == 5):
            p[0] = If_Action(p[2], p[3], None, lineno = p.lineno(1))
        elif (len(p) == 6):
            p[0] = If_Action(p[2], p[3], p[4], lineno = p.lineno(1))

    def p_then_clause(self, p):
        '''then_clause :  THEN
                       |  THEN action_statement_list'''
        if (len(p) == 2):
            p[0] = Then_Clause(None, lineno = p.lineno(1))
        elif (len(p) == 3):
            p[0] = Then_Clause(p[2], lineno = p.lineno(1))

    def p_action_statement_list(self, p):
        '''action_statement_list : action_statement
                                 | action_statement_list action_statement'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 3):
            p[0] = p[1] + [p[2]]

    def p_else_clause(self, p):
        '''else_clause :  ELSE
                        | ELSE action_statement_list
                        | ELSIF boolean_expression then_clause
                        | ELSIF boolean_expression then_clause else_clause '''
        if (len(p) == 2):
            p[0] = Else_Clause(None, None, None, None, lineno = p.lineno(1))
        elif (len(p) == 3):
            p[0] = Else_Clause(p[2], None, None, None, lineno = p.lineno(1))
        elif (len(p) == 4):
            p[0] = Else_Clause(None, p[2], p[3], None, lineno = p.lineno(1))
        elif (len(p) == 5):
            p[0] = Else_Clause(None, p[2], p[3], p[4], lineno = p.lineno(1))

    def p_do_action(self, p):
        '''do_action :  DO OD
                     |  DO control_part SEMI OD
                     |  DO action_statement_list OD
                     |  DO control_part SEMI action_statement_list OD'''
        if (len(p) == 3):
            p[0] = Do_Action(None, None, lineno = p.lineno(1))
        elif (len(p) == 5):
            p[0] = Do_Action(p[2], None, lineno = p.lineno(1))
        elif(len(p) == 4):
            p[0] = Do_Action(None, p[2], lineno = p.lineno(1))
        elif (len(p) == 6):
            p[0] = Do_Action(p[2], p[4], lineno = p.lineno(1))

    def p_control_part(self, p):
        '''control_part : while_control
                        | FOR for_control
                        | FOR for_control while_control'''
        if (len(p) == 2):
            p[0] = Control_Part(None, p[1], lineno = p[1].lineno)
        elif (len(p) == 3):
            p[0] = Control_Part(p[2], None, lineno = p.lineno(1))
        elif (len(p) == 4):
            p[0] = Control_Part(p[2], p[3], lineno = p.lineno(1))

    def p_for_control(self, p):
        '''for_control : iteration'''
        p[0] = For_Control(p[1], lineno = p[1].lineno)

    def p_iteration(self, p):
        '''iteration : step_enumeration
                     | range_enumeration'''
        p[0] = p[1]

    def p_step_enumeration(self, p):
        '''step_enumeration : loop_counter ASSIGN start_value end_value
                            | loop_counter ASSIGN start_value step_value end_value'''
        if (len(p) == 5):
            p[0] = Step_Enumeration(p[1], p[3], None, p[4], lineno = p[1].lineno)
        elif (len(p) == 6):
            p[0] = Step_Enumeration(p[1], p[3], p[4], p[5], lineno = p[1].lineno)

    def p_loop_counter(self, p):
        '''loop_counter :  identifier'''
        p[0] = Loop_Counter(p[1], lineno = p[1].lineno)

    def p_start_value(self, p):
        '''start_value :  discrete_expression'''
        p[0] = p[1]

    def p_step_value(self, p):
        '''step_value :  BY integer_expression'''
        p[0] = p[2]

    def p_end_value(self, p):
        '''end_value : TO discrete_expression
                     | DOWN TO discrete_expression'''
        if (len(p) == 3):
            p[0] = p[2]
        elif(len(p) == 4):
            p[0] = p[3]

    def p_discrete_expression(self, p):
        '''discrete_expression : expression'''
        p[0] = p[1]

    def p_range_enumeration(self, p):
        '''range_enumeration : loop_counter IN discrete_mode
                             | loop_counter DOWN IN discrete_mode'''
        if (len(p) == 4):
            p[0] = Range_Enumeration(p[1], p[3], lineno = p[1].lineno)
        elif (len(p) == 5):
            p[0] = Range_Enumeration(p[1], p[4], lineno = p[1].lineno)

    def p_while_control(self, p):
        '''while_control :  WHILE boolean_expression'''
        p[0] = While_Control(p[2], lineno = p.lineno(1))

    def p_call_action(self, p):
        '''call_action :  procedure_call
                        | builtin_call'''
        p[0] = p[1]

    def p_procedure_call(self, p):
        '''procedure_call : identifier LPAREN RPAREN
                          | identifier LPAREN parameter_list RPAREN'''
        if (len(p) == 4):
            p[0] = Procedure_Call(p[1], None, lineno = p[1].lineno)
        elif (len(p) == 5):
            p[0] = Procedure_Call(p[1], p[3], lineno = p[1].lineno)

    def p_parameter_list(self, p):
        '''parameter_list :  parameter
                          |  parameter_list COMMA parameter'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 4):
            p[0] = p[1] + [p[3]]

    def p_parameter(self, p):
        '''parameter :  expression'''
        p[0] = Parameter(p[1], lineno = p[1].lineno)





    def p_exit_action(self, p):
        '''exit_action :  EXIT exit_label_id'''
        p[0] = Exit_Action(p[2], lineno = p.lineno(1))

    def p_exit_label_id(self, p):
        '''exit_label_id :  identifier'''
        p[0] = Exit_Label_Id(p[1], lineno = p[1].lineno)

    def p_return_action(self, p):
        '''return_action :  RETURN
                         |  RETURN result'''
        if (len(p) == 2):
            p[0] = Return_Action(None, lineno = p.lineno(1))
        elif (len(p) == 3):
            p[0] = Return_Action(p[2], lineno = p.lineno(1))

    def p_result_action(self, p):
        '''result_action :  RESULT result'''
        p[0] = Result_Action(p[2], lineno = p.lineno(1))

    def p_result(self, p):
        '''result :  expression'''
        p[0] = p[1]

    def p_builtin_call(self, p):
        '''builtin_call : builtin_name LPAREN RPAREN
                        | builtin_name LPAREN parameter_list RPAREN'''
        if (len(p) == 4):
            p[0] = Builtin_Call(p[1], None, lineno = p[1].lineno)
        elif (len(p) == 5):
            p[0] = Builtin_Call(p[1], p[3], lineno = p[1].lineno)

    def p_builtin_name(self, p):
        '''builtin_name : ABS
                        | ASC
                        | NUM
                        | UPPER
                        | LOWER
                        | LENGTH
                        | READ
                        | PRINT'''
        p[0] = Builtin_Name(p[1], lineno = p.lineno(1))

    def p_procedure_statement(self, p):
        '''procedure_statement :  label_id COLON procedure_definition SEMI'''
        p[0] = Procedure_Statement(p[1], p[3], lineno = p[1].lineno)

    def p_procedure_definition(self, p):
        '''procedure_definition :  formal_procedure_head END
                                |  formal_procedure_head statement_list END'''
        if (len(p) == 3):
            p[0] = Procedure_Definition(p[1], None, lineno = p[1].lineno)
        elif (len(p) == 4):
            p[0] = Procedure_Definition(p[1], p[2], lineno = p[1].lineno)

    def p_formal_procedure_head(self, p):
        '''formal_procedure_head : PROC parenthesis_gambiarra SEMI
                                 | PROC parenthesis_gambiarra result_spec SEMI'''
        if (len(p) == 4):
            p[0] = Formal_Procedure_Head(p[2], None, lineno = p.lineno(1))
        elif (len(p) == 5):
            p[0] = Formal_Procedure_Head(p[2], p[3], lineno = p.lineno(1))


    def p_parenthesis_gambiarra(self, p):
        '''parenthesis_gambiarra : LPAREN RPAREN
                                 | LPAREN formal_parameter_list RPAREN'''
        if (len(p) == 3):
            p[0] = None
        elif (len(p) == 4):
            p[0] = p[2]

    def p_formal_parameter_list(self, p):
        '''formal_parameter_list :  formal_parameter
                                 |  formal_parameter_list COMMA formal_parameter'''
        if (len(p) == 2):
            p[0] = [p[1]]
        elif (len(p) == 4):
            p[0] = p[1] + [p[3]]

    def p_formal_parameter(self, p):
        '''formal_parameter :  identifier_list parameter_spec'''
        p[0] = Formal_Parameter(p[1], p[2], lineno = p[1][0].lineno)

    def p_parameter_spec(self, p):
        '''parameter_spec :  mode
                          |  mode LOC'''
        if(len(p) == 2):
            p[0] = Parameter_Spec(p[1], False, lineno = p[1].lineno)
        elif(len(p) == 3):
            p[0] = Parameter_Spec(p[1], True, lineno = p[1].lineno)

    def p_result_spec(self, p):
        '''result_spec  :  RETURNS LPAREN mode RPAREN
                        |  RETURNS LPAREN mode LOC RPAREN'''
        if(len(p) == 5):
            p[0] = Result_Spec(p[3], False, lineno = p.lineno(1))
        elif(len(p) == 6):
            p[0] = Result_Spec(p[3], True, lineno = p.lineno(1))

    def p_error(self,p):
        print("Syntax error in input! Found unknown " + str(p))

    def parse(self, text):
        return self.parser.parse(text, self.lexer)

# Build the parser
counter = 1
while counter > 0:
    counter -= 1
    try:
        s = "dcl m,n,s int; "\
            "syn k = \"hello\"; "\
            "read(m,n); "\
            "s = 0; "\
            "do while m <= n; "\
            "s += m * n; "\
            "print(m,s); "\
            "m += 1; "\
            "od; "

        s = "/* Bubble sort code: */ "\
        "dcl n, c, d, swap int; "\
        "print(\"Enter number of elements: \"); "\
        "read(n); "\
        "print(\"Enter \", n, \" integers\\n\"); "\
        "do "\
        "for c = 0 to n - 1; "\
        "read(v[c]); "\
        "od; "\
        "do "\
        "for c = 0 to n-2; "\
        "do "\
        "for d = 0 to n-c-2; "\
        "if v[d] > v[d + 1] then "\
        "swap = v[d]; "\
        "v[d] =  v[d + 1]; "\
        "v[d + 1] = swap; "\
        "fi; "\
        "od; "\
        "od; "\
        "print(\"Sorted list in ascending order:\\n\"); "\
        "do "\
        "for c = 0 to n - 1; "\
        "print(v[c], \" \"); "\
        "od;"

        s = "dcl v array[0:100] int;"

    except EOFError:
        break
