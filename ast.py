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
    _fields = []

#class Constant_Expression(AST):
#    _fields = ['expression']

class Newmode_Statement(AST):
    _fields = ['type', 'newmode_list']

# newmode_list

class Mode_Definition(AST):
    _fields = ['identifier_list', 'mode']

# mode

# discrete_mode

#class Integer_Mode(AST):
#    _fields = ['INT']

#class Boolean_Mode(AST):
#    _fields = ['BOOL']

#class Character_Mode(AST):
#    _fields = ['CHAR']

# discrete_range_mode STILL WORK TO BE DONE IN THIS LINE RIGHT HERE!!!

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
    _fields = ['ICONST']

class Boolean_Literal(AST):
    _fields = ['bool']

class Character_Literal(AST):
    _fields = ['CCONST']

class Empty_Literal(AST):
    _fields = ['NULL']

class Character_String_Literal(AST):
    _fields = ['SCONST']

class Value_Array_Element(AST):
    _fields = ['array_primitive_value', 'integer_expression']

class Value_Array_Slice(AST):
    _fields = ['array_primitive_value', 'lower_bound', 'upper_bound']

class Array_Primitive_Value(AST):
    _fields = ['primitive_value']

class Parenthesized_Expression(AST):
    _fields = ['expression']





class Assignment(AST):
    _fields = ['lvalue', 'op', 'rvalue']
