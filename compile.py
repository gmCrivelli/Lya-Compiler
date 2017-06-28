
from lya_vm import VirtualMachine
import lexer as lex
from parser import Parser
from semantic import *
import sys

# Run parser on given file
def main():
    file_name = sys.argv[1]

    # Read given file
    file = open(file_name, "r")

    s = file.read()

    result = Parser()
    ast = result.parse(s)

    nv = Visitor()
    nv.visit(ast)

    #ast.print(False,'')

    ast.generate_code()

    # print('[')
    # for bla in AST.code:
    #     print(bla)
    # print(']')

    H = nv.string_literals
    # print("String literals: ", nv.string_literals_ascii)
    VirtualMachine.execute(AST.code, H, False)

if __name__ == "__main__": main()
