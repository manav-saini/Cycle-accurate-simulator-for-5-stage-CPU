log_file_path = "/Users/manavsaini/Documents/GitHub/Cycle-accurate-simulator-for-5-stage-CPU/simulation.log"
test_file_path = "/Users/manavsaini/Documents/GitHub/Cycle-accurate-simulator-for-5-stage-CPU/assembly_stall.txt"


number_of_instructions = 0

with open(test_file_path, 'r') as test_file:
    for line in test_file:
        number_of_instructions+=1

instructions_count={}
clock_cycle_memory_access = {}
clock_cycle_hits = {}
clock_cycle_misses = {}
clock_cycle_stall = {}
pc_f = []
pc_x=[]
pc_d =[]
clock_cycle_fetch = {}
register_instruction = 0
memory_instruction = 0
instructions = []
clock_cycle_stall = {}



with open(log_file_path, 'r') as log_file:
    cc = "-1"
    # Read the file line by line
    for line in log_file:
        # Process each line as needed
        line= line.strip()
        if line[0]=="-":
            space_tokens = line.split(" ")
            cc = space_tokens[2]
            clock_cycle_memory_access[cc] = 0
            clock_cycle_hits[cc] = 0
            clock_cycle_misses[cc] = 0
            clock_cycle_stall[cc] = 0
        else:
            stripped_line = line.strip()
            line_tokens = line.split(": ")
            if line_tokens[0] == "F":
                sub_space_tokens = line_tokens[1].split(" ")
                if sub_space_tokens[0] not in pc_f:
                    pc_f.append(sub_space_tokens[0])
                    clock_cycle_fetch[cc] = 1
            if line_tokens[0] == "D":
                sub_space_tokens = line_tokens[1].split(" ")
                if sub_space_tokens[0] not in pc_d:
                    pc_d.append(sub_space_tokens[0])
                    instruction_op = sub_space_tokens[1]
                    instructions.append(instruction_op)
                else:
                    clock_cycle_stall[cc] = 1
            elif line_tokens[0]=="X":
                sub_space_tokens = line_tokens[1].split(" ")
                if sub_space_tokens[0] not in pc_x:
                    pc_x.append(sub_space_tokens[0])
                    instruction_type = line_tokens[-1]
                    if instruction_type in instructions_count:
                        instructions_count[instruction_type] +=1
                    else:
                        instructions_count[instruction_type] = 1
            elif line_tokens[0]=="Hits":
                print(line_tokens)
                # print(sub_space_tokens)
                clock_cycle_hits[cc] = line_tokens[1][0]
                # print(sub_space_tokens)
                clock_cycle_misses[cc] = line_tokens[-1]
            elif line_tokens[0]=="Memory Accesses":
                clock_cycle_memory_access[cc] = line_tokens[1]

mem_instr = ["LB","LH","LW","LBU","LHU","SB","SH","SW","STORENOC","LOADNOC"]
for instr in instructions:
    if instr in mem_instr:
        memory_instruction += 1
    else:
        register_instruction += 1

print(instructions_count)
print(clock_cycle_memory_access)
print(clock_cycle_hits)
print(clock_cycle_misses)
print(clock_cycle_stall)
print(clock_cycle_fetch)
print(instructions)
print(memory_instruction)
print(register_instruction)

import matplotlib.pyplot as plt
def plot_dictionary(dictionary, title):
    keys = list(dictionary.keys())
    values = list(dictionary.values())

    plt.figure(figsize=(10, 6))
    plt.bar(keys, values, color='skyblue')
    plt.xlabel('Instructions')
    plt.ylabel('Values')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Plot each dictionary


mem_reg_value = {"Memory Instruction":memory_instruction,"Register_instruction":register_instruction}

for i in range(int(cc)+1):
    if str(i) not in clock_cycle_memory_access:
        clock_cycle_memory_access[str(i)] = 0
    if str(i) not in clock_cycle_hits:
        clock_cycle_hits[str(i)] = 0
    if str(i) not in clock_cycle_misses:
        clock_cycle_misses[str(i)] = 0
    if str(i) not in clock_cycle_stall:
        clock_cycle_stall[str(i)] = 0
    if str(i) not in clock_cycle_fetch:
        clock_cycle_fetch[str(i)] = 0

clock_cycle_fetch_updated = {}

for i in range(int(cc)+1):
    clock_cycle_fetch_updated[str(i)] = clock_cycle_fetch[str(i)]

plot_dictionary(instructions_count, 'Instructions Count')
plot_dictionary(clock_cycle_memory_access, 'Memory Access')
plot_dictionary(clock_cycle_hits, 'Clock Cycle Hits')
plot_dictionary(clock_cycle_misses, 'Clock Cycle Misses')
plot_dictionary(clock_cycle_stall, 'Clock Cycle Stall')
plot_dictionary(clock_cycle_fetch_updated, 'Instruction Access')
plot_dictionary(mem_reg_value, 'Memory Instruction vs Register Instructions')


    

