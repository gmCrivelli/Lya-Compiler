
from lya_vm import VirtualMachine
import lexer as lex
from parser import Parser
from semantic import *
import sys

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python3 compile.py file.lya <-d> <-o>")
        print("-d: debug mode")
        print("-o: generate lvm code only")
        return 1

    file_name = sys.argv[1]

    debug = '-d' in sys.argv
    code = '-o' in sys.argv

    # Read given file
    file = open(file_name, "r")

    s = file.read()

    result = Parser()
    ast = result.parse(s)

    nv = Visitor()
    nv.visit(ast)

    if nv.semantic_error:
        print("Error found. Terminating execution")
        exit(1)

    ast.generate_code()

    if debug:
        # Print undecorated AST
        print("Printing Undecorated AST")
        ast.print(False,'')
        print("Printing Decorated AST")
        ast.print(True,'')
        print("Printing LVM Code")

    if code or debug:
        print('[')
        for st in AST.code:
            print(st)
        print(']')

    H = nv.string_literals
    if not code:
        VirtualMachine.execute(AST.code, H, False)

if __name__ == "__main__": main()
