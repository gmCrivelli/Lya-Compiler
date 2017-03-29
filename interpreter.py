import sys

# Run lexer on given file
def main():
    file_name = sys.argv[1]

    # Read given file
    file = open(file_name, "r")

    title = ""
    k = 0

    for line in file:
        tok = line.split()

        if '::=' in line:
            if k != 0:
                sys.stdout.write("\'\'\'\n    p[0] = (\"" + title + "\", ")
                for i in range (1, k + 1):
                    sys.stdout.write("p[" + str(i) + "], ")
                print("p.lineno)\n")

            print("def p_" + tok[0][1:-1] + "(self, p):")
            title = tok[0][1:-1]
            k = 0
            tok = tok[2:]

            sys.stdout.write("    \'\'\'" + title + " : ")
        else:
            sys.stdout.write('    ')
        for l in tok:
            if(l == '|'):
                sys.stdout.write("\n        |")
                k = 0
            elif '<' in l and '>' in l:
                sys.stdout.write(" " + l[1:-1])
                k += 1
            else:
                sys.stdout.write(" " + l)
                k += 1

    if k != 0:
        sys.stdout.write("\'\'\'\n    p[0] = (\"" + title + "\", ")
        for i in range (1, k + 1):
            sys.stdout.write("p[" + str(i) + "], ")
        print("p.lineno)")
        print("\n\n")



if __name__ == "__main__": main()
