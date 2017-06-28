from ast import *

class Visitor(NodeVisitor):

    def print(self,node,show_values,tabbing):
        """
        Execute a method of the form print_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        if node:
            method = 'print_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_print)
            return visitor(node,show_values,tabbing)
        else:
            return None

    def generic_print(self,node,show_values,tabbing):
        #if not isinstance(node, AST):
        #    print(node)
        #    return

        #node.print()

        """
        Method executed if no applicable print_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        """
        print(tabbing, node.__class__.__name__)

        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        #item.print()
                        self.print(item,show_values,tabbing + '  ')
            elif isinstance(value, AST):
                #value.print()
                self.print(value, show_values, tabbing + '  ')

    def print_Identifier(self, node, show_values, tabbing):
        print(tabbing, node.__class__.__name__, end='')
        if show_values:
            print(" [ID={}, Type={}, Scope={}, Offset={}]".format(node.ID, node.raw_type, node.scope, node.offset),end='')
        print('')

    def print_Constant_Expression(self, node, show_values, tabbing):
        print(tabbing, node.__class__.__name__, end='')
        if show_values:
            print(" [Type={}, Value={}]".format(node.raw_type, node.value),end='')
        print('')
        self.print(node.expression, show_values, tabbing + '  ')

    def print_Discrete_Range_Mode(self, node, show_values, tabbing):
        print(tabbing, node.__class__.__name__, end='')
        if show_values:
            print(" [Lower Bound={}, Upper Bound={}]".format(node.lower_bound_value, node.upper_bound_value),end='')
        print('')
        self.print(node.identifier, show_values, tabbing + '  ')
        self.print(node.literal_range, show_values, tabbing + '  ')
        self.print(node.discrete_mode, show_values, tabbing + '  ')

    def print_Literal_Range(self, node, show_values, tabbing):
        print(tabbing, node.__class__.__name__, end='')
        if show_values:
            print(" [Lower Bound={}, Upper Bound={}]".format(node.lower_bound_value, node.upper_bound_value),end='')
        print('')
        self.print(node.lower_bound.expression, show_values, tabbing + '  ')
        self.print(node.upper_bound.expression, show_values, tabbing + '  ')

    def print_Array_Mode(self, node, show_values, tabbing):
        print(tabbing, node.__class__.__name__, end='')
        if show_values:
            print(" [Lower Bound={}, Upper Bound={}, Size={}]".format(node.lower_bound_value, node.upper_bound_value, node.size),end='')
        print('')
        self.print(node.index_mode_list, show_values, tabbing + '  ')
        self.print(node.element_mode, show_values, tabbing + '  ')

    def visit_Element_Mode(self, node):
        self.visit(node.mode)
        node.raw_type = node.mode.raw_type

    def visit_Integer_Expression(self, node):
        #print("Integer expression")
        self.visit(node.expression)

        #if isinstance(node.expression, Identifier):
        #    exp_type = node.expression.type[1]
        #else:
        #    exp_type = node.expression.type
        exp_type = node.expression.raw_type

        if (exp_type != 'int'):
            self.print_error(node.lineno, "Expected integer expression, found {}".format(exp_type))
        else:
            node.value = node.expression.value

        node.raw_type = exp_type

    # location

    def visit_Dereferenced_Reference(self, node):
        self.visit(node.location)
        raw_type = None
        if node.location.raw_type is not None and node.location.raw_type[0] == self.ref_symbol:
            raw_type = node.location.raw_type.replace(self.ref_symbol, '', 1)
        else:
            self.print_error(node.lineno, "Attempted to dereference in non-reference element")

        node.raw_type = raw_type
        node.dcl_type = node.location.dcl_type
        node.ID = node.location.ID
        node.loc = node.location.loc

    def visit_Array_Element(self, node):

        self.visit(node.array_location)
        raw_type = None
        if node.array_location.raw_type is not None:
            if node.array_location.raw_type == 'string':
                raw_type = 'char'
            elif node.array_location.raw_type[0] == self.array_symbol:
                raw_type = node.array_location.raw_type.replace(self.array_symbol,'',1)
            else:
                self.print_error(node.lineno, "Attempted subscript in non-array element")

            if not node.expression_list is None:
                for expression in node.expression_list: self.visit(expression)

        node.raw_type = raw_type
        node.dcl_type = node.array_location.dcl_type
        node.ID = node.array_location.ID
        node.loc = node.array_location.loc
        node.lower_bound_value = node.array_location.lower_bound_value
        node.upper_bound_value = node.array_location.upper_bound_value
        #print("ARRAY",node.lower_bound_value, node.upper_bound_value)

    def visit_Array_Slice(self, node):
        self.visit(node.array_location)
        self.visit(node.lower_bound)
        self.visit(node.upper_bound)

        node.raw_type = node.array_location.raw_type
        node.dcl_type = node.array_location.dcl_type
        node.ID = node.array_location.ID
        node.loc = node.array_location.loc

        if (node.lower_bound.raw_type != node.upper_bound.raw_type):
            self.print_error(node.lineno, "Mismatching bound types {} and {} in array slice".format(node.lower_bound.raw_type, node.upper_bound.raw_type))

    def visit_Array_Location(self, node):
        self.visit(node.location)

        node.raw_type = node.location.raw_type
        node.dcl_type = node.location.dcl_type
        node.ID = node.location.ID
        node.loc = node.location.loc
        node.lower_bound_value = 0
        node.upper_bound_value = 0
        if hasattr(node.location, "lower_bound_value"):
            node.lower_bound_value = node.location.lower_bound_value
            node.upper_bound_value = node.location.upper_bound_value

        else:
            self.print_error(node.lineno, "Array must have a lower bound")

    # primitive_value

    # literal

    def visit_Integer_Literal(self, node):
        #self.visit(node.ICONST)
        #print("Integer Literal: " + str(node.value))
        node.raw_type = 'int' #self.typemap["int"]
        node.dcl_type = 'literal'
        node.ID = None
        node.loc = False

    def visit_Boolean_Literal(self, node):
        #self.visit(node.BOOL)
        #print("Boolean Literal: " + str(node.value))
        node.raw_type = 'bool' #self.typemap["bool"]
        node.dcl_type = 'literal'
        node.ID = None
        node.loc = False

    def visit_Character_Literal(self, node):
        #self.visit(node.CCONST)
        #print("Character Literal: " + str(node.value))
        node.raw_type = 'char' #self.typemap["char"]
        node.dcl_type = 'literal'
        node.ID = None
        node.loc = False

    def visit_Empty_Literal(self, node):
        #self.visit(node.NULL)
        #print("Empty literal")
        node.raw_type = 'void' #self.typemap["void"]
        node.dcl_type = 'literal'
        node.ID = None
        node.loc = False

    def visit_Character_String_Literal(self, node):
        #self.visit(node.SCONST)
        #print("Character String Literal: " + str(node.value))
        node.raw_type = 'string' #self.typemap["string"]
        node.dcl_type = 'literal'
        node.ID = None
        node.loc = False
        node.heap_index = len(self.string_literals)
        self.string_literals.append(node.value[1:-1])

    def visit_Value_Array_Element(self, node):
        self.visit(node.array_primitive_value)
        self.visit(node.integer_expression)
        node.raw_type = node.array_primitive_value.raw_type
        node.dcl_type = 'literal'
        node.ID = None
        node.loc = False

    def visit_Value_Array_Slice(self, node):
        self.visit(node.array_primitive_value)
        self.visit(node.lower_bound)
        self.visit(node.upper_bound)
        node.raw_type = node.array_primitive_value.raw_type
        node.dcl_type = 'literal'
        node.ID = None
        node.loc = False

    def visit_Array_Primitive_Value(self, node):
        self.visit(node.primitive_value)
        node.raw_type = node.array_primitive_value.raw_type
        # you don't really need the rest here
        #node.dcl_type = 'literal'
        #node.ID = None
        #node.loc = False

    #def visit_Parenthesized_Expression(self, node):
    #    self.visit(node.expression)

    # expression

    def visit_Conditional_Expression(self, node):
        #print("Conditional expression")
        self.visit(node.boolean_expression)
        self.visit(node.then_expression)
        then_type = node.then_expression.raw_type
        elsif_type = then_type

        if not node.elsif_expression is None:
            self.visit(node.elsif_expression)
            elsif_type = node.elsif_expression.raw_type

        self.visit(node.else_expression)
        else_type = node.else_expression.raw_type

        if not (then_type == elsif_type and elsif_type == else_type):
            aux_msg = "Mismatching types in conditional expression, found {}".format(then_type)
            if not node.elsif_expression is None:
                aux_msg += ", {}".format(elsif_type)
            aux_msg += " and {}".format(else_type)
            self.print_error(node.lineno, aux_msg)
        else:
            if node.boolean_expression.value != None:
                if node.boolean_expression.value:
                    node.value = node.then_expression.value
                elif node.elsif_expression != None:
                    choice = node.elsif_expression.was_chosen
                    if choice != None:
                        if choice:
                            node.value = node.elsif_expression.value
                        else:
                            node.value = node.else_expression.value

        node.raw_type = then_type
        node.dcl_type = 'conditional expression'
        node.ID = None
        node.loc = False


    def visit_Boolean_Expression(self, node):
        #print("Boolean expression")
        self.visit(node.expression)
        exp_type = None
        if node.expression.raw_type != None:
            #if isinstance(node.expression, Identifier):
            #    exp_type = node.expression.type[1]
            #else:
            #    exp_type = node.expression.type
            exp_type = node.expression.raw_type

        if (exp_type != 'bool'):
            self.print_error(node.lineno, "Expected boolean expression, found {}".format(exp_type))
        else:
            node.value = node.expression.value
        node.raw_type = exp_type

    def visit_Then_Expression(self, node):
        #print("Then expression")
        self.visit(node.expression)

        #if isinstance(node.expression, Identifier):
        #    exp_type = node.expression.type[1]
        #else:
        #    exp_type = node.expression.type
        exp_type = node.expression.raw_type
        node.raw_type = exp_type
        node.value = node.expression.value

    def visit_Else_Expression(self, node):
        #print("Else expression")
        self.visit(node.expression)

        #if isinstance(node.expression, Identifier):
        #    exp_type = node.expression.type[1]
        #else:
        #    exp_type = node.expression.type
        exp_type = node.expression.raw_type
        node.raw_type = exp_type
        node.value = node.expression.value

    def visit_Elsif_Expression(self, node):
        #print("Elsif expression")
        node.was_chosen = None
        self.visit(node.boolean_expression)
        self.visit(node.then_expression)
        then_type = node.then_expression.raw_type

        if node.elsif_expression == None:
            if node.boolean_expression.value != None:
                if node.boolean_expression.value:
                    node.value = node.then_expression.value
                    #print("I dont have children and was chosen")
                node.was_chosen = node.boolean_expression.value
                #print("I dont have children and was looked at")
        else:
            self.visit(node.elsif_expression)
            elsif_type = node.elsif_expression.raw_type
            if(then_type != elsif_type):
                self.print_error(node.lineno, "Mismatching types in Elsif expression {} and {}".format(then_type, elsif_type))
            else:
                if node.elsif_expression.was_chosen:
                    #print("my child was chosen, so I was too!!")
                    node.value = node.elsif_expression.value
                    node.was_chosen = True
                elif node.elsif_expression.was_chosen == False:
                    node.was_chosen = node.boolean_expression.value
                    if node.was_chosen:
                        node.value = node.then_expression.value

        node.raw_type = then_type

    def visit_Rel_Mem_Expression(self, node):
        self.visit(node.operand0)
        self.visit(node.operand1)
        # self.visit(node.operator1)
        #print("Relational or Membership operator: " + str(node.operator1))
        node.raw_type = self.raw_type_binary(node, node.operator1, node.operand0, node.operand1)
        if node.operand0.value != None and node.operand1.value != None and not self.semantic_error:
            node.value = self.executeBinaryOperation(node.operand0.value, node.operand1.value, node.operator1, node.lineno)
        node.dcl_type = 'relational expression'
        node.ID = None
        node.loc = False

    # operator1

    # relational_operator

    # membership_operator

    def visit_Binary_Expression(self, node):
        self.visit(node.operand1)
        self.visit(node.operand2)
        #self.visit(node.operator2)
        #print("Binary operator: " + str(node.operator2))
        node.raw_type = self.raw_type_binary(node, node.operator2, node.operand1, node.operand2)
        if node.operand1.value != None and node.operand2.value != None and not self.semantic_error:
            node.value = self.executeBinaryOperation(node.operand1.value, node.operand2.value, node.operator2, node.lineno)
        node.dcl_type = 'binary expression'
        node.ID = None
        node.loc = False

    # operator2

    # arithmetic_additive_operator

    # string_concatenation_operator

    # operand2

    # arithmetic_multiplicative_operator

    def visit_Unary_Expression(self, node):
        #self.visit(node.monadic_operator)
        #print("Monadic operator: " + str(node.monadic_operator))
        self.visit(node.operand4)
        node.raw_type = self.raw_type_unary(node, node.monadic_operator, node.operand4)
        if node.operand4.value != None and not self.semantic_error:
            node.value = self.executeUnaryOperation(node.operand4.value, node.monadic_operator, node.lineno)
        node.dcl_type = 'unary expression'
        node.ID = None
        node.loc = False

    # monadic_operator

    # operand4

    def visit_Referenced_Location(self, node):
        self.visit(node.location)
        node.raw_type = self.ref_symbol + node.location.raw_type
        node.dcl_type = node.location.dcl_type
        node.ID = node.location.ID
        node.loc = node.location.loc

    def visit_Action_Statement(self, node):
        self.visit(node.label_id)
        self.visit(node.action)

    def visit_Label_Id(self, node):
        ident = node.identifier
        aux_type = self.environment.lookup(ident.ID)
        if not aux_type is None:
            self.print_error(node.lineno,
                             "Identifier " + str(ident.ID) + " already declared as {} {}".format(aux_type[0],
                                                                                                 aux_type[1]))
        else:
            self.environment.add_local(ident.ID, ['label',
                                                  'void',
                                                  False,
                                                  0,
                                                  0,
                                                  self.environment.get_current_scope(),
                                                  0])

    # action

    # bracketed_action

    def visit_Assignment_Action(self, node):
        self.visit(node.location)
        self.visit(node.expression)

        #if (hasattr(node.location, "type") and hasattr(node.expression, "type") and (node.location.type != None) and (node.expression.type != None)):
        if(hasattr(node.location, "dcl_type") and hasattr(node.location, "raw_type") and hasattr(node.expression, "raw_type")):
            if node.location.dcl_type is None:
                self.print_error(node.lineno, "Assigning to undefined location")
                return
            if node.location.dcl_type != 'var' and node.location.dcl_type != 'proc':
                self.print_error(node.lineno, "Assignment to unsupported dcl_type {}".format(node.location.dcl_type))
                return
            if node.location.dcl_type == 'proc' and not node.location.loc:
                self.print_error(node.lineno, "Assignment to unsupported dcl_type {}".format(node.location.dcl_type))
                return
            if node.expression.raw_type is None:
                self.print_error(node.lineno, "Assigning from undefined location")
                return

            #if isinstance(node.expression, Identifier):
            #    exp_type = node.expression.type[1]
            #else:
            #    exp_type = node.expression.type
            exp_type = node.expression.raw_type

            if(node.location.raw_type != exp_type):
                self.print_error(node.lineno,
                                 "Mismatched assignment types {} and {}".format(node.location.raw_type, exp_type))

            # self.visit(node.assigning_operator)
            #print("Assigning to {} with operator {}".format(node.location.ID, node.assigning_operator))
            if(node.assigning_operator != self.assign):
                loc_type = self.get_exprType(node.location.raw_type, node.lineno)
                if not (node.assigning_operator in loc_type.closed_dyadic_ops):
                    self.print_error(node.lineno, "Assignment operator {} not supported".format(node.assigning_operator))


        if(not hasattr(node.location, "dcl_type")):
            self.print_error(node.lineno,
                             "Location {} has no dcl_type".format(node.location))
        if (not hasattr(node.location, "raw_type")):
            self.print_error(node.lineno,
                             "Location {} has no type".format(node.location))
        if(not hasattr(node.expression, "raw_type")):
            self.print_error(node.lineno,
                             "Expression {} has no type".format(node.expression))

    # assigning_operator

    # closed_dyadic_operator

    def visit_If_Action(self, node):
        #print("If Action")
        self.visit(node.boolean_expression)

        self.environment.push("IF_ACTION.THEN_CLAUSE")
        self.visit(node.then_clause)
        self.environment.pop()

        if(node.else_clause != None):
            self.environment.push("IF_ACTION.ELSE_CLAUSE")
            self.visit(node.else_clause)
            self.environment.pop()

    def visit_Then_Clause(self, node):
        if not node.action_statement_list is None:
            for action_statement in node.action_statement_list: self.visit(action_statement)

    # action_statement_list

    def visit_Else_Clause(self, node):
        if not node.action_statement_list is None:
            for action_statement in node.action_statement_list: self.visit(action_statement)
        self.visit(node.boolean_expression)
        self.visit(node.then_clause)
        self.visit(node.else_clause)

    def visit_Do_Action(self, node):
        self.environment.push("DO_ACTION")
        self.visit(node.control_part)
        if not node.action_statement_list is None:
            for action_statement in node.action_statement_list: self.visit(action_statement)
        self.environment.pop()

    def visit_Control_Part(self, node):
        self.visit(node.for_control)
        self.visit(node.while_control)

    # for_control
    # iteration

    def visit_Step_Enumeration(self, node):
        self.visit(node.loop_counter)
        self.visit(node.start_value)
        self.visit(node.step_value)
        self.visit(node.end_value)

    def visit_Loop_Counter(self, node):
        self.visit(node.identifier)
        if node.identifier.dcl_type != 'var':
            self.print_error(node.lineno, "Loop counter is not variable.")

    # start_value
    # step_value
    # end_value
    # discrete_expression

    def visit_Range_Enumeration(self, node):
        self.visit(node.loop_counter)
        self.visit(node.discrete_mode)

    def visit_While_Control(self, node):
        self.visit(node.boolean_expression)

    # def visit_Call_Action(self, node):
    #    self.visit(node.label_id)


    #TODO: CHECK IF LOC PARAMETER IS VARIABLE OR PROC WITH LOC RETURN
    #this may be tough, since parameters are expressions

    def visit_Procedure_Call(self, node):
        self.visit(node.identifier)

        # type is a matrix.
        # type[0] is the dcl_type, expected to be 'proc'.
        # type[1] is the raw return type.
        # type[2] is a boolean value representing LOC
        # type[3] is a list of parameters. each parameter is a list by itself:
        # type[3][i][0] is the parameter type.
        # type[3][i][0] is the parameter size im memory.
        # type[3][i][2] is a boolean value representing LOC
        # type[4] is the return offset (in the procedure scope, so it's something like
        ### offset = -2 (this is the base) - total parameter size - return size =~ -3 or lower
        # type[5] is the procedure scope
        # now go forth and conquer the beast!

        type = self.environment.lookup(node.identifier.ID)
        if type is None:
            self.print_error(node.lineno,"Procedure {} not found".format(node.identifier.ID))
            return

        node.dcl_type = type[0]
        node.raw_type = type[1]
        node.ID = node.identifier.ID
        node.loc = node.identifier.loc
        node.offset = node.identifier.offset
        node.scope = node.identifier.scope
        node.return_size = 0
        if type[1] != None:
            node.return_size = 1

        if (type[0] != 'proc'):
            self.print_error(node.lineno, "Expected Procedure call {}, found {} {}".format(node.identifier.ID, type[0], type[1]))
        else:
            parameter_count = 0
            if not node.parameter_list is None:
                parameter_count = len(node.parameter_list)
            expected_count = len(type[3])
            if (parameter_count != expected_count):
                self.print_error(node.lineno, "Incorrect parameter count at Procedure {}; Expected {}, found {}".format(node.identifier.ID, expected_count, parameter_count))
            elif not node.parameter_list is None:
                for i, param in enumerate(node.parameter_list, start=0):
                    self.visit(param)
                    param.is_reference = False
                    if (param.raw_type != type[3][i][0]):
                        self.print_error(node.lineno,
                                         "Incorrect parameter type at position i={}; Expected {}, found {}".format(
                                             i, type[3][i][0], param.raw_type))
                    elif type[3][i][2]:
                        if param.dcl_type != 'var' and param.dcl_type != 'proc':
                            self.print_error(node.lineno,
                                         "Expected location at position i={}; Found {} instead".format(
                                             i, param.dcl_type))
                        elif param.dcl_type == 'proc' and not param.loc:
                            self.print_error(node.lineno,
                                         "Expected location at position i={}; Found {} instead".format(
                                             i, param.dcl_type))
                        else:
                            param.is_reference = True



    # parameter_list

    def visit_Parameter(self, node):
        self.visit(node.expression)
        node.raw_type = node.expression.raw_type
        node.dcl_type = node.expression.dcl_type
        node.ID = node.expression.ID
        node.loc = node.expression.loc
        #print(node.ID)

    def visit_Exit_Action(self, node):
        self.visit(node.exit_label_id)

    def visit_Exit_Label_ID(self, node):
        node.type = self.environment.lookup(node.ID)
        node.raw_type = None
        node.dcl_type = None
        node.loc = False
        node.offset = 0
        node.scope = 0
        if(node.type != None):
            #print("Identifier: ID \"" + str(node.ID) + "\" type \"{} {}\"".format(node.type[0], node.type[1]))
            node.dcl_type = node.type[0]
            node.raw_type = node.type[1]
            node.loc = node.type[2]
            if node.raw_type != 'lbl':
                self.print_error(node.lineno,
            "Label {} was not defined".format(node.ID))


    def visit_Return_Action(self, node):

        self.environment.procedure_has_returns_stack[-1] = True
        node.scope = self.environment.procedure_scope_stack[-1]
        node.parameter_space = self.environment.parameter_space_stack[-1]
        node.offset = self.environment.procedure_offset_stack[-1]
        node.loc = False

        found_type = 'void'

        if not node.result is None:
            self.visit(node.result)
            found_type = node.result.raw_type

        if self.environment.expected_return_stack[-1] is None:
            if not found_type is None:
                self.print_error(node.lineno, "Expected void return, found {}".format(found_type))
        else:
            node.loc = self.environment.expected_return_stack[-1].loc
            if (found_type != self.environment.expected_return_stack[-1].mode.raw_type):
                self.print_error(node.lineno, "Expected {} return, found {}".format(self.environment.expected_return_stack[-1].mode.raw_type, found_type))

    def visit_Result_Action(self, node):
        self.environment.procedure_has_returns_stack[-1] = True
        node.scope = self.environment.procedure_scope_stack[-1]
        node.parameter_space = self.environment.parameter_space_stack[-1]
        node.offset = self.environment.procedure_offset_stack[-1]
        node.loc = self.environment.expected_return_stack[-1].loc

        self.visit(node.result)
        found_type = node.result.raw_type

        if self.environment.expected_return_stack[-1] is None:
            self.print_error(node.lineno, "Expected void result, found {}".format(found_type))
        else:
            if (found_type != self.environment.expected_return_stack[-1].mode.raw_type):
                self.print_error(node.lineno, "Expected {} result, found {}".format(self.environment.expected_return_stack[-1].mode.raw_type, found_type))


    # def visit_Result(self, node):
    #    self.visit(node.expression)

    def visit_Builtin_Call(self, node):
        #node.identifier = Identifier(node.builtin_name.name)
        #self.visit_Procedure_Call(node)

        self.visit(node.builtin_name)
        if not node.parameter_list is None:
            for param in node.parameter_list: self.visit(param)

        node.raw_type = 'void'
        node.dcl_type = 'proc'
        node.ID = node.builtin_name.name
        node.loc = False

        if node.ID in ['asc','lower','upper']:
            node.raw_type = 'char'
        elif node.ID in ['num', 'abs','length']:
            node.raw_type = 'int'

    # TODO: LIST OF PARAMETERS FOR BUILTIN NAMES
    def visit_Builtin_Name(self, node):
        #print("Builtin Name: " + str(node.name))
        return


    def visit_Procedure_Statement(self, node):
        proc_name = node.label_id.identifier.ID
        self.environment.push('PROCEDURE DECLARATION '+ proc_name)
        self.visit(node.procedure_definition)
        self.environment.pop()

        self.environment.parameter_space_stack.pop()
        self.environment.procedure_scope_stack.pop()
        self.environment.procedure_offset_stack.pop()

        node.scope = node.procedure_definition.scope

    def visit_Procedure_Definition(self, node):
        self.visit(node.formal_procedure_head)
        node.scope = node.formal_procedure_head.scope
        node.parameter_space = node.formal_procedure_head.parameter_space

        self.environment.parameter_space_stack.append(node.parameter_space)
        self.environment.procedure_scope_stack.append(node.scope)
        self.environment.procedure_offset_stack.append(node.formal_procedure_head.offset)

        self.environment.expected_return_stack.append(node.formal_procedure_head.result_spec)

        if not node.statement_list is None:
            for statement in node.statement_list:
                self.visit(statement)

        if not self.environment.procedure_has_returns_stack[-1] and self.environment.expected_return_stack[-1] is not None:
            proc_name = self.environment.peek().return_type().replace("PROCEDURE DECLARATION ", "")
            self.print_error(node.lineno, "Procedure {} has no return".format(proc_name))

        self.environment.expected_return_stack.pop()

    def visit_Formal_Procedure_Head(self, node):
        node.param_types = []
        node.scope = self.environment.get_current_scope()
        self.environment.offset = -2
        node.offset = -2
        if not node.formal_parameter_list is None:
            for formal_param in node.formal_parameter_list:
                self.visit(formal_param)
                node.param_types += formal_param.param_list

        param_list = node.param_types
        if node.result_spec is None:
            result_type = 'void'
            result_loc = False
        else:
            self.visit(node.result_spec)
            result_type = node.result_spec.mode.raw_type
            result_loc = node.result_spec.loc
            node.offset = self.environment.offset - node.result_spec.mode.size

        node.parameter_space = (-2) - self.environment.offset

        proc_name = self.environment.peek().return_type().replace("PROCEDURE DECLARATION ","")
        #print("Procedure declaration: {}".format(proc_name))

        aux_type = self.environment.lookup(proc_name)
        if not aux_type is None:
            self.print_error(node.lineno,
                             "Identifier " + str(proc_name) + " already declared as {} {}".format(aux_type[0],
                                                                                                  aux_type[1]))
        else:
            self.environment.add_parent(proc_name, ['proc',
                                                    result_type,
                                                    result_loc,
                                                    node.param_types,
                                                    node.offset,
                                                    node.scope])
        node.raw_type = result_type
        node.loc = result_loc
        self.environment.offset = 0

    # formal_parameter_list

    def visit_Formal_Parameter(self, node):

        self.visit(node.parameter_spec)
        node.mode = node.parameter_spec.mode
        node.raw_type = node.mode.raw_type
        node.loc = node.parameter_spec.loc
        node.param_list = []

        if not node.identifier_list is None:
            for ident in node.identifier_list:

                #print(ident.ID, node.loc)
                aux_type = self.environment.lookup(ident.ID)

                if not aux_type is None and aux_type[0] == 'var' and aux_type[5] == self.environment.get_current_scope():
                            self.print_error(node.lineno,
                                     "Identifier " + str(ident.ID) + " already declared as {} {}".format(aux_type[0],aux_type[1]))
                else:
                    self.environment.offset -= 1 #node.mode.size
                    offset = self.environment.offset
                    self.environment.add_local(ident.ID, ['var',
                                                          node.mode.raw_type,
                                                          node.loc,
                                                          node.mode.size,
                                                          offset,
                                                          self.environment.get_current_scope(),
                                                          node.mode.upper_bound_value,
                                                          node.mode.lower_bound_value])
                    node.param_list.append([node.raw_type, node.mode.size, node.loc])

    def visit_Parameter_Spec(self, node):
        self.visit(node.mode)

        #if (node.loc != None):
        #    node.mode.dcl_type = self.loc_symbol + node.mode.dcl_type
    # parameter_attribute

    def visit_Result_Spec(self, node):
        self.visit(node.mode)
        #if (node.loc != None):
        #    node.mode.dcl_type = self.loc_symbol + node.mode.dcl_type
