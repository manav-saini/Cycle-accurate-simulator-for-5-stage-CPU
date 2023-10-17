from functions import *
from cache_lru import *

def simulate():
    global registers, memory, pc
    clock_cycles = 0
    cache_hits = 0
    cache_misses = 0
    pipeline = [{"instruction": None, "stall": False} for _ in range(5)]
    simulation_log = []

    # Initialize cache and sets for LRU
    cache = {}
    sets = {
        "00": {"ru": None, "data": [None, None]},
        "01": {"ru": None, "data": [None, None]},
        "10": {"ru": None, "data": [None, None]},
        "11": {"ru": None, "data": [None, None]}
    }

    with open('simulation.log', 'w') as log_file:
        for i in range(0, len(instructions)):
            # Handle instruction forwarding and stall
            if i >= MEM:
                if pipeline[MEM]["instruction"] and pipeline[EX]["instruction"]:
                    if pipeline[EX]["instruction"][:7] == "0000011" and get_memory_address(pipeline[EX]["instruction"]) == get_memory_address(pipeline[MEM]["instruction"]):
                        # Data hazard detected, stall the pipeline
                        for i in range(WB, IF - 1, -1):
                            pipeline[i] = pipeline[i - 1]
                        pipeline[IF] = {"instruction": None, "stall": True}
            
            # Update the pipeline stages
            for i in range(WB, IF, -1):
                pipeline[i] = pipeline[i - 1]

            if pipeline[IF]["stall"]:
                pipeline[IF] = {"instruction": None, "stall": False}
            else:
                instruction = instructions[i]
                pipeline[IF] = {"instruction": instruction, "stall": False}

            # Log the current clock cycle's pipeline state
            clock_cycle_log = {"cycle": clock_cycles, "stages": pipeline.copy(), "registers": registers.copy()}
            simulation_log.append(clock_cycle_log)
            
            if pipeline[MEM]["instruction"]:
                # Execute instructions in MEM and WB stages
                execute_instruction(pipeline[MEM]["instruction"])

                # Update the cache and memory for memory operations
                memory_address = get_memory_address(pipeline[MEM]["instruction"])
                if memory_address is not None:
                    if pipeline[MEM]["instruction"].startswith("0000011"):
                        cache_hit = update_cache_LRU(cache, memory_address, sets)
                        if cache_hit:
                            cache_hits += 1
                        else:
                            cache_misses += 1
                    # Handle memory read/write here
                    if pipeline[MEM]["instruction"].startswith("0000011"):  # Memory read
                        read_data = memory[memory_address]
                        registers[registers_mapping[pipeline[MEM]["instruction"][20:25]]] = read_data
                    elif pipeline[MEM]["instruction"].startswith("0000010"):  # Memory write
                        write_data = registers[registers_mapping[pipeline[MEM]["instruction"][20:25]]]
                        memory[memory_address] = write_data

            # Increment clock cycles
            clock_cycles += 1

            # Write the log to the log file
            log_file.write(f"Clock Cycle {clock_cycle_log['cycle']}:\n")
            for i, stage in enumerate(clock_cycle_log["stages"]):
                if stage["instruction"]:
                    log_file.write(f"{pipeline_stages[i]} - {stage['instruction']}\n")
            log_file.write("Registers: " + str(clock_cycle_log["registers"]) + "\n")
            log_file.write("-" * 50 + "\n")

    # Print cache statistics
    print("Cache Hits:", cache_hits)
    print("Cache Misses:", cache_misses)


# Define the update_cache_LRU function
def update_cache_LRU(cache, memory_address, sets):
    set_bits = memory_address[-2:]
    if set_bits not in cache:
        cache[set_bits] = sets.copy()
    cache_set = cache[set_bits]
    update(memory_address, set_bits, cache_set)
    return any(addr == memory_address for data in cache_set.values() for addr in data["data"])

def execute_instruction(binary_instruction):
    global registers
    global memory
    global pc
    print("execute_instruction: ", binary_instruction)
    opcode = binary_instruction[25:32]
    funct3 = binary_instruction[17:20]
    funct7 = binary_instruction[0:7]
    
    # print("execute_instruction opcode: ", opcode)
    # print("execute_instruction funct3: ", funct3)

    if opcode in opcode_to_instruction:
        # print(opcode)
        operation = opcode_to_instruction[opcode]
        # print("operation: ", operation)
        
        if isinstance(operation, dict):
            if funct3 in operation:
                operation = operation[funct3]
            else:
                raise ValueError(f"Unsupported funct3 {funct3} for opcode {opcode}")

        if operation == 'LUI':
            imm = int(binary_instruction[0:20], 2)
            rd = registers_mapping.get(binary_instruction[20:25])
            print("LUI: ", imm, rd)
            print("[]: ",registers[rd])
            print("get: ",registers.get(rd))
            registers, memory, pc = lui(rd, imm, registers, memory, pc)
        elif operation == 'AUIPC':
            imm = int(binary_instruction[0:20], 2)
            rd = registers_mapping.get(binary_instruction[20:25])
            print("AUIPC: ", imm, rd)
            registers, memory, pc = auipc(rd, imm, registers, memory, pc)
        elif operation == 'JAL':
            imm = int(binary_instruction[0]) << 20 | int(binary_instruction[12:20], 2) << 12 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
            rd = registers_mapping.get(binary_instruction[20:25])
            print("JAL: ", imm, rd)
            registers, memory, pc = jal(rd, imm, registers, memory, pc)
        elif operation == 'JALR':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("JALR: ", imm, rs1, rd)
            registers, memory, pc = jalr(rd, rs1, imm, registers, memory, pc)
        elif operation == 'BEQ':
            imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            print("BEQ: ", imm, rs1, rs2)
            registers, memory, pc = beq(rs1, rs2, imm, registers, memory, pc)
        elif operation == 'BNE':
            imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            print("BNE: ", imm, rs1, rs2)
            registers, memory, pc = bne(rs1, rs2, imm, registers, memory, pc)
        elif operation == 'BLT':
            imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            print("BLT: ", imm, rs1, rs2)
            registers, memory, pc = blt(rs1, rs2, imm, registers, memory, pc)
        elif operation == 'BGE':
            imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            print("BGE: ", imm, rs1, rs2)
            registers, memory, pc = bge(rs1, rs2, imm, registers, memory, pc)
        elif operation == 'BLTU':
            imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            print("BLTU: ", imm, rs1, rs2)
            registers, memory, pc = bltu(rs1, rs2, imm, registers, memory, pc)
        elif operation == 'BGEU':
            imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            print("BGEU: ", imm, rs1, rs2)
            registers, memory, pc = bgeu(rs1, rs2, imm, registers, memory, pc)
        elif operation == 'LB':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("LB: ", imm, rs1, rd)
            registers, memory, pc = lb(rd, rs1, imm, registers, memory, pc)
        elif operation == 'LH':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("LH: ", imm, rs1, rd)
            registers, memory, pc = lh(rd, rs1, imm, registers, memory, pc)
        elif operation == 'LW':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("LW: ", imm, rs1, rd)
            registers, memory, pc = lw(rd, rs1, imm, registers, memory, pc)
        elif operation == 'LBU':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("LBU: ", imm, rs1, rd)
            registers, memory, pc = lbu(rd, rs1, imm, registers, memory, pc)
        elif operation == 'LHU':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("LHU: ", imm, rs1, rd)
            registers, memory, pc = lhu(rd, rs1, imm, registers, memory, pc)
        elif operation == 'SB':
            imm = int(binary_instruction[0:12], 2)
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            print("SB: ", imm, rs1, rs2)
            registers, memory, pc = sb(rs1, rs2, imm, registers, memory, pc)
        elif operation == 'SH':
            imm = int(binary_instruction[0:12], 2)
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            print("SH: ", imm, rs1, rs2)
            registers, memory, pc = sh(rs1, rs2, imm, registers, memory, pc)
        elif operation == 'SW':
            imm = int(binary_instruction[0:12], 2)
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            print("SW: ", imm, rs1, rs2)
            registers, memory, pc = sw(rs1, rs2, imm, registers, memory, pc)
        elif operation == 'ADDI':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("ADDI: ", imm, rs1, rd)
            registers, memory, pc = addi(rd, rs1, imm, registers, memory, pc)
        elif operation == 'SLTI':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SLTI: ", imm, rs1, rd)
            registers, memory, pc = slti(rd, rs1, imm, registers, memory, pc)
        elif operation == 'SLTIU':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SLTIU: ", imm, rs1, rd)
            registers, memory, pc = sltiu(rd, rs1, imm, registers, memory, pc)
        elif operation == 'XORI':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("XORI: ", imm, rs1, rd)
            registers, memory, pc = xori(rd, rs1, imm, registers, memory, pc)
        elif operation == 'ORI':
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("ORI: ", imm, rs1, rd)
            registers, memory, pc = ori(rd, rs1, imm, registers, memory, pc)
        elif operation == 'ANDI':
            imm = registers_mapping.get(binary_instruction[0:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("ANDI: ", imm, rs1, rd)
            registers, memory, pc = andi(rd, rs1, imm, registers, memory, pc)
        elif operation == 'SLLI':
            shamt = registers_mapping.get(binary_instruction[20:25])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SLLI: ", shamt, rs1, rd)
            registers, memory, pc = slli(rd, rs1, shamt, registers, memory, pc)
        elif operation == 'SRLI':
            shamt = registers_mapping.get(binary_instruction[20:25])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SRLI: ", shamt, rs1, rd)
            registers, memory, pc = srli(rd, rs1, shamt, registers, memory, pc)
        elif operation == 'SRAI':
            shamt = registers_mapping.get(binary_instruction[20:25])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SRAI: ", shamt, rs1, rd)
            registers, memory, pc = srai(rd, rs1, shamt, registers, memory, pc)
        elif operation == 'ADD':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("ADD: ", rs1, rs2, rd)
            registers, memory, pc = add(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'SUB':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SUB: ", rs1, rs2, rd)
            registers, memory, pc = sub(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'SLL':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SLL: ", rs1, rs2, rd)
            registers, memory, pc = sll(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'SLT':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SLT: ", rs1, rs2, rd)
            registers, memory, pc = slt(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'SLTU':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SLTU: ", rs1, rs2, rd)
            registers, memory, pc = sltu(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'XOR':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("XOR: ", rs1, rs2, rd)
            registers, memory, pc = xor(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'SRL':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SRL: ", rs1, rs2, rd)
            registers, memory, pc = srl(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'SRA':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("SRA: ", rs1, rs2, rd)
            registers, memory, pc = sra(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'OR':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("OR: ", rs1, rs2, rd)
            registers, memory, pc = or_(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'AND':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            rd = registers_mapping.get(binary_instruction[20:25])
            print("AND: ", rs1, rs2, rd)
            registers, memory, pc = and_(rd, rs1, rs2, registers, memory, pc)
        elif operation == 'LOADNOC':
            rd = registers_mapping.get(binary_instruction[20:25])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            imm = int(binary_instruction[0:12], 2)
            print("LOADNOC: ", rd, rs1, imm)
            registers, memory, pc = loadnoc(rd, rs1, imm, registers, memory, pc)
        elif operation == 'STORENOC':
            rs2 = registers_mapping.get(binary_instruction[7:12])
            rs1 = registers_mapping.get(binary_instruction[12:17])
            imm = int(binary_instruction[0:12], 2)
            print("STORENOC: ", rs1, rs2, imm)
            registers, memory, pc = sendnoc(rs1, rs2, imm, registers, memory, pc)
        else:
            raise ValueError(f"Unsupported operation {operation}")
    return registers, memory, pc

def get_memory_address(binary_instruction):
    opcode = binary_instruction[25:32]
    funct3 = binary_instruction[17:20]
    
    if opcode in opcode_to_instruction:
        operation = opcode_to_instruction[opcode]
        
        if operation in ["LW", "SW", "LH", "SH", "LB", "SB", "LBU", "LHU"]:
            # Extract the fields from the instruction
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))

            # Calculate the effective address
            effective_address = registers[rs1] + imm

            return effective_address
        elif operation == "LOADNOC":
            imm = int(binary_instruction[0:12], 2)
            rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))

            # Calculate the effective address for Memory Mapped Register
            effective_address = registers[rs1] + imm + 0x4000

            return effective_address
    return None  # Return None for instructions that don't access memory

def read_binary_file(file_path):
    with open(file_path, "rb") as binary_file:
        binary_data = binary_file.read()
        
        # Loop through the binary data, assuming each instruction is 4 bytes (32 bits)
        instruction_size = 4
        num_instructions = len(binary_data) // instruction_size
        
        instructions = []
        
        for i in range(num_instructions):
            # Extract 4 bytes (32 bits) for each instruction
            instruction_bytes = binary_data[i * instruction_size : (i + 1) * instruction_size]
            
            # Convert the bytes to an integer and then to a binary string
            instruction_int = int.from_bytes(instruction_bytes, byteorder='big')
            instruction_binary = format(instruction_int, '032b')
            
            # Output the binary instruction
            # print(f"Instruction {i + 1}: {instruction_binary}")
            
            instructions.append(instruction_binary)
    return instructions
            
# the opcode to instruction mapping
opcode_to_instruction = {
    "0110111": "LUI",
    "0010111": "AUIPC",
    "0010011": {
        "000": "ADDI",
        "001": "SLLI",
        "010": "SLTI",
        "011": "SLTIU",
        "100": "XORI",
        "101": {
            "0000000": "SRLI",
            "0100000": "SRAI"
        },
        "110": "ORI",
        "111": "ANDI"
    },
    "1100111": {
        "000": "JALR"
    },
    "1101111": "JAL",
    "1100011": {
        "000": "BEQ",
        "001": "BNE",
        "100": "BLT",
        "101": "BGE",
        "110": "BLTU",
        "111": "BGEU"
    },
    "0000011": {
        "000": "LB",
        "001": "LH",
        "010": "LW",
        "100": "LBU",
        "101": "LHU"
    },
    "0100011": {
        "000": "SB",
        "001": "SH",
        "010": "SW",
        "011": "LOADNOC"
    },
    "0011011": {
        "000": "ADD",
        "001": "SLL",
        "010": "SLT",
        "011": "SLTU",
        "100": "XOR",
        "101": {
            "0000000": "SRL",
            "0100000": "SRA"
        },
        "110": "OR",
        "111": "AND"
    },
    "1111111": "STORENOC",
}

registers_mapping = {
    "00000": "zero",
    "00001": "ra",
    "00010": "sp",
    "00011": "gp",
    "00100": "tp",
    "00101": "t0",
    "00110": "t1",
    "00111": "t2",
    "01000": "s0",
    "01001": "s1",
    "01010": "a0",
    "01011": "a1",
    "01100": "a2",
    "01101": "a3",
    "01110": "a4",
    "01111": "a5",
    "10000": "a6",
    "10001": "a7",
    "10010": "s2",
    "10011": "s3",
    "10100": "s4",
    "10101": "s5",
    "10110": "s6",
    "10111": "s7",
    "11000": "s8",
    "11001": "s9",
    "11010": "s10",
    "11011": "s11",
    "11100": "t3",
    "11101": "t4",
    "11110": "t5",
    "11111": "t6"
}

# Initializing registers with initial values
registers = {
    'zero': 0,  # Hard-wired zero
    'ra': 0,  # Return address
    'sp': 0,  # Stack pointer
    'gp': 0,  # Global pointer
    'tp': 0,  # Thread pointer
    't0': 0,
    't1': 0,
    't2': 0,
    't3': 0,
    't4': 0,
    't5': 0,
    't6': 0,
    's0': 0,  # Saved register
    's1': 0,
    's2': 0,
    's3': 0,
    's4': 0,
    's5': 0,
    's6': 0,
    's7': 0,
    's8': 0,
    's9': 0,
    's10': 0,
    's11': 0,
    'a0': 0,  # Function argument/return value
    'a1': 0,
    'a2': 0,
    'a3': 0,
    'a4': 0,
    'a5': 0,
    'a6': 0,
    'a7': 0
}

# Initializing memory with initial values
memory = [0] * 1024  # Initialize your memory with an appropriate size

# Initializing cache with initial values (if applicable)
cache = {}

# Load instructions into the memory
instructions = read_binary_file("./output.bin")

pc = 0  # Program counter

# Define constants for pipeline stages
IF, ID, EX, MEM, WB = range(5)
pipeline_stages = ["IF", "ID", "EX", "MEM", "WB"]

# Creating a simulator and running the simulation
simulate()