import matplotlib.pyplot as plt

log_file = "./simulation.log"

with open(log_file, 'r') as file:
    lines = file.readlines()

def read_instruction_memory_access(lines, total_cycles):
    instruction_memory_access = []
    clock_cycle = []
    total_instruction_memory_access = []
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

    for i in range(0, total_cycles + 1):
        if i in clock_cycle:
            index = clock_cycle.index(i)
            total_instruction_memory_access.append(instruction_memory_access[index])
        else:
            total_instruction_memory_access.append(0)

    return total_instruction_memory_access, clock_cycle

def read_data_memory_access(lines, total_cycles):
    data_memory_access = []
    clock_cycle = []
    total_data_memory_access = []

    for line in lines:
        if "CLOCK CYCLE: " in line:
            cycle = int(line.split(" ")[2])
        if "Memory Accesses: " in line:
            index = line.split(" ")
            data_memory_access.append(int(index[2]))
            clock_cycle.append(cycle)
    
    for i in range(0, total_cycles + 1):
        if i in clock_cycle:
            index = clock_cycle.index(i)
            total_data_memory_access.append(data_memory_access[index])
        else:
            total_data_memory_access.append(0)
    
    return total_data_memory_access, clock_cycle

def read_type_of_instruction(lines, total_cycles):
    type_of_instruction = []
    clock_cycle = []
    total_type_of_instruction = []

    for line in lines:
        if "CLOCK CYCLE: " in line:
            cycle = int(line.split(" ")[2])
        if "X: " in line:
            index = line.split(" ")
            if len(index) > 3:
                inst_type = index[6]
                type_of_instruction.append(inst_type)
                clock_cycle.append(cycle)
    
    for i in range(0, total_cycles + 1):
        if i in clock_cycle:
            index = clock_cycle.index(i)
            total_type_of_instruction.append(type_of_instruction[index])
        else:
            total_type_of_instruction.append(0)
    
    return total_type_of_instruction, clock_cycle

def read_data_stalls(lines, total_cycles):
    check_f, check_stall, check_w = False, False, False
    data_stalls = []
    clock_cycle = []
    total_data_stalls = []

    for line in lines:
        if "CLOCK CYCLE: " in line:
            cycle = int(line.split(" ")[2])
        if "F: " in line:
            index = line.split(" ")
            if len(index) > 3:
                check_f = True
            else:
                check_f = False
        if "D: " in line or "X: " in line or "M: " in line:
            index = line.split(" ")
            if len(index) == 3 and index[1] == '':
                check_stall = True
        if "W: " in line:
            index = line.split(" ")
            if len(index) > 3:
                check_w = True
            else:
                check_w = False
        if check_f and check_stall and check_w:
            data_stalls.append(1)
            clock_cycle.append(cycle)
            check_f = False
            check_stall = False
            check_w = False
    
    for i in range(0, total_cycles + 1):
        if i in clock_cycle:
            index = clock_cycle.index(i)
            total_data_stalls.append(data_stalls[index])
        else:
            total_data_stalls.append(0)
    
    return total_data_stalls, clock_cycle

def read_hit_and_miss(lines, total_cycles):
    hits = []
    misses = []
    clock_cycle = []
    total_hits = []
    total_misses = []

    for line in lines:
        if "CLOCK CYCLE: " in line:
            cycle = int(line.split(" ")[2])
        if "Hits: " in line:
            index = line.split(" ")
            hits.append(int(index[1]))
            misses.append(int(index[3]))
            clock_cycle.append(cycle)
    
    for i in range(0, total_cycles + 1):
        if i in clock_cycle:
            index = clock_cycle.index(i)
            total_hits.append(hits[index])
            total_misses.append(misses[index])
        else:
            total_hits.append(0)
            total_misses.append(0)
    
    return total_hits, total_misses, clock_cycle

def calculate_total_cycles(lines):
    total = 0
    for line in lines:
        if "CLOCK CYCLE: " in line:
            total += 1
    return total

total_cycles = calculate_total_cycles(lines)
total_instruction_memory_access, clock_cycle = read_instruction_memory_access(lines, total_cycles)
total_data_memory_access, clock_cycle2 = read_data_memory_access(lines, total_cycles)
total_type_of_instruction, clock_cycle3 = read_type_of_instruction(lines, total_cycles)
total_data_stalls, clock_cycle4 = read_data_stalls(lines, total_cycles)
total_hits, total_misses, clock_cycle5 = read_hit_and_miss(lines, total_cycles)

print("Total Cycles: ", total_cycles)

# ############
# # PLOTTING #
# ############

print("Instruction Memory Access Plot")
print("Instruction Memory Access List: ")
print(total_instruction_memory_access)
print("Clock Cycles: ")
print(clock_cycle)

print("Data Memory Access Plot")
print("Data Memory Access List: ")
print(total_data_memory_access)
print("Clock Cycles: ")
print(clock_cycle2)

# Create subplots for Instruction Memory Access and Data Memory Access
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
# Instruction Memory Access plot
ax1.plot(range(0, total_cycles + 1), total_instruction_memory_access, marker='o', linestyle='-', color='blue')
ax1.set_xlabel('Clock Cycle')
ax1.set_ylabel('Instruction Memory Access')
ax1.set_title('Instruction Memory Access Plot')
ax1.grid(True)
# Data Memory Access plot
ax2.plot(range(0, total_cycles + 1), total_data_memory_access, marker='o', linestyle='-', color='green')
ax2.set_xlabel('Clock Cycle')
ax2.set_ylabel('Data Memory Access')
ax2.set_title('Data Memory Access Plot')
ax2.grid(True)
# Adjust layout
plt.tight_layout()
plt.show()

print("Type of Instructions Plot")
print("Instruction Memory Access List: ")
print(total_type_of_instruction)
print("Clock Cycles: ")
print(clock_cycle3)
# Type of Instructions Plot
plt.figure(figsize=(10, 6))
plt.hist(total_type_of_instruction, bins=len(set(total_type_of_instruction)), color='orange')
plt.xlabel('Type of Instructions')
plt.ylabel('Frequency')
plt.title('Type of Instructions Plot')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()


print("Data Stalling Plot")
print("Data Stall List: ")
print(total_data_stalls)
print("Clock Cycles: ")
print(clock_cycle4)
# Data Stalling Plot
plt.figure(figsize=(10, 6))
plt.plot(range(0, total_cycles + 1), total_data_stalls, marker='o', linestyle='-', color='red')
plt.xlabel('Clock Cycle')
plt.ylabel('Data Stalls')
plt.title('Data Stalling Plot')
plt.grid(True)
plt.show()

print("Hit and Miss Plot")
print("Hit List: ")
print(total_hits)
print("Miss List: ")
print(total_misses)
print("Clock Cycles: ")
print(clock_cycle5)
# Hit and Miss Plot
plt.figure(figsize=(10, 6))
plt.plot(range(0, total_cycles + 1), total_hits, marker='o', linestyle='-', color='blue', label='Hits')
plt.plot(range(0, total_cycles + 1), total_misses, marker='o', linestyle='-', color='red', label='Misses')
plt.xlabel('Clock Cycle')
plt.ylabel('Hits/Misses')
plt.title('Hit and Miss Plot')
plt.legend()
plt.grid(True)
plt.show()