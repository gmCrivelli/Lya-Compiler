#!/usr/bin/env python
# -*- coding: utf-8 -*-

MEMORY_SIZE = 64
DISPLAY_SIZE = 8

class VirtualMachine:
    def execute(program, heap = [], debug = False):
        labels = {}
        memory = []
        display = []
        buf = []
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
                memory[sp - 1] = int(memory[sp - 1] / memory[sp])
                sp -= 1

            elif t[0] == 'mod':
                memory[sp - 1] = memory[sp - 1] % memory[sp]
                sp -= 1

            elif t[0] == 'neg':
                memory[sp] = -memory[sp]

            elif t[0] == 'abs':
                memory[sp] = abs(memory[sp])

            elif t[0] == 'num':
                t = memory[sp]
                num = 0
                for i in range(0,memory[t]):
                    num *= 10
                    num += memory[t+i+1] - ord('0')
                memory[sp] = num

            elif t[0] == 'low':
                if memory[sp] >= 65 and memory[sp] <= 90:
                    memory[sp] += 32

            elif t[0] == 'upp':
                if memory[sp] >= 97 and memory[sp] <= 122:
                    memory[sp] -= 32

            elif t[0] == 'and':
                memory[sp - 1] = memory[sp - 1] and memory[sp]
                sp -= 1

            elif t[0] == 'lor':
                memory[sp - 1] = memory[sp - 1] or memory[sp]
                sp -= 1

            elif t[0] == 'not':
                memory[sp] = not memory[sp]

            elif t[0] == 'les':
                memory[sp - 1] = memory[sp - 1] < memory[sp]
                sp -= 1

            elif t[0] == 'leq':
                memory[sp - 1] = memory[sp - 1] <= memory[sp]
                sp -= 1

            elif t[0] == 'grt':
                memory[sp - 1] = memory[sp - 1] > memory[sp]
                sp -= 1

            elif t[0] == 'gre':
                memory[sp - 1] = memory[sp - 1] >= memory[sp]
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

                if not memory[sp] or memory[sp] == 'false':
                    pc = labels.get(p, pc)

                sp -= 1

            elif t[0] == 'alc':
                n = t[1]

                memory.extend([0] * n)
                sp += n

            elif t[0] == 'dlc':
                n = t[1]
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
                if len(buf) == 0:
                    buf = input().split()
                value = int(buf[0])
                buf = buf[1:]

                try:
                    value = int(value)
                except ValueError:
                    print("ValueError: expected an 'int', found 'string'")
                    exit(1)

                sp += 1
                memory[sp] = value

            elif t[0] == 'rdc':
                if len(buf) == 0:
                    buf = input().split()

                if len(list(buf[0])) > 1:
                        print("ValueError: expected a 'char', found a 'string'")
                        exit(1)
                value = ord(list(buf[0])[0])
                buf = buf[1:]

                sp += 1
                memory[sp] = value

            elif t[0] == 'rds':
                if len(buf) == 0:
                    buf = input().split()
                st = buf[0]
                buf = buf[1:]

                adr = memory[sp]
                memory[adr] = len(st)

                for k in st:
                    adr = adr + 1
                    memory[adr] = k

                sp -= 1

            elif t[0] == 'prv':
                ischar = t[1]

                if ischar:
                    print(chr(memory[sp]),end='')
                else:
                    print(memory[sp],end=' ')
                sp -= 1

            elif t[0] == 'prt':
                k = t[1]

                print(memory[sp - k + 1 : sp + 1], end='');
                sp -= (k-1)

            elif t[0] == 'prc':
                i = t[1]
                for c in heap[i]:
                    print(chr(c),end="")

            elif t[0] == 'prs':
                adr = memory[sp]
                l = memory[adr]
                for i in range(0,l):
                    adr = adr + 1
                    print(chr(memory[adr]), end = "")
                sp -= 1

            elif t[0] == 'stp':
                memory = [0] * MEMORY_SIZE
                display = [0] * DISPLAY_SIZE

                sp = -1
                display[0] = 0

            elif t[0] == 'lbl':
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
