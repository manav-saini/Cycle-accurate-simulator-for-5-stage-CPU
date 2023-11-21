log_file = "./simulation.log"

with open(log_file, 'r') as file:
    lines = file.readlines()

def read_instruction_memory_access(lines):
    instruction_memory_access = []
    clock_cycle = []
    instruction_dict = {}

    for line in lines:
        if "CLOCK CYCLE: " in line:
            cycle = int(line.split(" ")[2])
        if "F: " in line:
            index = line.split(" ")
            if len(index) > 3:
                inst = int(index[1])

                # Check if the instruction is encountered before
                if inst not in instruction_dict:
                    instruction_memory_access.append(inst)
                    clock_cycle.append(cycle)
                    instruction_dict[inst] = cycle  # Store the latest cycle for this instruction
                else:
                    # If encountered again, compare the cycle and update if the new cycle is earlier
                    if cycle < instruction_dict[inst]:
                        idx = instruction_memory_access.index(inst)
                        clock_cycle[idx] = cycle
                        instruction_dict[inst] = cycle
    return instruction_memory_access, clock_cycle

def read_data_memory_access(lines):
    data_memory_access = []
    clock_cycle = []
    data_dict = {}

    for line in lines:
        if "CLOCK CYCLE: " in line:
            cycle = int(line.split(" ")[2])
        if "M: " in line:
            index = line.split(" ")
            if len(index) > 3 and index[2] == "Done":
                inst = int(index[1])

                # Check if the data memory access is encountered before
                if inst not in data_dict:
                    data_memory_access.append(inst)
                    clock_cycle.append(cycle)
                    data_dict[inst] = cycle  # Store the latest cycle for this data memory access
                else:
                    # If encountered again, compare the cycle and update if the new cycle is earlier
                    if cycle < data_dict[inst]:
                        idx = data_memory_access.index(inst)
                        clock_cycle[idx] = cycle
                        data_dict[inst] = cycle

    return data_memory_access, clock_cycle

def read_type_of_instruction(lines):
    type_of_instruction = []
    clock_cycle = []
    for line in lines:
        if "CLOCK CYCLE: " in line:
            cycle = int(line.split(" ")[2])
        if "X: " in line:
            index = line.split(" ")
            if len(index) > 3:
                inst_type = index[6]
                type_of_instruction.append(inst_type)
                clock_cycle.append(cycle)
    return type_of_instruction, clock_cycle

def read_data_stalls(lines):
    data_stalls = []
    clock_cycle = []
    for line in lines:
        if "Data Stall" in line:
            data_stalls.append(int(line.split(":")[1]))
            clock_cycle.append(int(line.split(":")[0]))
    return data_stalls, clock_cycle

def calculate_total_cycles(lines):
    total = 0
    for line in lines:
        if "CLOCK CYCLE: " in line:
            total += 1
    return total

total_cycles = calculate_total_cycles(lines)
instruction_memory_access, clock_cycle = read_instruction_memory_access(lines)
data_memory_access, clock_cycle2 = read_data_memory_access(lines)
type_of_instruction, clock_cycle3 = read_type_of_instruction(lines)
data_stalls, clock_cycle4 = read_data_stalls(lines)

print(total_cycles)
# print(instruction_memory_access, clock_cycle)
# print(data_memory_access, clock_cycle2)
# print(type_of_instruction, clock_cycle3)
# print(data_stalls, clock_cycle4)