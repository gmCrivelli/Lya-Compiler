import sys
import lexer
from ast import *

debug = False

class SymbolTable(dict):
    """
    Class representing a symbol table. It should
    provide functionality for adding and looking
    up nodes associated with identifiers.
    """
    def __init__(self, decl=None):
        super().__init__()
        self.decl = decl
    def add(self, name, value):
        self[name] = value
    def lookup(self, name):
        return self.get(name, None)
    def return_type(self):
        if self.decl:
            #return self.decl.mode
            return self.decl
        return None


class ExprType(object):
    def __init__(self, type, unary_ops, binary_ops, closed_dyadic_ops, default_value):
        super().__init__()
        self.type = type
        self.unary_ops = unary_ops
        self.binary_ops = binary_ops
        self.closed_dyadic_ops = closed_dyadic_ops
        self.default_value = default_value

    def __str__(self):
        return self.type

relational_ops = ["!=", "==", ">", ">=", "<", "<="]
membership_ops = ["in"]

int_type = ExprType("int",["-"],["+", "-", "*", "/", "%", "!=", "==", ">", ">=", "<", "<="],['+=','-=','*=','/=','%='],0)
bool_type = ExprType("bool",["!"],["==", "!="],[],False)
char_type = ExprType("char",[],[],[],"")
string_type = ExprType("string",[],["+", "==", "!="],['+='],"")
void_type = ExprType("void",[],[],[],"")

class Environment(object):
    def __init__(self):
        self.stack = []
        self.root = SymbolTable()
        self.stack.append(self.root)
        self.root.update({
            "int": int_type,
            "char": char_type,
            "string": string_type,
            "bool": bool_type

            #TODO: implement structure for built-in calls
            # Remember that parameters and returns may vary
            #"abs": ['proc', 'int', ['int']],
            #"asc": ['proc', 'int', ['char' OR 'string']],
            #"num": ['proc', 'int' OR 'bool, ['string']],
            #"upper": ['proc', 'string' OR 'char', ['string' OR 'char']],
            #"lower": ['proc', 'string' OR 'char', ['string' OR 'char']],
            #"length": ['proc', 'int', ['string' OR array?]],
            #"read": ['proc', 'void', [ MULTIPLE VARIABLES ]],
            #"print": ['proc', 'void', ['string']]
        })
    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))
    def pop(self):
        self.stack.pop()
    def peek(self):
        return self.stack[-1]
    def parent_scope(self):
        return self.stack[-2]
    def scope_level(self):
        return len(self.stack)
    def add_local(self, name, value):
        self.peek().add(name, value)
    def add_parent(self, name, value):
        self.parent_scope().add(name, value)
    def add_root(self, name, value):
        self.root.add(name, value)
    def lookup(self, name):
        for scope in reversed(self.stack):
            hit = scope.lookup(name)
            if hit is not None:
                return hit
        return None
    def find(self, name):
        if name in self.stack[-1]:
            return True
        else:
            return False
    def printStack(self):
        for table in self.stack:
            print(table)

class Visitor(NodeVisitor):
    """
    Program Visitor class. This class uses the visitor pattern as
    described in lya_ast.py.   It’s define methods of the form
    visit_NodeName() for each kind of AST node that we want to process.
    Note: You will need to adjust the names of the AST nodes if you
    picked different names.
    """
    def __init__(self):
        self.environment = Environment()
        self.typemap = {
            "int": int_type,
            "char": char_type,
            "string": string_type,
            "bool": bool_type,
            "void": void_type
        }
        self.assign = '='

    def print_error(self, lineno, text):
        if lineno is None:
            e = "ERROR: "
        else:
            e = "ERROR (line " + str(lineno) + "): "
        print(e + text)

    def get_exprType(self, raw_type, lineno):
        if raw_type in self.typemap:
            return self.typemap[raw_type]
        self.print_error(lineno, "Type {} not found".format(raw_type))
        return self.typemap["void"]

    def raw_type_unary(self, node, op, val):
        if hasattr(val, "raw_type") and (val.raw_type != None):
            #if isinstance(val.type, ExprType):
            #    val_type = val.type
            #else:
            #    val_type = val.type[1]

            val_type = self.get_exprType(val.raw_type, node.lineno)

            if op not in val_type.unary_ops:
                self.print_error(node.lineno,
                      "Unary operator {} not supported".format(op))
            return val_type

    def raw_type_binary(self, node, op, left, right):
        if hasattr(left, "raw_type") and hasattr(right, "raw_type") and (left.raw_type != None) and (right.raw_type != None):

            #if isinstance(left.type, ExprType):
            #    left_type = left.type
            #else:
            #    left_type = left.type[1]

            #if isinstance(right.type, ExprType):
            #    right_type = right.type
            #else:
            #    right_type = right.type[1]

            left_type = self.get_exprType(left.raw_type, node.lineno)
            right_type = self.get_exprType(right.raw_type, node.lineno)

            if left_type != right_type:
                self.print_error(node.lineno,
                "Binary operator {} does not have matching types: {} and {}".format(op, left_type, right_type))
                return left_type
            errside = None
            if op not in left_type.binary_ops:
                errside = "LHS"
            if op not in right_type.binary_ops:
                errside = "RHS"
            if errside is not None:
                self.print_error(node.lineno,
                      "Binary operator {} not supported on {} of expression".format(op, errside))

            if op in relational_ops:
                return self.typemap['bool']
            return left_type

        if(not hasattr(left, "raw_type")):
            self.print_error(node.lineno,
            "Operand {} has no type".format(left))
        else:
            self.print_error(node.lineno,
            "Operand {} has no type".format(right))

    def visit_Program(self,node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        # Visit all of the statements
        if not node.stmts is None:
            for stmts in node.stmts: self.visit(stmts)

        self.environment.printStack()

    def visit_Declaration_Statement(self,node):
        # Visit all of the declarations
        if not node.declaration_list is None:
            for dcl in node.declaration_list: self.visit(dcl)

    def visit_Declaration(self,node):
        self.visit(node.mode)
        if not node.initialization is None:
            self.visit(node.initialization)
            if(node.mode.raw_type != node.initialization.raw_type):
                self.print_error(node.lineno, "Mismatched type initialization, expected " + str(node.mode.raw_type) + ", found " + str(node.initialization.type))

        # Visit all of the identifiers
        if not node.identifier_list is None:
            for ident in node.identifier_list:
                aux_type = self.environment.lookup(ident.ID)
                if not aux_type is None:
                    self.print_error(node.lineno,
                                     "Identifier " + str(ident.ID) + " already declared as {} {}".format(aux_type[0],
                                                                                                         aux_type[1]))
                else:
                    self.environment.add_local(ident.ID, ['var', node.mode.raw_type])

#    def visit_Initialization(self, node):
#        self.visit(node.expression) <- GO HERE

    def visit_Identifier(self, node):
        node.type = self.environment.lookup(node.ID)
        node.raw_type = None
        node.dcl_type = None
        #self.visit(node.ID)
        if(node.type != None):
            print("Identifier: ID \"" + str(node.ID) + "\" type \"{} {}\"".format(node.type[0], node.type[1]))
            node.dcl_type = node.type[0]
            node.raw_type = node.type[1]
            #while(not isinstance(node.type, ExprType) and node.type[0] == "type"):
            #    node.type = node.type[1]
        else:
            self.print_error(node.lineno,
            "Variable {} was not defined".format(node.ID))

    def visit_Synonym_Statement(self, node):
        # Visit all of the synonyms
        if not node.synonym_list is None:
            for syn in node.synonym_list: self.visit(syn)

    def visit_Synonym_Definition(self, node):
        self.visit(node.initialization)
        if not node.mode is None:
            self.visit(node.mode)
            if (node.mode.raw_type != node.initialization.raw_type):
                self.print_error(node.lineno,
                                 "Mismatched type initialization, expected " + node.mode.raw_type + ", found " + node.initialization.type)
        for ident in node.identifier_list:
            aux_type = self.environment.lookup(ident.ID)
            if not aux_type is None:
                self.print_error(node.lineno,
                                "Identifier " + str(ident.ID) + " already declared as {} {}".format(aux_type[0], aux_type[1]))
            else:
                self.environment.add_local(ident.ID, ['const', node.initialization.raw_type])

    def visit_Newmode_Statement(self, node):
        if not node.newmode_list is None:
            for newmode in node.newmode_list: self.visit(newmode)

    def visit_Mode_Definition(self, node):
        self.visit(node.mode)
        if not node.identifier_list is None:
            for ident in node.identifier_list:
                aux_type = self.environment.lookup(ident.ID)
                if not aux_type is None:
                    self.print_error(node.lineno,
                                     "Identifier " + str(ident.ID) + " already declared as {} {}".format(aux_type[0],
                                                                                                         aux_type[1]))
                else:
                    self.environment.add_local(ident.ID, ['type', node.mode.raw_type])

    def visit_Integer_Mode(self, node):
        #self.visit(node.INT)
        print("Integer Mode: " + str(node.INT))
        node.raw_type = 'int' #self.typemap[node.INT]

    def visit_Boolean_Mode(self, node):
        #self.visit(node.BOOL)
        print("Boolean Mode: " + str(node.BOOL))
        node.raw_type = 'bool' #self.typemap[node.BOOL]

    def visit_Character_Mode(self, node):
        #self.visit(node.CHAR)
        print("Character Mode: " + str(node.CHAR))
        node.raw_type = 'char' #self.typemap[node.CHAR]

    def visit_Discrete_Range_Mode(self, node):
        self.visit(node.identifier)
        self.visit(node.literal_range)
        self.visit(node.discrete_mode)

    def visit_Mode_Name(self, node):
        print("Mode name")
        self.visit(node.identifier)
        node.raw_type = node.identifier.raw_type

    def visit_Literal_Range(self, node):
        self.visit(node.lower_bound.expression)
        self.visit(node.upper_bound.expression)

    def visit_Reference_Mode(self, node):
        self.visit(node.mode)
        node.raw_type = node.mode.raw_type

    def visit_String_Mode(self, node):
        print("String Mode")
        node.raw_type = 'string' #self.typemap["string"]
        self.visit(node.string_length)

    def visit_String_Length(self, node):
        self.visit(node.integer_literal)

    def visit_Array_Mode(self, node):
        if not node.index_mode_list is None:
            for index_mode in node.index_mode_list: self.visit(index_mode)
        self.visit(node.element_mode)

    def visit_Element_Mode(self, node):
        self.visit(node.mode)

    def visit_Integer_Expression(self, node):
        print("Integer expression")
        self.visit(node.expression)

        #if isinstance(node.expression, Identifier):
        #    exp_type = node.expression.type[1]
        #else:
        #    exp_type = node.expression.type
        exp_type = node.expression.raw_type

        if (exp_type != 'int'):
            self.print_error(node.lineno, "Expected integer expression, found {}".format(exp_type))

        node.raw_type = exp_type

    # location

    #def visit_Dereferenced_Reference(self, node):
    #    self.visit(node.location)

    def visit_String_Element(self, node):
        self.visit(node.identifier)
        self.visit(node.start_element)
        node.raw_type = None
        node.dcl_type = node.identifier.dcl_type
        if (node.identifier.raw_type == 'string'):
            node.raw_type = 'char'
        else:
            self.print_error(node.lineno, "Attempted to access string element in non-string " + str(node.identifier.ID))



    def visit_Start_Element(self, node):
        self.visit(node.integer_expression)

    def visit_String_Slice(self, node):
        self.visit(node.identifier)
        self.visit(node.left_element)
        self.visit(node.right_element)

        node.raw_type = None
        node.dcl_type = node.identifier.dcl_type
        if (node.identifier.raw_type == 'string'):
            node.raw_type = 'char'
        else:
            self.print_error(node.lineno, "Attempted to access string element in non-string " + str(node.identifier.ID))

    def visit_Left_Element(self, node):
        self.visit(node.integer_expression)

    def visit_Right_Element(self, node):
        self.visit(node.integer_expression)

    def visit_Array_Element(self, node):
        self.visit(node.array_location)
        if not node.expression_list is None:
            for expression in node.expression_list: self.visit(expression)

        node.raw_type = node.array_location.raw_type
        node.dcl_type = node.array_location.dcl_type

    # expression_list

    def visit_Array_Slice(self, node):
        self.visit(node.array_location)
        self.visit(node.lower_bound)
        self.visit(node.upper_bound)

        node.raw_type = node.array_location.raw_type
        node.dcl_type = node.array_location.dcl_type
        if (node.lower_bound.raw_type != node.upper_bound.raw_type):
            self.print_error(node.lineno, "Mismatching bound types {} and {} in array slice".format(node.lower_bound.raw_type, node.upper_bound.raw_type))


    # TODO: CHECK IF LOCATION IS ARRAY
    def visit_Array_Location(self, node):
        self.visit(node.location)

    # primitive_value

    # literal

    def visit_Integer_Literal(self, node):
        #self.visit(node.ICONST)
        node.raw_type = 'int' #self.typemap["int"]
        print("Integer Literal: " + str(node.value))

    def visit_Boolean_Literal(self, node):
        #self.visit(node.BOOL)
        print("Boolean Literal: " + str(node.value))
        node.raw_type = 'bool' #self.typemap["bool"]

    def visit_Character_Literal(self, node):
        #self.visit(node.CCONST)
        print("Character Literal: " + str(node.value))
        node.raw_type = 'char' #self.typemap["char"]

    def visit_Empty_Literal(self, node):
        #self.visit(node.NULL)
        print("Empty literal")
        node.raw_type = 'void' #self.typemap["void"]

    def visit_Character_String_Literal(self, node):
        #self.visit(node.SCONST)
        print("Character String Literal: " + str(node.value))
        node.raw_type = 'string' #self.typemap["string"]

    def visit_Value_Array_Element(self, node):
        self.visit(node.array_primitive_value)
        self.visit(node.integer_expression)

    def visit_Value_Array_Slice(self, node):
        self.visit(node.array_primitive_value)
        self.visit(node.lower_bound)
        self.visit(node.upper_bound)

    def visit_Array_Primitive_Value(self, node):
        self.visit(node.primitive_value)

    #def visit_Parenthesized_Expression(self, node):
    #    self.visit(node.expression)

    # expression

    def visit_Conditional_Expression(self, node):
        print("Conditional expression")
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
            node.raw_type = then_type


    def visit_Boolean_Expression(self, node):
        print("Boolean expression")
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
        node.raw_type = exp_type

    def visit_Then_Expression(self, node):
        print("Then expression")
        self.visit(node.expression)

        #if isinstance(node.expression, Identifier):
        #    exp_type = node.expression.type[1]
        #else:
        #    exp_type = node.expression.type
        exp_type = node.expression.raw_type
        node.raw_type = exp_type

    def visit_Else_Expression(self, node):
        print("Else expression")
        self.visit(node.expression)

        #if isinstance(node.expression, Identifier):
        #    exp_type = node.expression.type[1]
        #else:
        #    exp_type = node.expression.type
        exp_type = node.expression.raw_type
        node.raw_type = exp_type

    def visit_Elsif_Expression(self, node):
        print("Elsif expression")

        self.visit(node.boolean_expresson)
        self.visit(node.then_expression)
        then_type = node.then_expression.raw_type
        if not node.elsif_expression is None:
            self.visit(node.elsif_expression)
            elsif_type = node.elsif_expression.raw_type
            if(then_type != elsif_type):
                self.print_error(node.lineno, "Mismatching types in Elsif expression {} and {}".format(then_type, elsif_type))
        node.raw_type = then_type


    def visit_Rel_Mem_Expression(self, node):
        self.visit(node.operand0)
        self.visit(node.operand1)
        # self.visit(node.operator1)
        print("Relational or Membership operator: " + str(node.operator1))
        node.type = self.raw_type_binary(node, node.operator1, node.operand0, node.operand1)
        node.raw_type = node.operand0.raw_type

    # operator1

    # relational_operator

    # membership_operator

    def visit_Binary_Expression(self, node):
        self.visit(node.operand1)
        self.visit(node.operand2)
        #self.visit(node.operator2)
        print("Binary operator: " + str(node.operator2))
        node.type = self.raw_type_binary(node, node.operator2, node.operand1, node.operand2)
        node.raw_type = node.operand1.raw_type

    # operator2

    # arithmetic_additive_operator

    # string_concatenation_operator

    # operand2

    # arithmetic_multiplicative_operator

    def visit_Unary_Expression(self, node):
        #self.visit(node.monadic_operator)
        print("Monadic operator: " + str(node.monadic_operator))
        self.visit(node.operand4)
        node.type = self.raw_type_unary(node, node.monadic_operator, node.operand4)
        node.raw_type = node.operand4.raw_type

    # monadic_operator

    # operand4

    def visit_Referenced_Location(self, node):
        self.visit(node.location)

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
            self.environment.add_local(ident.ID, ['label', 'void'])

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
            if (node.location.dcl_type != 'var'):
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
            print("Assigning operator: " + str(node.assigning_operator))
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
        print("If Action")
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

    def visit_Procedure_Call(self, node):
        self.visit(node.identifier)
        type = self.environment.lookup(node.identifier.ID)
        node.dcl_type = type[0]
        node.raw_type = type[1]
        if type is None:
            self.print_error(node.lineno,"Procedure {} not found".format(node.identifier.ID))
        elif (type[0] != 'proc'):
            self.print_error(node.lineno, "Expected Procedure call {}, found {} {}".format(node.identifier.ID, type[0], type[1]))
        else:
            parameter_count = 0
            if not node.parameter_list is None:
                parameter_count = len(node.parameter_list)
            expected_count = len(type[2])
            if (parameter_count != expected_count):
                self.print_error(node.lineno, "Incorrect parameter count at Procedure {}; Expected {}, found {}".format(node.identifier.ID, expected_count, parameter_count))
            elif not node.parameter_list is None:
                for i, param in enumerate(node.parameter_list, start=0):
                    self.visit(param)
                    if param.raw_type is None:
                        self.print_error(node.lineno,
                                         "Incorrect parameter type at position i={}; Expected {}, found {}".format(
                                             i, type[2][i], param_type))
                    else:
                        #if isinstance(param.type, ExprType):
                        #    param_type = param.type
                        #else:
                        #    param_type = param.type[1]
                        param_type = param.raw_type

                        if (param_type != type[2][i]):
                            self.print_error(node.lineno,
                                             "Incorrect parameter type at position i={}; Expected {}, found {}".format(
                                                 i, type[2][i], param_type))

    # parameter_list

    def visit_Parameter(self, node):
        self.visit(node.expression)
        node.raw_type = node.expression.raw_type

    def visit_Exit_Action(self, node):
        self.visit(node.label_id)

    def visit_Return_Action(self, node):
        self.visit(node.result)

    def visit_Result_Action(self, node):
        self.visit(node.result)

    # def visit_Result(self, node):
    #    self.visit(node.expression)

    def visit_Builtin_Call(self, node):
        #node.identifier = Identifier(node.builtin_name.name)
        #self.visit_Procedure_Call(node)

        self.visit(node.builtin_name)
        if not node.parameter_list is None:
            for param in node.parameter_list: self.visit(param)

    # TODO: LIST OF PARAMETERS FOR BUILTIN NAMES
    #def visit_Builtin_Name(self, node):
    #    print("Builtin Name: " + str(node.name))


    def visit_Procedure_Statement(self, node):
        proc_name = node.label_id.identifier.ID

        self.environment.push('PROCEDURE DECLARATION '+ proc_name)
        self.visit(node.procedure_definition)
        self.environment.pop()

    def visit_Procedure_Definition(self, node):
        self.visit(node.formal_procedure_head)

        if not node.statement_list is None:
            for statement in node.statement_list:
                self.visit(statement)
                if hasattr(statement, 'action') and statement.action.__class__.__name__ == "Return_Action":

                    expected = node.formal_procedure_head.result_spec
                    found_type = None
                    if not statement.action.result is None:
                        #if (isinstance(statement.action.result.type, ExprType)):
                        #    found_type = statement.action.result.type
                        #else:
                        #    found_type = statement.action.result.type[1]
                        found_type = statement.action.result.raw_type

                    if expected is None:
                            self.print_error(node.lineno, "Expected void return, found {}".format(found_type))
                    else:
                        if (found_type != expected.mode.raw_type):
                            self.print_error(node.lineno, "Expected {} return, found {}".format(expected.mode.raw_type,found_type))

    def visit_Formal_Procedure_Head(self, node):
        node.param_types = []
        if not node.formal_parameter_list is None:
            for formal_param in node.formal_parameter_list:
                self.visit(formal_param)
                node.param_types.append(formal_param.raw_type)

        if node.result_spec is None:
            result_type = 'void'
        else:
            self.visit(node.result_spec)
            result_type = node.result_spec.mode.raw_type

        proc_name = self.environment.peek().return_type().replace("PROCEDURE DECLARATION ","")
        print(proc_name)

        aux_type = self.environment.lookup(proc_name)
        if not aux_type is None:
            self.print_error(node.lineno,
                             "Identifier " + str(proc_name) + " already declared as {} {}".format(aux_type[0],
                                                                                                  aux_type[1]))
        else:
            param_list = node.param_types
            self.environment.add_parent(proc_name, ['proc', result_type, node.param_types])


    # formal_parameter_list

    def visit_Formal_Parameter(self, node):

        self.visit(node.parameter_spec)
        node.raw_type = node.parameter_spec.mode.raw_type

        if not node.identifier_list is None:
            for ident in node.identifier_list:
                aux_type = self.environment.lookup(ident.ID)

                if not aux_type is None:
                    self.print_error(node.lineno,
                                     "Identifier " + str(ident.ID) + " already declared as {} {}".format(aux_type[0],
                                                                                                         aux_type[1]))
                else:
                    self.environment.add_local(ident.ID, ['var', node.raw_type])
        self.visit(node.parameter_spec)

    def visit_Parameter_Spec(self, node):
        self.visit(node.mode)
        #if (node.parameter_attribute != None):
            #WHAT IS LOC?
            #node.mode.raw_type.append(node.parameter_attribute)

    # parameter_attribute

    def visit_Result_Spec(self, node):
        self.visit(node.mode)
        #if (node.result_attribute != None):
        #    node.mode.type.append(node.result_attribute)
