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
            return self.decl.mode
        return None


class ExprType(object):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.supported_operators = []

int_type = ExprType("int")
int_type.unary_ops = ["-"]
int_type.binary_ops = ["+", "-", "*", "/", "%", "!=", "==", ">", ">=", "<", "<="]

bool_type = ExprType("bool")
bool_type.unary_ops = ["!"]
bool_type.binary_ops = ["==", "!="]

char_type = ExprType("char")
char_type.unary_ops = []
char_type.binary_ops = []
#char_type.supported_operators = ["PLUS", "MINUS",  "TIMES", "DIVIDE", "MOD"]

string_type = ExprType("string")
string_type.unary_ops = []
string_type.binary_ops = ["+", "==", "!="]

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
        })
    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))
    def pop(self):
        self.stack.pop()
    def peek(self):
        return self.stack[-1]
    def scope_level(self):
        return len(self.stack)
    def add_local(self, name, value):
        self.peek().add(name, value)
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
            "bool": bool_type
        }

    def print_error(self, lineno, text):
        if lineno is None:
            e = "ERROR: "
        else:
            e = "ERROR (line " + str(lineno) + "): "
        print(e + text)

    def raw_type_unary(self, node, op, val):
        if hasattr(val, "type"):
            if op not in val.type.unary_ops:
                self.print_error(node.lineno,
                      "Unary operator {} not supported".format(op))
            return val.type

    def raw_type_binary(self, node, op, left, right):
        if hasattr(left, "type") and hasattr(right, "type"):
            if left.type != right.type:
                self.print_error(node.lineno,
                "Binary operator {} does not have matching types".format(op))
                return left.type
            errside = None
            if op not in left.type.binary_ops:
                errside = "LHS"
            if op not in right.type.binary_ops:
                errside = "RHS"
            if errside is not None:
                self.print_error(node.lineno,
                      "Binary operator {} not supported on {} of expression".format(op, errside))
        return left.type

    def visit_Program(self,node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        # Visit all of the statements
        if not node.stmts is None:
            for stmts in node.stmts: self.visit(stmts)

    def visit_Declaration_Statement(self,node):
        # Visit all of the declarations
        if not node.declaration_list is None:
            for dcl in node.declaration_list: self.visit(dcl)

    def visit_Declaration(self,node):
        self.visit(node.mode)
        self.visit(node.initialization)

        # Visit all of the identifiers
        if not node.identifier_list is None:
            for ident in node.identifier_list:
                if not self.environment.lookup(ident.ID) is None:
                    self.print_error(node.lineno, "Variable " + str(ident.ID) + " already declared")
                else:
                    self.environment.add_local(ident.ID, node.mode.type)

    def visit_Initialization(self, node):
        self.visit(node.expression)

    def visit_Identifier(self, node):
        node.type = self.environment.lookup(node.ID)
        #node.type =
        #self.visit(node.ID)
        print("I'm visiting an identifier with ID " + str(node.ID) + " and type " + str(node.type))

    def visit_Synonym_Statement(self, node):
        # Visit all of the synonyms
        if not node.synonym_list is None:
            for syn in node.synonym_list: self.visit(syn)

    def visit_Synonym_Definition(self, node):
        if not node.identifier_list is None:
            for ident in node.identifier_list: self.visit(ident)
        self.visit(node.mode)
        self.visit(node.expression)

    def visit_Newmode_Statement(self, node):
        self.visit(node.type)
        if not node.newmode_list is None:
            for newmode in node.newmode_list: self.visit(newmode)

    def visit_Mode_Definition(self, node):
        self.visit(node.mode)

        if not node.identifier_list is None:
            for ident in node.identifier_list: self.visit(ident)


    def visit_Integer_Mode(self, node):
        #self.visit(node.INT)
        print("Integer Mode: " + str(node.INT))
        node.type = self.typemap[node.INT]

    def visit_Boolean_Mode(self, node):
        #self.visit(node.BOOL)
        print("Boolean Mode" + str(node.BOOL))
        node.type = self.typemap[node.BOOL]

    def visit_Character_Mode(self, node):
        #self.visit(node.CHAR)
        print("Character Mode" + str(node.CHAR))
        node.type = self.typemap[node.CHAR]

    def visit_Discrete_Range_Mode(self, node):
        self.visit(node.identifier)
        self.visit(node.literal_range)
        self.visit(node.discrete_mode)

    def visit_Mode_Name(self, node):
        self.visit(node.identifier)

    def visit_Literal_Range(self, node):
        self.visit(node.lower_bound.expression)
        self.visit(node.upper_bound.expression)

    def visit_Reference_Mode(self, node):
        self.visit(node.mode)

    def visit_String_Mode(self, node):
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
        self.visit(node.expression)

    # location

    def visit_Dereferenced_Reference(self, node):
        self.visit(node.location)

    def visit_String_Element(self, node):
        self.visit(node.identifier)
        self.visit(node.start_element)

    def visit_Start_Element(self, node):
        self.visit(node.integer_expression)

    def visit_String_Slice(self, node):
        self.visit(node.identifier)
        self.visit(node.left_element)
        self.visit(node.right_element)

    def visit_Left_Element(self, node):
        self.visit(node.integer_expression)

    def visit_Right_Element(self, node):
        self.visit(node.integer_expression)

    def visit_Array_Element(self, node):
        self.visit(node.array_location)
        if not node.expression_list is None:
            for expression in node.expression_list: self.visit(expression)

    # expression_list

    def visit_Array_Slice(self, node):
        self.visit(node.array_location)
        self.visit(node.lower_bound)
        self.visit(node.upper_bound)

    def visit_Array_Location(self, node):
        self.visit(node.location)

    # primitive_value

    # literal

    def visit_Integer_Literal(self, node):
        #self.visit(node.ICONST)
        self.type = "int"
        print("Integer Literal: " + str(node.value))

    def visit_Boolean_Literal(self, node):
        #self.visit(node.BOOL)
        print("Boolean Literal: " + str(node.value))

    def visit_Character_Literal(self, node):
        #self.visit(node.CCONST)
        print("Character Literal: " + str(node.value))

    def visit_Empty_Literal(self, node):
        #self.visit(node.NULL)
        print("Empty literal")

    def visit_Character_String_Literal(self, node):
        #self.visit(node.SCONST)
        print("Character String Literal: " + str(node.value))

    def visit_Value_Array_Element(self, node):
        self.visit(node.array_primitive_value)
        self.visit(node.integer_expression)

    def visit_Value_Array_Slice(self, node):
        self.visit(node.array_primitive_value)
        self.visit(node.lower_bound)
        self.visit(node.upper_bound)

    def visit_Array_Primitive_Value(self, node):
        self.visit(node.primitive_value)

    def visit_Parenthesized_Expression(self, node):
        self.visit(node.expression)

    # expression

    def visit_Conditional_Expression(self, node):
        self.visit(node.boolean_expression)
        self.visit(node.then_expression)
        self.visit(node.elsif_expression)
        self.visit(node.else_expression)

    def visit_Boolean_Expression(self, node):
        self.visit(node.expression)

    def visit_Then_Expression(self, node):
        self.visit(node.expression)

    def visit_Else_Expression(self, node):
        self.visit(node.expression)

    def visit_Elsif_Expression(self, node):
        self.visit(node.elsif_expression)
        self.visit(node.boolean_expresson)
        self.visit(node.then_expression)

    def visit_Rel_Mem_Expression(self, node):
        self.visit(node.operand0)
        #self.visit(node.operator1)
        print("Relational or Membership operator: " + str(node.operator1))
        self.visit(node.operand1)

    # operator1

    # relational_operator

    # membership_operator

    def visit_Binary_Expression(self, node):
        self.visit(node.operand1)
        self.visit(node.operand2)
        #self.visit(node.operator2)
        print("Binary operator: " + str(node.operator2))
        node.type = self.raw_type_binary(node, node.operator2, node.operand1, node.operand2)

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


    # monadic_operator

    # operand4

    def visit_Referenced_Location(self, node):
        self.visit(node.location)

    def visit_Action_Statement(self, node):
        self.visit(node.label_id)
        self.visit(node.action)

    def visit_Label_Id(self, node):
        self.visit(node.identifier)

    # action

    # bracketed_action

    def visit_Assignment_Action(self, node):
        self.visit(node.location)
        #self.visit(node.assigning_operator)
        print("Assigning operator: " + str(node.assigning_operator))
        self.visit(node.expression)

    # assigning_operator

    # closed_dyadic_operator

    def visit_If_Action(self, node):
        self.visit(node.boolean_expression)
        self.visit(node.then_clause)
        self.visit(node.else_clause)

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
        self.visit(node.control_part)
        if not node.action_statement_list is None:
            for action_statement in node.action_statement_list: self.visit(action_statement)

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
        if not node.parameter_list is None:
            for param in node.parameter_list: self.visit(param)

    # parameter_list

    def visit_Parameter(self, node):
        self.visit(node.expression)

    def visit_Exit_Action(self, node):
        self.visit(node.label_id)

    def visit_Return_Action(self, node):
        self.visit(node.result)

    def visit_Result_Action(self, node):
        self.visit(node.result)

    # def visit_Result(self, node):
    #    self.visit(node.expression)

    def visit_Builtin_Call(self, node):
        self.visit(node.builtin_name)
        if not node.parameter_list is None:
            for param in node.parameter_list: self.visit(param)

    def visit_Builtin_Name(self, node):
        #self.visit(node.name)
        print("Builtin Name: " + str(node.name))

    def visit_Procedure_Statement(self, node):
        self.visit(node.label_id)
        self.visit(node.procedure_definition)

    def visit_Procedure_Definition(self, node):
        self.visit(node.formal_procedure_head)
        if not node.statement_list is None:
            for statement in node.statement_list: self.visit(statement)

    def visit_Formal_Procedure_Head(self, node):  # I HAVE NO IDEA
        self.visit(node.formal_parameter_list)
        self.visit(node.result_spec)

    # formal_parameter_list

    def visit_Formal_Parameter(self, node):
        self.visit(node.identifier_list)
        self.visit(node.parameter_spec)

    def visit_Parameter_Spec(self, node):
        self.visit(node.mode)
        self.visit(node.parameter_attribute)

    # parameter_attribute

    def visit_Result_Spec(self, node):
        self.visit(node.mode)
        self.visit(node.result_attribute)