class NodeVisitor(object):
    """
    Class for visiting nodes of the parse tree.  This is modeled after
    a similar class in the standard library ast.NodeVisitor.  For each
    node, the visit(node) method calls a method visit_NodeName(node)
    which should be implemented in subclasses.  The generic_visit() method
    is called for all nodes where there is no matching visit_NodeName()
    method.
    Here is a example of a visitor that examines binary operators:
    class VisitOps(NodeVisitor):
        visit_Binop(self,node):
            print("Binary operator", node.op)
            self.visit(node.left)
            self.visit(node.right)
        visit_Unaryop(self,node):
            print("Unary operator", node.op)
            self.visit(node.expr)
    tree = parse(txt)
    VisitOps().visit(tree)
    """

    def visit(self,node):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None

    def generic_visit(self,node):
        if not isinstance(node, AST):
            print(node)
            return

        node.print()

        """
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        """
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        #item.print()
                        self.visit(item)
            elif isinstance(value, AST):
                #value.print()
                self.visit(value)



class AST(object):
    """
    Base class example for the AST nodes.  Each node is expected to
    define the _fields attribute which lists the names of stored
    attributes.   The __init__() method below takes positional
    arguments and assigns them to the appropriate fields.  Any
    additional arguments specified as keywords are also assigned.
    """
    _fields = []
    def __init__(self, *args, **kwargs):
        assert len(args) == len(self._fields)
        for name,value in zip(self._fields, args):
            setattr(self, name, value)
        # Assign additional keyword arguments if supplied
        for name,value in kwargs.items():
            setattr(self,name,value)

    def print(self):
        for field in self._fields:
            if isinstance(field, list):
                for item in field:
                    if isinstance(item,AST):
                        item.print()
                    else:
                        print(item)
            elif isinstance(field, AST):
                field.print()
            else:
                print(field)

class Program(AST):
    _fields = ['stmts']

# statement_list
# statement

class Declaration_Statement(AST):
    _fields = ['declaration_list']

# declaration_list

class Declaration(AST):
    _fields = ['identifier_list', 'mode', 'initialization']

class Initialization(AST):
    _fields = ['expression']

# identifier_list

class Identifier(AST):
    _fields = ['ID']

class Synonym_Statement(AST):
    _fields = ['synonym_list']

# synonym_list

class Synonym_Definition(AST):
    _fields = ['identifier_list', 'mode', 'initialization']

#class Constant_Expression(AST):
#    _fields = ['expression']

class Newmode_Statement(AST):
    _fields = ['newmode_list']

# newmode_list

class Mode_Definition(AST):
    _fields = ['identifier_list', 'mode']

# mode

# discrete_mode

class Integer_Mode(AST):
    _fields = ['INT']

class Boolean_Mode(AST):
    _fields = ['BOOL']

class Character_Mode(AST):
    _fields = ['CHAR']

class Discrete_Range_Mode(AST):
    _fields = ['identifier', 'literal_range', 'discrete_mode']

class Mode_Name(AST):
    _fields = ['identifier']

class Literal_Range(AST):
    _fields = ['lower_bound', 'upper_bound']

class Lower_Bound(AST):
    _fields = ['expression']

class Upper_Bound(AST):
    _fields = ['expression']

class Reference_Mode(AST):
    _fields = ['mode']

# composite_mode

class String_Mode(AST):
    _fields = ['string_length']

class String_Length(AST):
    _fields = ['integer_literal']

class Array_Mode(AST):
    _fields = ['index_mode_list', 'element_mode']

# index_mode_list

# index_mode

class Element_Mode(AST):
    _fields = ['mode']

class Integer_Expression(AST):
    _fields = ['expression']

# location

class Dereferenced_Reference(AST):
    _fields = ['location']

class String_Element(AST):
    _fields = ['identifier', 'start_element']

class Start_Element(AST):
    _fields = ['integer_expression']

class String_Slice(AST):
    _fields = ['identifier', 'left_element', 'right_element']

class Left_Element(AST):
    _fields = ['integer_expression']

class Right_Element(AST):
    _fields = ['integer_expression']

class Array_Element(AST):
    _fields = ['array_location', 'expression_list']

# expression_list

class Array_Slice(AST):
    _fields = ['array_location', 'lower_bound', 'upper_bound']

class Array_Location(AST):
    _fields = ['location']

# primitive_value

# literal

class Integer_Literal(AST):
    _fields = ['value']

class Boolean_Literal(AST):
    _fields = ['value']

class Character_Literal(AST):
    _fields = ['value']

class Empty_Literal(AST):
    _fields = ['value']

class Character_String_Literal(AST):
    _fields = ['value']

class Value_Array_Element(AST):
    _fields = ['array_primitive_value', 'integer_expression']

class Value_Array_Slice(AST):
    _fields = ['array_primitive_value', 'lower_bound', 'upper_bound']

class Array_Primitive_Value(AST):
    _fields = ['primitive_value']

class Parenthesized_Expression(AST):
    _fields = ['expression']

# expression

class Conditional_Expression(AST):
    _fields = ['boolean_expression', 'then_expression', 'elsif_expression', 'else_expression']

class Boolean_Expression(AST):
    _fields = ['expression']

class Then_Expression(AST):
    _fields = ['expression']

class Else_Expression(AST):
    _fields = ['expression']

class Elsif_Expression(AST):
    _fields = ['elsif_expression', 'boolean_expresson', 'then_expression']

class Rel_Mem_Expression(AST):
    _fields = ['operand0', 'operator1', 'operand1']

# operator1

# relational_operator

# membership_operator

class Binary_Expression(AST):
    _fields = ['operand1', 'operator2', 'operand2']

# operator2

# arithmetic_additive_operator

# string_concatenation_operator

#operand2

# arithmetic_multiplicative_operator

class Unary_Expression(AST):
    _fields = ['monadic_operator', 'operand4']

# monadic_operator

# operand4

class Referenced_Location(AST):
    _fields = ['location']

class Action_Statement(AST):
    _fields = ['label_id', 'action']

class Label_Id(AST):
    _fields = ['identifier']

# action

# bracketed_action

class Assignment_Action(AST):
    _fields = ['location', 'assigning_operator', 'expression']

# assigning_operator

# closed_dyadic_operator

class If_Action(AST):
    _fields = ['boolean_expression', 'then_clause', 'else_clause']

class Then_Clause(AST):
    _fields = ['action_statement_list']

# action_statement_list

class Else_Clause(AST):
    _fields = ['action_statement_list', 'boolean_expression', 'then_clause', 'else_clause']

class Do_Action(AST):
    _fields = ['control_part', 'action_statement_list']

class Control_Part(AST):
    _fields = ['for_control','while_control']

#for_control
#iteration

class Step_Enumeration(AST):
    _fields = ['loop_counter', 'start_value', 'step_value', 'end_value']

class Loop_Counter(AST):
    _fields = ['identifier']

#start_value
#step_value
#end_value

#discrete_expression

class Range_Enumeration(AST):
    _fields = ['loop_counter', 'discrete_mode']

class While_Control(AST):
    _fields = ['boolean_expression']

#class Call_Action(AST):
#    _fields = ['label_id']

class Procedure_Call(AST):
    _fields = ['identifier', 'parameter_list']

#parameter_list

class Parameter(AST):
    _fields = ['expression']

class Exit_Action(AST):
    _fields = ['label_id']

class Return_Action(AST):
    _fields = ['result']

class Result_Action(AST):
    _fields = ['result']

#class Result(AST):
#    _fields = ['expression']

class Builtin_Call(AST):
    _fields = ['builtin_name', 'parameter_list']

class Builtin_Name(AST):
    _fields = ['name']

class Procedure_Statement(AST):
    _fields = ['label_id', 'procedure_definition']

class Procedure_Definition(AST):
    _fields = ['formal_procedure_head', 'statement_list']

class Formal_Procedure_Head(AST):
    _fields = ['formal_parameter_list', 'result_spec']

#formal_parameter_list

class Formal_Parameter(AST):
    _fields = ['identifier_list', 'parameter_spec']

class Parameter_Spec(AST):
    _fields = ['mode', 'loc']

#parameter_attribute

class Result_Spec(AST):
    _fields = ['mode', 'loc']

#result_attribute
