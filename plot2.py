log_file = "./simulation.log"

with open(log_file, 'r') as file:
    lines = file.readlines()

def read_instruction_memory_access(lines):
    instruction_memory_access = []
    clock_cycle = []
    for line in lines:
        if "Memory Access (Instruction)" in line:
            instruction_memory_access.append(int(line.split(":")[1]))
            clock_cycle.append(int(line.split(":")[0]))
    return instruction_memory_access, clock_cycle

def read_data_memory_access(lines):
    data_memory_access = []
    clock_cycle = []
    for line in lines:
        if "Memory Access (Data)" in line:
            data_memory_access.append(int(line.split(":")[1]))
            clock_cycle.append(int(line.split(":")[0]))
    return data_memory_access, clock_cycle

def read_type_of_instruction(lines):
    type_of_instruction = []
    clock_cycle = []
    for line in lines:
        if "Type of Instruction" in line:
            type_of_instruction.append(line.split(":")[1])
            clock_cycle.append(int(line.split(":")[0]))
    return type_of_instruction, clock_cycle

def read_data_stalls(lines):
    data_stalls = []
    clock_cycle = []
    for line in lines:
        if "Data Stall" in line:
            data_stalls.append(int(line.split(":")[1]))
            clock_cycle.append(int(line.split(":")[0]))
    return data_stalls, clock_cycle

instruction_memory_access, clock_cycle = read_instruction_memory_access(lines)
data_memory_access, clock_cycle2 = read_data_memory_access(lines)
type_of_instruction, clock_cycle3 = read_type_of_instruction(lines)