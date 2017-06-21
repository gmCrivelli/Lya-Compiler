

MEMORY_SIZE = 64
DISPLAY_SIZE = 8

class VirtualMachine:

    def main():
        # dcl a, b int;
        # a = 10;
        # b = 20;
        # a = a + b - 30;
        # print(a);

        program = [
            ('stp',),
            ('alc', 2),
            ('ldc', 100),
            ('stv', 0, 0),
            ('ldc', 200),
            ('stv', 0, 1),
            ('ldv', 0, 0),
            ('ldv', 0, 1),
            ('add',),
            ('ldc', 3000),
            ('sub',),
            ('stv', 0, 0),
            ('ldv', 0, 0),
            ('prv', 0),
            ('ldv', 0, 1),
            ('prv', 0),
            ('dlc', 2),
            ('end',)
        ]

        # program =  [
        #     ('stp',),
        #     ('alc', 2),      # dcl i,k int;
        #     ('rdv',),
        #     ('stv', 0, 1),   # read(k);
        #     ('ldc', 1),
        #     ('stv', 0, 0),   # i=1;
        #     ('lbl', 1),      # do
        #     ('ldv', 0, 0),
        #     ('ldv', 0, 1),
        #     ('leq',),
        #     ('jof', 2),      #   while i<=k;
        #     ('ldv', 0, 0),
        #     ('ldv', 0, 0),
        #     ('mul',),
        #     ('prv', 0),      #      print(i*i);
        #     ('ldv', 0, 0),
        #     ('ldc', 1),
        #     ('add',),
        #     ('stv', 0, 0),   #      i=i+1;
        #     ('jmp', 1),      # od;
        #     ('lbl', 2),
        #     ('dlc', 2),
        #     ('end',)
        #     ]

        # H = ["Welcome.\n", "What’s you name?", "Nice to meet you "]
        #
        # program = [
        #     ('stp',),
        #     ('alc', 11),
        #     ('ldc', 0),
        #     ('stv', 0, 0),    # dcl name chars[10];
        #     ('prc', 0),      # print("Welcome.\n");
        #     ('prc', 1),      # print("What’s your name?");
        #     ('ldr', 0, 0),
        #     ('rds',),         # read(name);
        #     ('prc', 2),
        #     ('ldr', 0, 0),
        #     ('prs',),         # print("Nice to meet you ", name);
        #     ('dlc', 11),
        #     ('end',)
        #     ]

        H = ["give-me a positive integer:", "fatorial of ", " = ", ]
        # program = [
        #   ('stp', ),
        #   ('alc', 1),
        #   ('jmp', 3),
        #   ('lbl', 1),
        #   ('enf', 1),
        #   ('ldv', 1, -3),
        #   ('ldc', 0),
        #   ('equ', ),
        #   ('jof', 4),
        #   ('ldc', 1),
        #   ('stv', 1, -4),
        #   ('jmp', 2),
        #   ('jmp', 5),
        #   ('lbl', 4),
        #   ('ldv', 1, -3),
        #   ('alc', 1),
        #   ('ldv', 1, -3),
        #   ('ldc', 1),
        #   ('sub', ),
        #   ('cfu', 1),
        #   ('mul', ),
        #   ('stv', 1, -4),
        #   ('jmp', 2),
        #   ('lbl', 5),
        #   ('lbl', 2),
        #   ('ret', 1, 1),
        #   ('lbl', 3),
        #   ('prc', 0),
        #   ('rdv', ),
        #   ('stv', 0, 0),
        #   ('prc', 1),
        #   ('ldv', 0, 0),
        #   ('prv', 0),
        #   ('prc', 2),
        #   ('alc', 1),
        #   ('ldv', 0, 0),
        #   ('cfu', 1),
        #   ('prv', 0),
        #   ('dlc', 1),
        #   ('end',)
        #   ]

        VirtualMachine.execute(program, H, False)

    def execute(program, heap = [], debug = False):
        labels = {}
        memory = []
        display = []
        sp = 0
        pc = 0

        for pc in range(len(program)):
            t = program[pc]

            if t[0] == 'lbl':
                i = t[1]

                if i in labels:
                    print("LabelError: label " + str(i) + " declared at " + str(labels[i]) + " and " + str(pc))
                    exit(1)

                labels[i] = pc

        if debug:
            print("Labels: " + str(labels))

        pc = 0
        while True:
            t = program[pc]

            if debug:
                print("At line: " + str(pc))
                print("Executing: " + str(t))
                print("PC: " + str(pc))
                print("SP: " + str(sp))

            if t[0] == 'ldc':
                k = t[1]

                sp += 1
                memory[sp] = k

            elif t[0] == 'ldv':
                i = t[1]
                j = t[2]

                sp += 1
                memory[sp] = memory[display[i] + j]

            elif t[0] == 'ldr':
                i = t[1]
                j = t[2]

                sp += 1
                memory[sp] = display[i] + j

            elif t[0] == 'stv':
                i = t[1]
                j = t[2]

                memory[display[i] + j] = memory[sp]
                sp -= 1

            elif t[0] == 'lrv':
                i = t[1]
                j = t[2]

                sp += 1
                memory[sp] = memory[memory[display[i] + j]]

            elif t[0] == 'srv':
                i = t[1]
                j = t[2]

                memory[memory[display[i] + j]] = memory[sp]
                sp -= 1

            elif t[0] == 'add':
                memory[sp - 1] = memory[sp - 1] + memory[sp]
                sp -= 1

            elif t[0] == 'sub':
                memory[sp-1] = memory[sp - 1] - memory[sp]
                sp -= 1

            elif t[0] == 'mul':
                memory[sp - 1] = memory[sp - 1] * memory[sp]
                sp -= 1

            elif t[0] == 'div':
                memory[sp - 1] = memory[sp - 1] / memory[sp]
                sp -= 1

            elif t[0] == 'mod':
                memory[sp - 1] = memory[sp - 1] % memory[sp]
                sp -= 1

            elif t[0] == 'neg':
                memory[sp] = -memory[sp]

            elif t[0] == 'abs':
                memory[sp] = abs(memory[sp])

            elif t[0] == 'and':
                memory[sp - 1] = memory[sp - 1] and memory[sp]
                sp -= 1

            elif t[0] == 'lor':
                memory[sp - 1] = memory[sp - 1] or memory[sp]
                sp -= 1

            elif t[0] == 'not':
                memory[sp] = not memory[sp]

            elif t[0] == 'les':
                memory[sp - 1] = memory[sp - 1] = memory[sp]
                sp -= 1

            elif t[0] == 'leq':
                memory[sp - 1] = memory[sp - 1] <= memory[sp];
                sp -= 1

            elif t[0] == 'grt':
                memory[sp - 1] = memory[sp - 1] <= memory[sp]
                sp -= 1

            elif t[0] == 'gre':
                memory[sp - 1] = memory[sp - 1] > memory[sp]
                sp -= 1

            elif t[0] == 'equ':
                memory[sp - 1] = memory[sp - 1] == memory[sp]
                sp -= 1

            elif t[0] == 'neq':
                memory[sp - 1] = memory[sp - 1] != memory[sp]
                sp -= 1

            elif t[0] == 'jmp':
                p = t[1]

                pc = labels.get(p, pc)

            elif t[0] == 'jof':
                p = t[1]

                if not memory[sp]:
                    pc = labels.get(p, pc)

                sp -= 1

            elif t[0] == 'alc':
                n = t[1]

                memory.extend([0] * n)
                sp += n

            elif t[0] == 'dlc':
                n = t[1]

                memory.pop(n)
                sp -= n

            elif t[0] == 'cfu':
                p = t[1]

                sp += 1
                memory[sp] = pc
                pc = labels.get(p, pc)

            elif t[0] == 'enf':
                k = t[1]

                sp += 1
                memory[sp] = display[k]
                display[k] = sp + 1

            elif t[0] == 'ret':
                k = t[1]
                n = t[2]

                display[k] = memory[sp]
                pc = memory[sp - 1]
                sp -= (n + 2)

            elif t[0] == 'idx':
                k = t[1]

                memory[sp - 1] = memory[sp - 1] + memory[sp] * k
                sp -= 1

            elif t[0] == 'grc':
                memory[sp] = memory[memory[sp]]

            elif t[0] == 'lmv':
                k = t[1]

                t = memory[sp]
                memory[sp : sp + k] = memory[t : t + k]
                sp += (k - 1)

            elif t[0] == 'smv':
                k = t[1]

                t = memory[sp - k]
                memory[t : t + k] = memory[sp - k + 1 : sp + 1]
                sp -= (k + 1)

            elif t[0] == 'smr':
                k = t[1]

                t1 = memory[sp - 1]
                t2 = memory[sp]
                memory[t1 : t1 + k] = memory[t2 : t2 + k]
                sp -= 1

            elif t[0] == 'sts':
                k = t[1]

                adr = memory[sp]
                memory[adr] = len(heap[k])
                for c in heap[k]:
                    adr = adr + 1
                    memory[adr] = c;
                sp -= 1

            elif t[0] == 'rdv':
                value = input()
                try:
                    value = int(value)
                except ValueError:
                    print("ValueError: expected an 'int', found 'string'")
                    exit(1)

                sp += 1
                memory[sp] = value

            elif t[0] == 'rds':
                st = input()
                adr = memory[sp]
                memory[adr] = len(st)

                for k in st:
                    adr = adr + 1
                    memory[adr] = k

                sp -= 1

            elif t[0] == 'prv':
                ischar = t[1]

                if ischar:
                    print(chr(memory[sp]))
                else:
                    print(memory[sp])
                sp -= 1

            elif t[0] == 'prt':
                k = t[1]

                print(memory[sp - k + 1 : sp + 1]);
                sp -= (k-1)

            elif t[0] == 'prc':
                i = t[1]

                print(heap[i],end="")

            elif t[0] == 'prs':
                adr = memory[sp]
                l = memory[adr]
                for i in range(0,l):
                    adr = adr + 1
                    print(memory[adr], end = "")
                sp -= 1

            elif t[0] == 'stp':
                memory = [0] * MEMORY_SIZE
                display = [0] * DISPLAY_SIZE

                sp = -1
                display[0] = 0

            elif t[0] == 'lbl':
                i = t[1]

                # labels were preprocessed
                pass

            elif t[0] == 'nop':
                pass

            elif t[0] == 'end':
                break

            else:
                print("UnknownCall: '" + t[0] + "' is not declared")
                exit(1)

            if debug:
                print(memory)
                print(display)

            pc += 1


if __name__ == '__main__':
    VirtualMachine.main()
