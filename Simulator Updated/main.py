from memory import memory_dict, memory_mapped_reg
from TABLES import opcode_to_instruction, registers, opcode_table
from cache_lru import *
from functions import *
from scoreboard import in_process, ready_state

sets = {
    0: {"ru": None, "data": [[None, None], [None, None]]},
    1: {"ru": None, "data": [[None, None], [None, None]]},
    2: {"ru": None, "data": [[None, None], [None, None]]},
    3: {"ru": None, "data": [[None, None], [None, None]]}
}

misses = 0
hits = 0
memory_accesses = 0

def update(addr, setno):
    global sets
    global misses
    global hits
    if sets[setno]["ru"] == None:
        # print("Miss")
        misses += 1
        value = memory_dict[addr]
        sets[setno]["data"][0][0] = addr
        sets[setno]["data"][0][1] = value
        sets[setno]["ru"] = 0
    else:
        if addr == sets[setno]["data"][0][0]:
            # print("Hit")
            hits += 1
            #print("before", sets[setno]["ru"])
            sets[setno]["ru"] = 0
            value = sets[setno]["data"][0][1]
            # print("after", sets[setno]["ru"])
        elif addr == sets[setno]["data"][1][0]:
            hits += 1
            #print("before", sets[setno]["ru"])
            sets[setno]["ru"] = 1
            value = sets[setno]["data"][0][1]
        else:
            # print("Miss")
            # print("before", sets[setno]["ru"])
            misses += 1
            upind = 1-sets[setno]["ru"]
            value = memory_dict[addr]
            sets[setno]["data"][upind][0] = addr
            sets[setno]["data"][upind][1] = value
            sets[setno]["ru"] = upind
            # print("after", sets[setno]["ru"])

    return [value]

registers_state = {
'R0': 0,
'R1': 0,
'R2': 0,
'R3': 0,
'R4': 0,
'R5': 0,
'R6': 0,
'R7': 0,
'R8': 0,
'R9': 0,
'R10': 0,
'R11': 0,
'R12': 0,
'R13': 0,
'R14': 0,
'R15': 0,
'R16': 0,
'R17': 0,
'R18': 0,
'R19': 0,
'R20': 0,
'R21': 0,
'R22': 0,
'R23': 0,
'R24': 0,
'R25': 0,
'R26': 0,
'R27': 0,
'R28': 0,
'R29': 0,
'R30': 0,
'R31': 0
}

temp_registers = {
    'R0': 0,
    'R1': 0,
    'R2': 0,
    'R3': 0,
    'R4': 0,
    'R5': 0,
    'R6': 0,
    'R7': 0,
    'R8': 0,
    'R9': 0,
    'R10': 0,
    'R11': 0,
    'R12': 0,
    'R13': 0,
    'R14': 0,
    'R15': 0,
    'R16': 0,
    'R17': 0,
    'R18': 0,
    'R19': 0,
    'R20': 0,
    'R21': 0,
    'R22': 0,
    'R23': 0,
    'R24': 0,
    'R25': 0,
    'R26': 0,
    'R27': 0,
    'R28': 0,
    'R29': 0,
    'R30': 0,
    'R31': 0
}

def read_binary_file(file_path):
    with open(file_path, "rb") as binary_file:
        binary_data = binary_file.read()
        instruction_size = 4
        num_instructions = len(binary_data) // instruction_size

        instructions = []
        for i in range(num_instructions):
            # Extract 4 bytes (32 bits) for each instruction
            instruction_bytes = binary_data[i *instruction_size: (i + 1) * instruction_size]
            # Convert the bytes to an integer and then to a binary string
            instruction_int = int.from_bytes(
                instruction_bytes, byteorder='big')
            instruction_binary = format(instruction_int, '032b')

            instructions.append(instruction_binary)
    return instructions


def signed_binary_to_decimal(binary_str):
    # Check if the number is negative (if the most significant bit is 1)
    is_negative = binary_str[0] == '1'

    # Convert binary string to decimal
    decimal_value = int(binary_str, 2)

    # If negative, adjust the value using two's complement
    if is_negative:
        decimal_value -= 2 ** len(binary_str)

    return decimal_value


def fetch(instructions, pc):
    return instructions[pc]


def decode(instruction):
    if instruction == "00000000000000000000000001111111":
        return "STORENOC", "N", -1, -1, -1, -1, -1, "STORENOC"
    opcode = instruction[-7:]
    func3_bits = -1
    func7_bits = -1
    operation = opcode_to_instruction[opcode]
    rs2 = -1
    rs1 = -1
    rd = -1
    shamt = -1
    imm = -1
    readable_format = ""
    if type(operation) == dict:
        func3_bits = instruction[32-14-1:32-12]
        operation = operation[func3_bits]
        if type(operation) == dict:
            func7_bits = instruction[32-31-1:32-25]
            operation = operation[func7_bits]
    operation_info = opcode_table[operation]
    instruction_type = operation_info[1]
    if instruction_type == "R":
        rs2 = registers[instruction[32-24-1:32-20]]
        rs1 = registers[instruction[32-19-1:32-15]]
        rd = registers[instruction[32-11-1:32-7]]
        readable_format = f"{operation} {rd} {rs1} {rs2}"
    elif instruction_type == "I":
        if operation == "SILLI" or operation == "SRLI" or operation == "SRAI":
            shamt = int(instruction[32-24-1:32-20], 2)
            rs1 = registers[instruction[32-19-1:32-15]]
            rd = registers[instruction[32-11-1:32-7]]
            readable_format = f"{operation} {rd} {rs1} {shamt}"
        else:
            imm = signed_binary_to_decimal(instruction[32-31-1:32-20])
            rs1 = registers[instruction[32-19-1:32-15]]
            rd = registers[instruction[32-11-1:32-7]]
            readable_format = f"{operation} {rd} {rs1} {imm}"
    elif instruction_type == "S":
        # imm = signed_binary_to_decimal(instruction[32-31-1]*20 + instruction[32-31-1:32-25] + instruction[32-11-1:32-7])
        imm = signed_binary_to_decimal(instruction[32-31-1:32-25] + instruction[32-11-1:32-7])
        rs2 = registers[instruction[32-24-1:32-20]]
        rs1 = registers[instruction[32-19-1:32-15]]
        readable_format = f"{operation} {rs1} {rs2} {imm}"
    elif instruction_type == "SB":
        # imm = signed_binary_to_decimal(instruction[32-31-1]*19 + instruction[32-31-1] + instruction[32-7-1] + instruction[32-30-1:32-25] + instruction[32-11-1:32-8] + "0")
        imm = signed_binary_to_decimal(instruction[32-31-1] + instruction[32-7-1] + instruction[32-30-1:32-25] + instruction[32-11-1:32-8])
        rs2 = registers[instruction[32-24-1:32-20]]
        rs1 = registers[instruction[32-19-1:32-15]]
        readable_format = f"{operation} {rs1} {rs2} {imm}"
    elif instruction_type == "U":
        imm = int(instruction[32-31-1:32-12]+"0"*12, 2)
        rd = registers[instruction[32-11-1:32-7]]
        readable_format = f"{operation} {rd} {imm}"
    elif instruction_type == "UJ":
        # imm = signed_binary_to_decimal(instruction[32-31-1]*11+instruction[32-31-1] +instruction[32-19-1:32-12] + instruction[32-20-1] + instruction[32-30-1:32-21] + "0")
        imm = signed_binary_to_decimal(instruction[32-31-1] +instruction[32-19-1:32-12] + instruction[32-20-1] + instruction[32-30-1:32-21])
        rd = registers[instruction[32-11-1:32-7]]
        readable_format = f"{operation} {rd} {imm}"

    return operation, instruction_type, rs2, rs1, rd, shamt, imm, readable_format


def execute(operation, instruction_type, rs2, rs1, rd, shamt, imm, register_state,temp_register,pc):
    result = -1
    new_pc = 1
    address = -1
    branch_taken = False
    updated_temp_registers={}
    for r in temp_register:
        updated_temp_registers[r] = temp_register[r]
    if instruction_type == "R":
        if operation == "ADD":
            result_op = add(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SUB":
            result_op = sub(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SLL":
            result_op = sll(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SLT":
            result_op = slt(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SLTU":
            result_op = sltu(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "XOR":
            result_op = xor(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SRL":
            result_op = srl(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SRA":
            result_op = sra(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "OR":
            result_op= or_(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "AND":
            result_op = and_(rd, rs1, rs2,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
    elif instruction_type == "I":
        if operation == "JALR":
            result_op = jalr(rd, rs1, imm, pc,temp_register)
            result = result_op[0]
            new_pc = result_op[1]
        elif operation == "LB":
            address = lb(rd, rs1, imm,temp_register)[0]
        elif operation == "LH":
            address = lh(rd, rs1, imm,temp_register)[0]
        elif operation == "LW":
            address = lw(rd, rs1, imm,temp_register)[0]
        elif operation == "LBU":
            address = lbu(rd, rs1, imm,temp_register)[0]
        elif operation == "LHU":
            address = lhu(rd, rs1, imm,temp_register)[0]
        elif operation == "ADDI":
            result_op = addi(rd, rs1, imm,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SLTI":
            result_op = slti(rd, rs1, imm,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SLTIU":
            result_op = sltiu(rd, rs1, imm,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "XORI":
            result_op = xori(rd, rs1, imm,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "ORI":
            result_op = ori(rd, rs1, imm,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "ANDI":
            result_op = andi(rd, rs1, imm,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SLLI":
            result_op = slli(rd, rs1, shamt,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SRLI":
            result_op = srli(rd, rs1, shamt,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "SRAI":
            result_op = srai(rd, rs1, shamt,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "LOADNOC":
            address = loadnoc(rd,rs1,imm,temp_register)[0]
    elif instruction_type == "S":
        if operation == "SB":
            result_op = sb(rs1, rs2, imm,temp_register)
            result = result_op[0]
            address = result_op[1]
        elif operation == "SH":
            result_op = sh(rs1, rs2, imm,temp_register)
            result = result_op[0]
            address = result_op[1]
        elif operation == "SW":
            result_op = sw(rs1, rs2, imm,temp_register)
            result = result_op[0]
            address = result_op[1]
    elif instruction_type == "SB":
        if operation == "BEQ":
            result_op = beq(rs1, rs2, imm, pc,temp_register)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BNE":
            result_op = bne(rs1, rs2, imm, pc,temp_register)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BLT":
            result_op = blt(rs1, rs2, imm, pc,temp_register)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BGE":
            result_op = bge(rs1, rs2, imm, pc,temp_register)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BLTU":
            result_op = bltu(rs1, rs2, imm, pc,temp_register)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BGEU":
            result_op = bgeu(rs1, rs2, imm, pc,temp_register)
            new_pc = result_op[0]
            branch_taken = result_op[1]
    elif instruction_type == "U":
        if operation == "LUI":
            result_op = lui(rd, imm,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]
        elif operation == "AUIPC":
            result_op = auipc(rd, imm, pc,temp_register)
            result = result_op[0]
            updated_temp_registers = result_op[1]

    return result, int(new_pc), address, branch_taken,register_state,updated_temp_registers


def memory(address, result, rd, instruction_type,register_state,temp_register):
    global memory_accesses
    updated_temp_registers={}
    for r in temp_register:
        updated_temp_registers[r] = temp_register[r]
    if instruction_type=="N":
        memory_mapped_reg[3]=1
        memory_accesses +=1
        return ["Done",register_state,updated_temp_registers]
    if address>=4096:
        value = update(address,address//4)[0]
        memory_mapped_reg[rd] = value
        memory_accesses +=1
        return ["Done",register_state,updated_temp_registers]
    else:
        if address != -1 and instruction_type == "S":
            memory_dict[address] = result
            memory_accesses += 1
            update(address,address//4)
            return ["Done",register_state,updated_temp_registers]
        elif address != -1 and instruction_type == "I":
            value = update(address,address//4)[0]
            print(sets)
            result= value
            updated_temp_registers[rd] = result
            memory_accesses +=1
            return ["Done",register_state,updated_temp_registers]
        else:
            return ["NOP",register_state,updated_temp_registers]

def writeback(temp_register):
    global registers_state
    # global temp_registers
    # for add in temp_register:
    #     temp_registers[add] = temp_register[add]
    for address in registers_state:
        registers_state[address] = temp_register[address]
    # for r in temp_register:
    #     temp_registers[r] = temp_register[r]
    return "COMPLETED"


def simulate(instructions):
    pc_flag = False
    pc = 0
    new_pc = 0
    clock_cycle = 0
    branch_taken = False
    dead_branches = 0
    stall = False
    pipeline = {"F": "", "D": "", "X": "", "M": "", "W": ""}
    mid_stall = False
    memory_stall_operations = {}
    I_flag = False
    with open("simulation.log", "w") as file1:
        while True: 
            global registers_state
            global temp_registers
            file1.write("-"*50+"CLOCK CYCLE: "+str(clock_cycle)+" "+"-"*50+"\n")
            if pc >= len(instructions):
                pipeline["F"] = ""
            if pipeline["W"] != "":
                # status, address, instruction_type,register_state,temp_register,rd, i_pc = pipeline["W"]
                status, address, instruction_type,rd, i_pc = pipeline["W"]
                w_status = writeback(temp_registers)
                pipeline["W"] = [w_status, i_pc]
            if pipeline["M"] != "":
                if pipeline["M"][0]!="STORENOC":
                    # result, new_pc, address,branch_taken, rd, instruction_type,register_state,temp_register,i_pc = pipeline["M"]
                    result, new_pc, address,branch_taken, rd, instruction_type,i_pc = pipeline["M"]
                    if I_flag == True:
                        if address != -1 and instruction_type != "S" and instruction_type != "SB" and rd in in_process:
                            in_process.remove(rd)
                            ready_state.add(rd)
                        if rs1 in in_process or rs2 in in_process:
                            stall = True
                        else:
                            stall = False
                    status,register_state,temp_register = memory(address, result, rd, instruction_type,registers_state,temp_registers)
                    # for r in registers_state:
                    #     registers_state[r] = register_state[r]
                    for r in temp_registers:
                        temp_registers[r] = temp_register[r]
                    # pipeline["M"] = [status, address, instruction_type,register_state,temp_register,rd, i_pc]
                    pipeline["M"] = [status, address, instruction_type,rd, i_pc]
                else:
                    status,register_state,temp_register = memory(-1, -1, -1, "N",registers_state,temp_registers)
                    for r in temp_registers:
                        temp_registers[r] = temp_register[r]
                    # pipeline["M"] = [status, -1, "N",register_state,temp_register,-1,pipeline["M"][-1]]
                    pipeline["M"] = [status, -1, "N",-1,pipeline["M"][-1]]

            if pipeline["X"] != "":
                operation, instruction_type, rs2, rs1, rd, shamt, imm, readable_format,i_pc = pipeline["X"]
                if operation!="STORENOC":
                    # result, new_pc, address, branch_taken,register_state,temp_register= execute(operation, instruction_type, rs2, rs1, rd, shamt, imm, register_state,temp_register,i_pc)
                    result, new_pc, address, branch_taken,register_state,temp_register= execute(operation, instruction_type, rs2, rs1, rd, shamt, imm, registers_state,temp_registers,i_pc)
                    # for r in registers_state:
                    #     registers_state[r] = register_state[r]
                    for r in temp_register:
                        temp_registers[r] = temp_register[r]
                    if I_flag == True:
                        if instruction_type != "I" and instruction_type != "S" and instruction_type != "SB" and rs1 not in in_process and rs2 not in in_process:
                            in_process.remove(rd)
                            ready_state.add(rd)
                    pc_flag = True
                    if branch_taken == True:
                        dead_branches = (imm//4)-1
                    # pipeline["X"] = [result, new_pc, address,branch_taken, rd, instruction_type,register_state,temp_register,i_pc]
                    pipeline["X"] = [result, new_pc, address,branch_taken, rd, instruction_type,i_pc]
                else:
                    pipeline["X"] = ["STORENOC",register_state,temp_register,i_pc]
            if pipeline["D"] != "" and stall == False:
                try:
                    operation, instruction_type, rs2, rs1, rd, shamt, imm, readable_format = decode(pipeline["D"][0])
                    # register_state = pipeline["D"][1]
                    # temp_register = pipeline["D"][2]
                    i_pc = pipeline["D"][1]
                except:
                    # operation, instruction_type, rs2, rs1, rd, shamt, imm, readable_format,register_state,temp_register,i_pc = pipeline["D"]
                    operation, instruction_type, rs2, rs1, rd, shamt, imm, readable_format,i_pc = pipeline["D"]
                if operation in ['LB', 'LH', 'LW', 'LBU', 'LHU']:
                    I_flag = True
                if I_flag == True:
                    if rs2 in in_process or rs1 in in_process:
                        stall = True
                    if instruction_type != "S" and instruction_type != "SB" and rd not in ready_state and rd != rs2 and rd != rs1:
                        in_process.add(rd)
                # pipeline["D"] = [operation, instruction_type, rs2,rs1, rd, shamt, imm, readable_format,register_state,temp_register,i_pc]
                pipeline["D"] = [operation, instruction_type, rs2,rs1, rd, shamt, imm, readable_format,i_pc]

            if pc < len(instructions) and stall == False:
                # pipeline["F"] = [fetch(instructions, pc), registers_state,temp_registers,pc]
                pipeline["F"] = [fetch(instructions, pc),pc]
                if pc_flag == False:
                    pc += 1
                elif new_pc > pc:
                    pc = new_pc
                else:
                    pc += 1
                # if mid_stall==True:
                #     stall = True
            keys = list(pipeline.keys())
            clock_cycle += 1
            #print(pipeline)
            for stages in pipeline:
                if pipeline[stages] != "":
                    if stages=="F":
                        file1.write("F: "+str(pipeline["F"][-1])+" "+str(pipeline["F"][0])+" \n")
                    elif stages=="D":
                        file1.write("D: "+str(pipeline["D"][-1])+" "+str(pipeline["D"][7])+" \n")
                    elif stages=="X":
                        if pipeline["X"][0]!="STORENOC":
                            file1.write("X: "+str(pipeline["X"][-1])+" Result: "+str(pipeline["X"][0])+" Instruction Type: "+str(pipeline["X"][5])+" \n")
                        else:
                            file1.write("X: STORENOC \n")
                    elif stages=="M":
                        file1.write("M: "+str(pipeline["M"][-1])+" "+str(pipeline["M"][0])+" \n")
                    elif stages=="W":
                        file1.write("W: "+str(pipeline["W"][-1])+" "+str(pipeline["W"][0])+" \n")
                else:
                    file1.write(stages+":  \n")
            # file1.write("\n")
            file1.write("Registers in process: "+ str(in_process)+"\n")
            file1.write("Registers in ready state: "+ str(ready_state)+"\n")
            file1.write("Registers Sate \n"+str(registers_state)+"\n")
            file1.write("Memory Mapped Registers: \n"+str(memory_mapped_reg)+"\n")
            file1.write("Memory State\n"+str(memory_dict)+"\n")
            file1.write("Cache: \n")
            file1.write(str(sets)+"\n")
            file1.write("Hits: "+str(hits)+" Misses: "+str(misses)+"\n")
            file1.write("Memory Accesses: "+str(memory_accesses)+"\n")
            # Shift values to the next key
            if stall == False:
                for i in range(len(keys) - 1, 0, -1):
                    pipeline[keys[i]] = pipeline[keys[i - 1]]
            else:
                for i in range(len(keys) - 1, 2, -1):
                    pipeline[keys[i]] = pipeline[keys[i - 1]]
                pipeline["X"] = ""
            all_empty = all(value == "" for value in pipeline.values())
            if all_empty:
                break
            if branch_taken == True:
                branch_taken = False
                removed_c = 0
                if dead_branches == 1:
                    pipeline["X"] = ""
                elif dead_branches > 1:
                    for i in range(2, 0, -1):
                        if removed_c != dead_branches:
                            pipeline[keys[i]] = ""
                        else:
                            break
                dead_branches = 0

def main():
    file_path = input()
    instructions = read_binary_file(file_path)
    simulate(instructions)
    print("TOTAL MISSES",misses)
    print("TOTAL HITS",hits)
    print("TOTAL MEMORY ACCESSES",memory_accesses)
main()
