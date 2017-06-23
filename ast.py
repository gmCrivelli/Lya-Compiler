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
    code = []
    variables = {}
    label_counter = 0
    label_dict = dict()
    offset = 0
    scope = 0

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

    def generate_code(self):
        for field in self._fields:
            aux = getattr(self, field)
            if isinstance(aux, list):
                for item in aux:
                    if isinstance(item, AST):
                        item.generate_code()
            elif isinstance(aux, AST):
                aux.generate_code()

class Program(AST):
    _fields = ['stmts']

    def generate_code(self):
        AST.code = []
        AST.label_counter = 0

        print("Program")
        AST.code.append(("stp", ))
        super(Program, self).generate_code()
        AST.code.append(("end", ))

# statement_list
# statement

class Declaration_Statement(AST):
    _fields = ['declaration_list']

# declaration_list

class Declaration(AST):
    _fields = ['identifier_list', 'mode', 'initialization']

    def generate_code(self):
        size = 1
        n = len(self.identifier_list)

        AST.code.append(("alc", size * n))

        if self.initialization != None:
            self.initialization.generate_code()

            for i, ident in enumerate(self.identifier_list):
                AST.code.append(("stv", 0, ident.offset))

                if i != len(self.identifier_list) - 1:
                    AST.code.append(("ldv", ident.scope, ident.offset))


class Initialization(AST):
    _fields = ['expression']

# identifier_list

class Identifier(AST):
    _fields = ['ID']

    def generate_code(self):
        #print("ID={}, raw_type={}, dcl_type={}, loc={}".format(self.ID, self.raw_type, self.dcl_type, self.loc))
        print(self.__dict__)
        AST.code.append(('ldv', self.scope, self.offset))

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
    _fields = ['size']

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

    def generate_code(self):
        super(Integer_Literal, self).generate_code()
        AST.code.append(("ldc", self.value))

class Boolean_Literal(AST):
    _fields = ['value']

    def generate_code(self):
        super(Boolean_Literal, self).generate_code()
        AST.code.append(("ldc", self.value))

class Character_Literal(AST):
    _fields = ['value']

    def generate_code(self):
        super(Character_Literal, self).generate_code()
        AST.code.append(("ldc", self.value))

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

    def generate_code(self):
        super(Rel_Mem_Expression, self).generate_code()
        if self.operator1 == '>':
            AST.code.append(("grt",))
        elif self.operator1 == '>=':
            AST.code.append(("gre",))
        elif self.operator1 == '<':
            AST.code.append(("les",))
        elif self.operator1 == '<=':
            AST.code.append(("leq",))
        elif self.operator1 == '==':
            AST.code.append(("equ",))
        elif self.operator1 == '!=':
            AST.code.append(("neq",))
        elif self.operator1 == '&&':
            AST.code.append(("and",))
        elif self.operator1 == '||':
            AST.code.append(("lor",))

# operator1

# relational_operator

# membership_operator

class Binary_Expression(AST):
    _fields = ['operand1', 'operator2', 'operand2']

    def generate_code(self):
        super(Binary_Expression, self).generate_code()
        if self.operator2 == '+' :
            AST.code.append(("add",))
        elif self.operator2 == '-':
            AST.code.append(("sub",))
        elif self.operator2 == '*':
            AST.code.append(("mul",))
        elif self.operator2 == '/':
            AST.code.append(("div",))
        elif self.operator2 == '%':
            AST.code.append(("mod",))
        else:
            raise Exception("Not implemented yet")

# operator2

# arithmetic_additive_operator

# string_concatenation_operator

#operand2

# arithmetic_multiplicative_operator

class Unary_Expression(AST):
    _fields = ['monadic_operator', 'operand4']

    def generate_code(self):
        super(Unary_Expression, self).generate_code()

        if self.monadic_operator == '-':
            AST.code.append(("neg",))
        elif self.monadic_operator == '!':
            AST.code.append(("not"))
        else:
            raise Exception("Not implemented yet")

# monadic_operator

# operand4

class Referenced_Location(AST):
    _fields = ['location']

class Action_Statement(AST):
    _fields = ['label_id', 'action']

class Label_Id(AST):
    _fields = ['identifier']

    def generate_code(self):
        AST.label_dict[self.identifier.ID] = AST.label_counter
        AST.code.append(("lbl",AST.label_counter))
        AST.label_counter += 1

# action

# bracketed_action

class Assignment_Action(AST):
    _fields = ['location', 'assigning_operator', 'expression']

    def generate_code(self):
        # super(Assignment_Action, self).generate_code()
        if self.assigning_operator == '=':
            self.expression.generate_code()
            AST.code.append(("stv", self.location.scope, self.location.offset))
        elif self.assigning_operator == '+=':
            AST.code.append(("ldv", self.location.scope, self.location.offset))
            self.expression.generate_code()
            AST.code.append(("add",))
            AST.code.append(("stv", self.location.scope, self.location.offset))
        elif self.assigning_operator == '-=':
            AST.code.append(("ldv", self.location.scope, self.location.offset))
            self.expression.generate_code()
            AST.code.append(("sub",))
            AST.code.append(("stv", self.location.scope, self.location.offset))
        elif self.assigning_operator == '*=':
            AST.code.append(("ldv", self.location.scope, self.location.offset))
            self.expression.generate_code()
            AST.code.append(("mul",))
            AST.code.append(("stv", self.location.scope, self.location.offset))
        elif self.assigning_operator == '/=':
            AST.code.append(("ldv", self.location.scope, self.location.offset))
            self.expression.generate_code()
            AST.code.append(("div",))
            AST.code.append(("stv", self.location.scope, self.location.offset))
        elif self.assigning_operator == '%=':
            AST.code.append(("ldv", self.location.scope, self.location.offset))
            self.expression.generate_code()
            AST.code.append(("mod",))
            AST.code.append(("stv", self.location.scope, self.location.offset))

# assigning_operator

# closed_dyadic_operator

class If_Action(AST):
    _fields = ['boolean_expression', 'then_clause', 'else_clause']

    def generate_code(self):
        end_label = AST.label_counter
        AST.label_counter += 1
        else_label = end_label

        if self.else_clause != None:
            else_label = AST.label_counter
            AST.label_counter += 1

        self.boolean_expression.generate_code()
        AST.code.append(("jof", else_label))
        self.then_clause.generate_code()

        if self.else_clause != None:
            AST.code.append(("jmp", end_label))
            AST.code.append(("lbl", else_label))
            self.else_clause.generate_code(end_label)
            AST.code.append(("lbl", end_label))

class Then_Clause(AST):
    _fields = ['action_statement_list']

# action_statement_list

class Else_Clause(AST):
    _fields = ['action_statement_list', 'boolean_expression', 'then_clause', 'else_clause']

    def generate_code(self, end_label):
        if self.action_statement_list != None:
            super(Else_Clause, self).generate_code()
        else:
            #end_label = AST.label_counter
            #AST.label_counter += 1
            else_label = end_label

            if self.else_clause != None:
                else_label = AST.label_counter
                AST.label_counter += 1

            self.boolean_expression.generate_code()
            AST.code.append(("jof", else_label))
            self.then_clause.generate_code()

            if self.else_clause != None:
                AST.code.append(("jmp", end_label))
                AST.code.append(("lbl", else_label))
                self.else_clause.generate_code(end_label)
                #AST.code.append(("lbl", end_label))

class Do_Action(AST):
    _fields = ['control_part', 'action_statement_list']

    def generate_code(self):
        if self.control_part != None:
            control_label = AST.label_counter
            AST.label_counter += 1
            end_label = AST.label_counter
            AST.label_counter += 1

            control_instructions = self.control_part.generate_code(control_label, end_label)

            if self.action_statement_list != None:
                for action in self.action_statement_list:
                    action.generate_code()
            for instruction in control_instructions:
                AST.code.append(instruction)
            AST.code.append(("jmp", control_label))
            AST.code.append(("lbl", end_label))

        else:
            super(Do_Action, self).generate_code()


# TODO: FOR_CONTROL
class Control_Part(AST):
    _fields = ['for_control','while_control']

    def generate_code(self, control_label, end_label):
        control_instructions = []
        if self.for_control != None:
            control_instructions = control_instructions + self.for_control.generate_code(control_label, end_label)
        else:
            AST.code.append(("lbl", control_label))
        if self.while_control != None:
           self.while_control.generate_code(end_label)
        return control_instructions

class For_Control(AST):
    _fields = ['iteration']

    def generate_code(self, control_label, end_label):
        return self.iteration.generate_code(control_label, end_label)

#iteration

class Step_Enumeration(AST):
    _fields = ['loop_counter', 'start_value', 'step_value', 'end_value']

    def generate_code(self, control_label, end_label):
        offset = self.loop_counter.identifier.offset
        scope = self.loop_counter.identifier.scope

        self.start_value.generate_code()
        AST.code.append(("stv", scope, offset))
        AST.code.append(("lbl", control_label))
        self.loop_counter.generate_code()
        loop_counter_code = AST.code[-1]

        self.end_value.generate_code()
        AST.code.append(("leq",))
        AST.code.append(("jof", end_label))

        print("WRITING THE CONTROL INSTRUCTIONS!")
        control_instructions = []

        if self.step_value != None:
            print("OOOOH BOY HERE WE GO AGAIN")
            leng = len(AST.code)
            self.step_value.generate_code()
            print(AST.code)
            control_instructions = AST.code[leng:]
            del AST.code[leng:]
            print(AST.code)
        else:
            control_instructions.append(("ldc", 1))

        control_instructions.append(loop_counter_code)
        control_instructions.append(("add",))
        control_instructions.append(("stv", scope, offset))
        print(control_instructions)
        return control_instructions

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

    def generate_code(self, end_label):
        self.boolean_expression.generate_code()
        AST.code.append(("jof", end_label))

#class Call_Action(AST):
#    _fields = ['label_id']

class Procedure_Call(AST):
    _fields = ['identifier', 'parameter_list']

    def generate_code(self):

        if self.identifier.type[1] != 'void':
            AST.code.append(("alc",1))

        for parameter in reversed(self.parameter_list):
            parameter.generate_code()

        AST.code.append(("cfu", self.identifier.scope))




#parameter_list

class Parameter(AST):
    _fields = ['expression']

class Exit_Action(AST):
    _fields = ['exit_label_id']

class Exit_Label_Id(AST):
    _fields = ['identifier']

class Return_Action(AST):
    _fields = ['result']

    def generate_code(self):
        if self.result != None:
            self.result.generate_code()
            AST.code.append(("stv", self.scope, self.offset))
        AST.code.append(("ret", self.scope, self.parameter_space))

class Result_Action(AST):
    _fields = ['result']

#class Result(AST):
#    _fields = ['expression']

class Builtin_Call(AST):
    _fields = ['builtin_name', 'parameter_list']

    def generate_code(self):
        #parameter = self.parameter_list[0].expression
        #AST.code.append(('ldv', 0, parameter.offset))

        if self.builtin_name.name == 'print':
            for param in self.parameter_list:
                if param.expression.raw_type == "string":
                    AST.code.append(('prc', param.expression.heap_index))
                else:
                    param.expression.generate_code()
                    if param.expression.raw_type == 'char':
                        AST.code.append(('prv', 1))
                    else:
                        AST.code.append(('prv', 0))
        elif self.builtin_name.name == 'read':
            for param in self.parameter_list:
                AST.code.append(('rdv',))
                AST.code.append(('stv', param.expression.scope, param.expression.offset))


        # super(Builtin_Call, self).generate_code()

class Builtin_Name(AST):
    _fields = ['name']

class Procedure_Statement(AST):
    _fields = ['label_id', 'procedure_definition']

    # Things are about to get tricky
    # Pass label_id object as parameter, since we must first write the "jmp" to
    # the end of the procedure, and only then write the "lbl"
    def generate_code(self):
        self.procedure_definition.generate_code(self.label_id)

class Procedure_Definition(AST):
    _fields = ['formal_procedure_head', 'statement_list']

    def generate_code(self, label_id):

        end_label = AST.label_counter
        AST.label_counter += 1
        AST.code.append(("jmp", end_label))

        label_id.generate_code()
        self.formal_procedure_head.generate_code()

        for statement in self.statement_list:
            statement.generate_code()

        AST.code.append(("lbl", end_label))

class Formal_Procedure_Head(AST):
    _fields = ['formal_parameter_list', 'result_spec']

    def generate_code(self):
        AST.code.append(("enf", self.scope))


#formal_parameter_list

class Formal_Parameter(AST):
    _fields = ['identifier_list', 'parameter_spec']

class Parameter_Spec(AST):
    _fields = ['mode', 'loc']

#parameter_attribute

class Result_Spec(AST):
    _fields = ['mode', 'loc']

#result_attribute
