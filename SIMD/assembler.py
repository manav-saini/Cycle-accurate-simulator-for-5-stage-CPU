table={
    "LD": '000',
    "ST": '001',
    "ADD": '010',
    "SUB": '011',
    "ADDI": '100',
}

array_table={
    "a0": '000',
    "a1": '001',
    "a2": '010',
    "a3": '011',
    "a4": '100'
}

reg_table={
    "r0": '000',
    "r1": '001', 
    "r2": '010',
    "r3": '011',
    "r4": '100'
}

def convert(instruction):
    writef = open('D:\Download\Cycle-accurate-simulator-for-5-stage-CPU-main\Cycle-accurate-simulator-for-5-stage-CPU-main\SIMD\/bin.txt', 'a')
    instr = instruction.split()
    print(instr)
    binins = []
    binins.append(table[instr[0]])
    if instr[0] == 'LD':
        binins.append(array_table[instr[1]])
        buff = bin(int(instr[2]))[2:]
        if len(buff) < 3:
            while len(buff) < 3:
                buff = '0'+buff
        binins.append(buff)
        for i in range(int(instr[2])):
            buff = bin(int(instr[i+3]))[2:]
        if len(buff) < 3:
            while len(buff) < 3:
                buff = '0'+buff
        binins.append(buff)
    if instr[0] == 'ADD' or instr[0] == 'SUB':
        binins.append(array_table[instr[1]])
        binins.append(array_table[instr[2]])
        binins.append(array_table[instr[3]])
    if instr[0] == 'ADDI':
        binins.append(array_table[instr[1]])
        binins.append(array_table[instr[2]])
        buff = bin(int(instr[3]))[2:]
        if len(buff) < 3:
            while len(buff) < 3:
                buff = '0'+buff
        binins.append(buff)
    if instr[0] == 'ST':
        buff = bin(int(instr[1][0]))[2:]
        if len(buff) < 3:
            while len(buff) < 3:
                buff = '0'+buff
        binins.append(buff)
        binins.append(array_table[instr[1][2:-1]])
        binins.append(reg_table[instr[2]])

    binstr = ''
    for i in binins:
        binstr = binstr+str(i)
    print(binstr)
    writef.write(binstr)
    writef.write('\n')

    # print(binins)


f = open('D:\Download\Cycle-accurate-simulator-for-5-stage-CPU-main\Cycle-accurate-simulator-for-5-stage-CPU-main\SIMD\simd_instructions.txt', 'r')
for i in f:
    convert(i)
