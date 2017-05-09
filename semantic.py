import sys
import lexer
import parser
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
int_type.unary_ops = ["PLUS", "MINUS", "TIMES", "DIVIDE", "MOD", "DIFF", "EQUAL"]
int_type.bin_ops = ["PLUS", "MINUS", "TIMES", "DIVIDE", "MOD", "DIFF", "EQUAL"]

bool_type = ExprType("bool")
bool_type.supported_operators = ["AND", "OR",  "NOT", "DIFF", "EQUAL"]

char_type = ExprType("char")
#char_type.supported_operators = ["PLUS", "MINUS",  "TIMES", "DIVIDE", "MOD"]

string_type = ExprType("string")
string_type.supported_operators = ["STRCAT"]

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
        for stmts in node.stmts: self.visit(stmts)

    def visit_Identifier(self, node):
        print("I'm visiting an identifier!")

    def visit_SynStmt(self, node):
        # Visit all of the synonyms
        for syn in node.syns:
            self.visit(syn)

    def visit_UnaryExpr(self,node):
        self.visit(node.expr)
        # Make sure that the operation is supported by the type
        raw_type = self.raw_type_unary(node, node.op, node.expr)
        # Set the result type to the same as the operand
        node.raw_type = raw_type

    def visit_BinaryExpr(self,node):
        # Make sure left and right operands have the same type
        # Make sure the operation is supported
        self.visit(node.left)
        self.visit(node.right)
        raw_type = self.raw_type_binary(node, node.op, node.left, node.right)
        # Assign the result type
        node.raw_type = raw_type