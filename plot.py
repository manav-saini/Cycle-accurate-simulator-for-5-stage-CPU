import re
import matplotlib.pyplot as plt

# Function to extract data from the log file
def extract_data(log_file):
    with open(log_file, 'r') as file:
        lines = file.readlines()

    memory_access_instruction = []
    memory_access_data = []
    instruction_types = []
    data_stalls = []

    # Regular expressions for extracting relevant information
    memory_access_instr_pattern = re.compile(r'Memory: (\d+)')
    memory_access_data_pattern = re.compile(r'Memory: (\d+)')
    instruction_type_pattern = re.compile(r'Registers State: (.+)')
    data_stall_pattern = re.compile(r'Data Stall: (\d+)')

    for line in lines:
        # Extract memory access (instruction and data)
        memory_instr_match = memory_access_instr_pattern.search(line)
        memory_data_match = memory_access_data_pattern.search(line)
        if memory_instr_match:
            memory_access_instruction.append(int(memory_instr_match.group(1)))
        if memory_data_match:
            memory_access_data.append(int(memory_data_match.group(1)))

        # Extract instruction types
        instruction_type_match = instruction_type_pattern.search(line)
        if instruction_type_match:
            instruction_types.append(instruction_type_match.group(1))

        # Extract data stalls
        data_stall_match = data_stall_pattern.search(line)
        if data_stall_match:
            data_stalls.append(int(data_stall_match.group(1)))

    return memory_access_instruction, memory_access_data, instruction_types, data_stalls

# Provide the path to your log file
log_file_path = 'simulation.log'

# Extract data from the log file
memory_access_instruction, memory_access_data, instruction_types, data_stalls = extract_data(log_file_path)

# Plotting graphs
# Memory Access (Instruction and Data)
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(memory_access_instruction, label='Memory Access (Instruction)', color='blue')
plt.xlabel('Clock Cycle')
plt.ylabel('Memory Access')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(memory_access_data, label='Memory Access (Data)', color='green')
plt.xlabel('Clock Cycle')
plt.ylabel('Memory Access')
plt.legend()

plt.tight_layout()
plt.show()

# Types of Instructions (from the log file)
# Extracting instruction types from the log file content
instruction_types = [instruction.split(':')[-1].strip() for instruction in instruction_types]

# Plotting instruction types
plt.figure(figsize=(8, 6))
plt.hist(instruction_types, bins=20, color='orange')
plt.xlabel('Instruction Types')
plt.ylabel('Frequency')
plt.title('Distribution of Instruction Types')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# Data Stalls (from the log file)
# Plotting data stalls
plt.figure(figsize=(8, 5))
plt.plot(data_stalls, label='Data Stalls', color='red')
plt.xlabel('Clock Cycle')
plt.ylabel('Number of Data Stalls')
plt.legend()
plt.show()
