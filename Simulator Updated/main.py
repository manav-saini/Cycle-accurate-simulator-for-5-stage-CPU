from memory import memory_dict, memory_mapped_reg
from TABLES import opcode_to_instruction, registers, opcode_table, type_table
from registerfile import temp_registers, registers_state
from functions import *
from scoreboard import in_process, ready_state


def read_binary_file(file_path):
    with open(file_path, "rb") as binary_file:
        binary_data = binary_file.read()
        instruction_size = 4
        num_instructions = len(binary_data) // instruction_size

        instructions = []
        for i in range(num_instructions):
            # Extract 4 bytes (32 bits) for each instruction
            instruction_bytes = binary_data[i *
                                            instruction_size: (i + 1) * instruction_size]

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
        imm = signed_binary_to_decimal(
            instruction[32-31-1]*20 + instruction[32-31-1:32-25] + instruction[32-11-1:32-7])
        rs2 = registers[instruction[32-24-1:32-20]]
        rs1 = registers[instruction[32-19-1:32-15]]
        readable_format = f"{operation} {rs1} {rs2} {imm}"
    elif instruction_type == "SB":
        # imm = signed_binary_to_decimal(instruction[32-31-1]*19 + instruction[32-31-1] + instruction[32-7-1] + instruction[32-30-1:32-25] + instruction[32-11-1:32-8] + "0")
        imm = signed_binary_to_decimal(
            instruction[32-31-1] + instruction[32-7-1] + instruction[32-30-1:32-25] + instruction[32-11-1:32-8])
        rs2 = registers[instruction[32-24-1:32-20]]
        rs1 = registers[instruction[32-19-1:32-15]]
        readable_format = f"{operation} {rs1} {rs2} {imm}"
    elif instruction_type == "U":
        imm = int(instruction[32-31-1:32-12]+"0"*12, 2)
        rd = registers[instruction[32-11-1:32-7]]
        readable_format = f"{operation} {rd} {imm}"
    elif instruction_type == "UJ":
        imm = signed_binary_to_decimal(instruction[32-31-1]*11+instruction[32-31-1] +
                                       instruction[32-19-1:32-12] + instruction[32-20-1] + instruction[32-30-1:32-21] + "0")
        rd = registers[instruction[32-11-1:32-7]]
        readable_format = f"{operation} {rd} {imm}"

    return operation, instruction_type, rs2, rs1, rd, shamt, imm, readable_format


def execute(operation, instruction_type, rs2, rs1, rd, shamt, imm, pc):
    result = -1
    new_pc = 1
    address = -1
    branch_taken = False
    if instruction_type == "R":
        if operation == "ADD":
            result = add(rd, rs1, rs2)[0]
        elif operation == "SUB":
            result = sub(rd, rs1, rs2)[0]
        elif operation == "SLL":
            result = sll(rd, rs1, rs2)[0]
        elif operation == "SLT":
            result = slt(rd, rs1, rs2)[0]
        elif operation == "SLTU":
            result = sltu(rd, rs1, rs2)[0]
        elif operation == "XOR":
            result = xor(rd, rs1, rs2)[0]
        elif operation == "SRL":
            result = srl(rd, rs1, rs2)[0]
        elif operation == "SRA":
            result = sra(rd, rs1, rs2)[0]
        elif operation == "OR":
            result = or_(rd, rs1, rs2)[0]
        elif operation == "AND":
            result = and_(rd, rs1, rs2)[0]
    elif instruction_type == "I":
        if operation == "JALR":
            result_op = jalr(rd, rs1, imm, pc)
            result = result_op[0]
            new_pc = result_op[1]
        elif operation == "LB":
            address = lb(rd, rs1, imm)[0]
        elif operation == "LH":
            address = lh(rd, rs1, imm)[0]
        elif operation == "LW":
            address = lw(rd, rs1, imm)[0]
        elif operation == "LBU":
            address = lbu(rd, rs1, imm)[0]
        elif operation == "LHU":
            address = lhu(rd, rs1, imm)[0]
        elif operation == "ADDI":
            address = addi(rd, rs1, imm)[0]
        elif operation == "SLTI":
            address = slti(rd, rs1, imm)[0]
        elif operation == "SLTIU":
            address = sltiu(rd, rs1, imm)[0]
        elif operation == "XORI":
            address = xori(rd, rs1, imm)[0]
        elif operation == "ORI":
            address = ori(rd, rs1, imm)[0]
        elif operation == "ANDI":
            address = andi(rd, rs1, imm)[0]
        elif operation == "SLLI":
            address = slli(rd, rs1, shamt)[0]
        elif operation == "SRLI":
            address = srli(rd, rs1, shamt)[0]
        elif operation == "SRAI":
            address = srai(rd, rs1, shamt)[0]
    elif instruction_type == "S":
        if operation == "SB":
            result_op = sb(rs1, rs2, imm)
            result = result_op[0]
            address = result_op[1]
        elif operation == "SH":
            result_op = sh(rs1, rs2, imm)
            result = result_op[0]
            address = result_op[1]
        elif operation == "SW":
            result_op = sw(rs1, rs2, imm)
            result = result_op[0]
            address = result_op[1]
        elif operation == "LOADNOC":
            loadnoc(rs2, rs1, imm)
    elif instruction_type == "SB":
        if operation == "BEQ":
            result_op = beq(rs1, rs2, imm, pc)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BNE":
            result_op = bne(rs1, rs2, imm, pc)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BLT":
            result_op = blt(rs1, rs2, imm, pc)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BGE":
            result_op = bge(rs1, rs2, imm, pc)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BLTU":
            result_op = bltu(rs1, rs2, imm, pc)
            new_pc = result_op[0]
            branch_taken = result_op[1]
        elif operation == "BGEU":
            result_op = bgeu(rs1, rs2, imm, pc)
            new_pc = result_op[0]
            branch_taken = result_op[1]
    elif instruction_type == "U":
        if operation == "LUI":
            result = lui(rd, imm)[0]
        elif operation == "AUIPC":
            result = auipc(rd, imm, pc)[0]
    if operation == "STORENOC":
        storenoc()

    return result, int(new_pc), address, branch_taken


def memory(address, result, rd, instruction_type):
    if address != -1 and instruction_type == "S":
        memory_dict[address] = result
    elif address != -1 and instruction_type == "I":
        memory_dict[address] = result
        temp_registers[rd] = result
        return ("Done")
    else:
        return ("NOP")


def writeback():
    for address in temp_registers:
        registers_state[address] = temp_registers[address]

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
    while True:
        print("-"*50+"CLOCK CYCLE: "+str(clock_cycle)+" "+"-"*50)
        if pc >= len(instructions):
            pipeline["F"] = ""
        if pipeline["W"] != "":
            status, address, instruction_type, rd, i_pc = pipeline["W"]
            w_status = writeback()
            pipeline["W"] = [w_status, i_pc]
        if pipeline["M"] != "":
            result, new_pc, address, branch_taken, rd, instruction_type, i_pc = pipeline["M"]
            if I_flag == True:
                if address != -1 and instruction_type != "S" and instruction_type != "SB" and rd in in_process:
                    # print(rd)
                    in_process.remove(rd)
                    ready_state.add(rd)
                if rs1 in in_process or rs2 in in_process:
                    stall = True
                else:
                    stall = False
            status = memory(address, result, rd, instruction_type)
            pipeline["M"] = [status, address, instruction_type, rd, i_pc]
        if pipeline["X"] != "":
            operation, instruction_type, rs2, rs1, rd, shamt, imm, readable_format, i_pc = pipeline[
                "X"]
            result, new_pc, address, branch_taken = execute(
                operation, instruction_type, rs2, rs1, rd, shamt, imm, i_pc)
            if I_flag == True:
                if instruction_type != "I" and instruction_type != "S" and instruction_type != "SB" and rs1 not in in_process and rs2 not in in_process:
                    in_process.remove(rd)
                    ready_state.add(rd)
            pc_flag = True
            if branch_taken == True:
                dead_branches = (imm//4)-1
            pipeline["X"] = [result, new_pc, address,
                             branch_taken, rd, instruction_type, i_pc]
        if pipeline["D"] != "" and stall == False:
            try:
                operation, instruction_type, rs2, rs1, rd, shamt, imm, readable_format = decode(
                    pipeline["D"][0])
                i_pc = pipeline["D"][1]
            except:
                operation, instruction_type, rs2, rs1, rd, shamt, imm, readable_format, i_pc = pipeline[
                    "D"]
            print(operation)
            if operation in ['LB', 'LH', 'LW', 'LBU', 'LHU']:
                I_flag = True
            if I_flag == True:
                if rs2 in in_process or rs1 in in_process:
                    stall = True
                if instruction_type != "S" and instruction_type != "SB" and rd not in ready_state and rd != rs2 and rd != rs1:
                    in_process.add(rd)
            pipeline["D"] = [operation, instruction_type, rs2,
                             rs1, rd, shamt, imm, readable_format, i_pc]
        if pc < len(instructions) and stall == False:
            pipeline["F"] = [fetch(instructions, pc), pc]
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
        # print(pipeline)
        for stages in pipeline:
            try:
                print(stages+": " +
                      str(pipeline[stages][len(pipeline[stages])-1]))
            except:
                print(stages+": ")
        print("\n")
        print(in_process)
        print(ready_state)
        print("\n")
        print(registers_state)
        print("\n")
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
    file_path = "/Users/manavsaini/Documents/Assembler Simulator/output.bin"
    instructions = read_binary_file(file_path)
    simulate(instructions)


main()
