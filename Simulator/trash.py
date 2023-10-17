from functions import Functions

class Simulator(Functions):
    def __init__(self, registers, memory, pc, instructions, cache):
        super().__init__(registers, memory, pc)
        self.instructions = instructions
        self.cache = cache

    def disassemble(self, binary):
        opcode = binary[25:32]
        funct3 = binary[17:20]
        funct7 = binary[0:7]

        if opcode in opcode_to_instruction:
            operation = opcode_to_instruction[opcode]

            if isinstance(operation, dict):
                # Handle opcode variations
                if funct3 in operation:
                    operation = operation[funct3]
                else:
                    raise ValueError(f"Unsupported funct3 {funct3} for opcode {opcode}")

            if operation == 'LUI':
                imm = int(binary[0:20], 2)
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.lui(rd, imm)
            elif operation == 'AUIPC':
                imm = int(binary[0:20], 2)
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.auipc(rd, imm)
            elif operation == 'JAL':
                imm = int(binary[0]) << 20 | int(binary[12:20], 2) << 12 | int(binary[11]) << 11 | int(binary[1:11], 2) << 1
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.jal(rd, imm)
            elif operation == 'JALR':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.jalr(rd, rs1, imm)
            elif operation == 'BEQ':
                imm = int(binary[0]) << 12 | int(binary[12:20], 2) << 5 | int(binary[11]) << 11 | int(binary[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                self.beq(rs1, rs2, imm)
            elif operation == 'BNE':
                imm = int(binary[0]) << 12 | int(binary[12:20], 2) << 5 | int(binary[11]) << 11 | int(binary[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                self.bne(rs1, rs2, imm)
            elif operation == 'BLT':
                imm = int(binary[0]) << 12 | int(binary[12:20], 2) << 5 | int(binary[11]) << 11 | int(binary[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                self.blt(rs1, rs2, imm)
            elif operation == 'BGE':
                imm = int(binary[0]) << 12 | int(binary[12:20], 2) << 5 | int(binary[11]) << 11 | int(binary[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                self.bge(rs1, rs2, imm)
            elif operation == 'BLTU':
                imm = int(binary[0]) << 12 | int(binary[12:20], 2) << 5 | int(binary[11]) << 11 | int(binary[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                self.bltu(rs1, rs2, imm)
            elif operation == 'BGEU':
                imm = int(binary[0]) << 12 | int(binary[12:20], 2) << 5 | int(binary[11]) << 11 | int(binary[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                self.bgeu(rs1, rs2, imm)
            elif operation == 'LB':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.lb(rd, rs1, imm)
            elif operation == 'LH':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.lh(rd, rs1, imm)
            elif operation == 'LW':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.lw(rd, rs1, imm)
            elif operation == 'LBU':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.lbu(rd, rs1, imm)
            elif operation == 'LHU':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.lhu(rd, rs1, imm)
            elif operation == 'SB':
                imm = int(binary[0:12], 2)
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                self.sb(rs1, rs2, imm)
            elif operation == 'SH':
                imm = int(binary[0:12], 2)
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                self.sh(rs1, rs2, imm)
            elif operation == 'SW':
                imm = int(binary[0:12], 2)
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                self.sw(rs1, rs2, imm)
            elif operation == 'ADDI':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.addi(rd, rs1, imm)
            elif operation == 'SLTI':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.slti(rd, rs1, imm)
            elif operation == 'SLTIU':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.sltiu(rd, rs1, imm)
            elif operation == 'XORI':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.xori(rd, rs1, imm)
            elif operation == 'ORI':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.ori(rd, rs1, imm)
            elif operation == 'ANDI':
                imm = int(binary[0:12], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.andi(rd, rs1, imm)
            elif operation == 'SLLI':
                shamt = int(binary[20:25], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.slli(rd, rs1, shamt)
            elif operation == 'SRLI':
                shamt = int(binary[20:25], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.srli(rd, rs1, shamt)
            elif operation == 'SRAI':
                shamt = int(binary[20:25], 2)
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.srai(rd, rs1, shamt)
            elif operation == 'ADD':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.add(rd, rs1, rs2)
            elif operation == 'SUB':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.sub(rd, rs1, rs2)
            elif operation == 'SLL':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.sll(rd, rs1, rs2)
            elif operation == 'SLT':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.slt(rd, rs1, rs2)
            elif operation == 'SLTU':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.sltu(rd, rs1, rs2)
            elif operation == 'XOR':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.xor(rd, rs1, rs2)
            elif operation == 'SRL':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.srl(rd, rs1, rs2)
            elif operation == 'SRA':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.sra(rd, rs1, rs2)
            elif operation == 'OR':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.or_(rd, rs1, rs2)
            elif operation == 'AND':
                rs2 = registers_mapping.get(int(binary[7:12], 2))
                rs1 = registers_mapping.get(int(binary[12:17], 2))
                rd = registers_mapping.get(int(binary[20:25], 2))
                self.and_(rd, rs1, rs2)

    def simulate(self):
        clock_cycles = 0
        pipeline = [{"instruction": None, "stall": False} for _ in range(5)]
        cache_hits = 0
        cache_misses = 0

        while True:
            if pipeline[4]["instruction"] is not None:
                break  # The last instruction has completed

            clock_cycles += 1

            # Move instructions through the pipeline (from stage 4 to 0)
            for i in range(4, -1, -1):
                if pipeline[i]["instruction"] is not None:
                    if i == 4:
                        continue  # The last stage is already completed

                    if i == 0:
                        # Execute the instruction in stage 0
                        self.execute_instruction(pipeline[i]["instruction"])
                        pipeline[i + 1] = {"instruction": pipeline[i]["instruction"], "stall": False}
                        pipeline[i] = {"instruction": None, "stall": False}
                        print(self.registers)
                    else:
                        # Move the instruction to the next stage
                        pipeline[i + 1] = {"instruction": pipeline[i]["instruction"], "stall": pipeline[i]["stall"]}
                        pipeline[i] = {"instruction": None, "stall": False}
                        print(self.registers)

            # Fetch the next instruction if the first stage is empty and not stalled
            if pipeline[0]["instruction"] is None and not pipeline[0]["stall"]:
                if self.pc < len(self.instructions):
                    # Load the binary instruction from memory
                    binary_instruction = format(self.memory[self.pc], '032b')
                    # Disassemble the binary instruction and pass it to execute_instruction
                    self.disassemble(binary_instruction)
                    pipeline[0]["instruction"] = binary_instruction
                    self.pc += 1
                    print(self.registers)
                else:
                    pipeline[0]["instruction"] = None
                    print(self.registers)

            # Check cache hits and misses
            if pipeline[0]["instruction"] is not None:
                addr = self.get_memory_address(pipeline[0]["instruction"])
                if addr in self.cache:
                    cache_hits += 1
                else:
                    cache_misses += 1

        # Output simulation results
        with open("simulation.log", "w") as log_file:
            log_file.write(f"Clock Cycles: {clock_cycles}\n")
            log_file.write(f"Cache Hits: {cache_hits}\n")
            log_file.write(f"Cache Misses: {cache_misses}\n")
            log_file.write("Register Values:\n")
            for reg_name, reg_value in self.registers.items():
                log_file.write(f"{reg_name}: {reg_value}\n")

    def execute_instruction(self, binary_instruction):
        opcode = binary_instruction[25:32]
        funct3 = binary_instruction[17:20]
        funct7 = binary_instruction[0:7]

        if opcode in opcode_to_instruction:
            operation = opcode_to_instruction[opcode]

            if isinstance(operation, dict):
                if funct3 in operation:
                    operation = operation[funct3]
                else:
                    raise ValueError(f"Unsupported funct3 {funct3} for opcode {opcode}")

            if operation == 'LUI':
                imm = int(binary_instruction[0:20], 2)
                print(binary_instruction[20:25])
                rd = registers_mapping.get(binary_instruction[20:25])
                self.lui(rd, imm)
            elif operation == 'AUIPC':
                imm = int(binary_instruction[0:20], 2)
                rd = registers_mapping.get(binary_instruction[20:25])
                self.auipc(rd, imm)
            elif operation == 'JAL':
                imm = int(binary_instruction[0]) << 20 | int(binary_instruction[12:20], 2) << 12 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
                rd = registers_mapping.get(binary_instruction[20:25])
                self.jal(rd, imm)
            elif operation == 'JALR':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.jalr(rd, rs1, imm)
            elif operation == 'BEQ':
                imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                self.beq(rs1, rs2, imm)
            elif operation == 'BNE':
                imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                self.bne(rs1, rs2, imm)
            elif operation == 'BLT':
                imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                self.blt(rs1, rs2, imm)
            elif operation == 'BGE':
                imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                self.bge(rs1, rs2, imm)
            elif operation == 'BLTU':
                imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                self.bltu(rs1, rs2, imm)
            elif operation == 'BGEU':
                imm = int(binary_instruction[0]) << 12 | int(binary_instruction[12:20], 2) << 5 | int(binary_instruction[11]) << 11 | int(binary_instruction[1:11], 2) << 1
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                self.bgeu(rs1, rs2, imm)
            elif operation == 'LB':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.lb(rd, rs1, imm)
            elif operation == 'LH':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.lh(rd, rs1, imm)
            elif operation == 'LW':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.lw(rd, rs1, imm)
            elif operation == 'LBU':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.lbu(rd, rs1, imm)
            elif operation == 'LHU':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.lhu(rd, rs1, imm)
            elif operation == 'SB':
                imm = int(binary_instruction[0:12], 2)
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                self.sb(rs1, rs2, imm)
            elif operation == 'SH':
                imm = int(binary_instruction[0:12], 2)
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                self.sh(rs1, rs2, imm)
            elif operation == 'SW':
                imm = int(binary_instruction[0:12], 2)
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                self.sw(rs1, rs2, imm)
            elif operation == 'ADDI':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.addi(rd, rs1, imm)
            elif operation == 'SLTI':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.slti(rd, rs1, imm)
            elif operation == 'SLTIU':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.sltiu(rd, rs1, imm)
            elif operation == 'XORI':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.xori(rd, rs1, imm)
            elif operation == 'ORI':
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.ori(rd, rs1, imm)
            elif operation == 'ANDI':
                imm = registers_mapping.get(int(binary_instruction[0:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.andi(rd, rs1, imm)
            elif operation == 'SLLI':
                shamt = registers_mapping.get(int(binary_instruction[20:25], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.slli(rd, rs1, shamt)
            elif operation == 'SRLI':
                shamt = registers_mapping.get(int(binary_instruction[20:25], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.srli(rd, rs1, shamt)
            elif operation == 'SRAI':
                shamt = registers_mapping.get(int(binary_instruction[20:25], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.srai(rd, rs1, shamt)
            elif operation == 'ADD':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.add(rd, rs1, rs2)
            elif operation == 'SUB':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.sub(rd, rs1, rs2)
            elif operation == 'SLL':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.sll(rd, rs1, rs2)
            elif operation == 'SLT':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.slt(rd, rs1, rs2)
            elif operation == 'SLTU':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.sltu(rd, rs1, rs2)
            elif operation == 'XOR':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.xor(rd, rs1, rs2)
            elif operation == 'SRL':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.srl(rd, rs1, rs2)
            elif operation == 'SRA':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.sra(rd, rs1, rs2)
            elif operation == 'OR':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.or_(rd, rs1, rs2)
            elif operation == 'AND':
                rs2 = registers_mapping.get(int(binary_instruction[7:12], 2))
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))
                rd = registers_mapping.get(int(binary_instruction[20:25], 2))
                self.and_(rd, rs1, rs2)

    def get_memory_address(self, binary_instruction):
        opcode = binary_instruction[25:32]
        funct3 = binary_instruction[17:20]
        
        if opcode in opcode_to_instruction:
            operation = opcode_to_instruction[opcode]
            
            if operation in ["LW", "SW", "LH", "SH", "LB", "SB", "LBU", "LHU"]:
                # Extract the fields from the instruction
                imm = int(binary_instruction[0:12], 2)
                rs1 = registers_mapping.get(int(binary_instruction[12:17], 2))

                # Calculate the effective address
                effective_address = self.registers[rs1] + imm

                return effective_address

        return None  # Return None for instructions that don't access memory

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
        "010": "SW"
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
    }
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
instructions = [
    '00000000000000000000000010110111',
    '00000000000000000000000010010111',
    '00000000101000000000000011101111',
    # int('00000000101001011000000011100111', 2),
    # int('00000000110001011000101001100011', 2),
    # int('00000000110001011001101001100011', 2),
    # int('00000000110001011100101001100011', 2),
    # int('00000000110001011101101001100011', 2),
    # int('00000000110001011110101001100011', 2),
    # int('00000000110001011111101001100011', 2),
    # int('00000000101001011000000010000011', 2),
    # int('00000000101001011001000010000011', 2),
    # int('00000000101001011010000010000011', 2),
    # int('00000000101001011100000010000011', 2),
    # int('00000000101001011101000010000011', 2),
    # int('00000000110001011000010100100011', 2),
    # int('00000000110001011001010100100011', 2),
    # int('00000000110001011010010100100011', 2),
    # int('00000000101001011000000010010011', 2),
    # int('00000000101001011010000010010011', 2),
    # int('00000000101001011011000010010011', 2),
    # int('00000000101001011100000010010011', 2),
    # int('00000000101001011110000010010011', 2),
    # int('00000000101001011111000010010011', 2),
    # int('00000000110001011000000010110011', 2),
    # int('01000000110001011000000010110011', 2),
    # int('00000000110001011001000010110011', 2),
    # int('00000000110001011010000010110011', 2),
    # int('00000000110001011011000010110011', 2),
    # int('00000000110001011100000010110011', 2),
    # int('00000000110001011101000010110011', 2),
    # int('01000000110001011101000010110011', 2),
    # int('00000000110001011110000010110011', 2),
    # int('00000000110001011111000010110011', 2)
]

# Creating a simulator and running the simulation
simulator = Simulator(registers, memory, 0, instructions, cache)
simulator.simulate()