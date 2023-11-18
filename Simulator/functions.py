# class Functions:
#     def __init__(self, registers, memory, pc):
#         # RISC-V registers
#         registers = registers
#         # memory (an array)
#         memory = memory
#         # program counter
#         pc = pc
        
def lui(rd, imm, registers, memory, pc):
    """
    Description: simulate the LUI (Load Upper Immediate) instruction
    Logic: rd ← imm u, pc ← pc+4
    """
    # print("lui")
    registers[rd] = imm << 12
    # print("function: ",registers[rd])
    return registers, memory, pc

def auipc(rd, imm, registers, memory, pc):
    """
    Description: simulate the AUIPC (Add Upper Immediate to PC) instruction
    Logic: rd ← pc + imm u, pc ← pc+4
    """
    # print("auipc")
    registers[rd] = (imm << 12) + pc
    # print("function: ",registers[rd])
    return registers, memory, pc

def jal(rd, imm, registers, memory, pc):
    """
    Description: simulate the JAL (Jump and Link) instruction
    Logic: rd ← pc+4, pc ← pc+imm j
    """
    # print("jal")
    registers[rd] = pc + 4
    pc += imm
    # print("function: ",registers[rd])
    return registers, memory, pc

def jalr(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the JALR (Jump and Link Register) instruction
    Logic: rd ← pc+4, pc ← (rs1+imm i) & ∼1
    """
    # print("jalr")
    registers[rd] = pc + 4
    pc = (registers[rs1] + imm) & -2
    # print("function: ",registers[rd])
    return registers, memory, pc

def beq(rs1, rs2, imm, registers, memory, pc):
    """
    Description: simulate the BEQ (Branch Equal) instruction
    Logic: pc ← pc + ((rs1==rs2) ? imm b : 4)
    """
    # print("beq")
    if registers[rs1] == registers[rs2]:
        pc += (imm//4)
    else:
        pc += 1
    return registers, memory, pc

def bne(rs1, rs2, imm, registers, memory, pc):
    """
    Description: simulate the BNE (Branch Not Equal) instruction
    Logic: pc ← pc + ((rs1!=rs2) ? imm b : 4)
    """
    # print("bne")
    if registers[rs1] != registers[rs2]:
        pc += (imm//4)
    else:
        pc += 1
    return registers, memory, pc

def blt(rs1, rs2, imm, registers, memory, pc):
    """
    Description: simulate the BLT (Branch Less Than) instruction
    Logic: pc ← pc + ((rs1<rs2) ? imm b : 4)
    """
    # print("blt")
    if registers[rs1] < registers[rs2]:
        pc += (imm//4)
    else:
        pc += 1
    return registers, memory, pc

def bge(rs1, rs2, imm, registers, memory, pc):
    """
    Description: simulate the BGE (Branch Greater Than or Equal) instruction
    Logic: pc ← pc + ((rs1>=rs2) ? imm b : 4)
    """
    # print("bge")
    if registers[rs1] >= registers[rs2]:
        pc += (imm//4)
    else:
        pc += 1
    return registers, memory, pc

def bltu(rs1, rs2, imm, registers, memory, pc):
    """
    Description: simulate the BLTU (Branch Less Than Unsigned) instruction
    Logic: pc ← pc + ((rs1<rs2) ? imm b : 4)
    """
    # print("bltu")
    if registers[rs1] < registers[rs2]:
        pc += (imm//4)
    else:
        pc += 1
    return registers, memory, pc

def bgeu(rs1, rs2, imm, registers, memory, pc):
    """
    Description: simulate the BGEU (Branch Greater Than or Equal Unsigned) instruction
    Logic: pc ← pc + ((rs1>=rs2) ? imm b : 4)
    """
    # print("bgeu")
    if registers[rs1] >= registers[rs2]:
        pc += (imm//4)
    else:
        pc += 1
    return registers, memory, pc

def lb(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the LB (Load Byte) instruction
    Logic: rd ← sx(m8(rs1+imm i)), pc ← pc+4
    """
    # print("lb")
    address = registers[rs1] + imm
    registers[rd] = memory[address]
    # print("function: ",registers[rd])
    return registers, memory, pc

def lh(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the LH (Load Halfword) instruction
    Logic: rd ← sx(m16(rs1+imm i)), pc ← pc+4
    """
    # print("lh")
    address = registers[rs1] + imm
    registers[rd] = (memory[address] & 0xFF) | (memory[address + 1] << 8)
    # print("function: ",registers[rd])
    return registers, memory, pc

def lw(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the LW (Load Word) instruction
    Logic: rd ← sx(m32(rs1+imm i)), pc ← pc+4
    """
    # print("lw")
    print(registers[rs1])
    address = registers[rs1] + imm
    registers[rd] = (memory[address] & 0xFF) | ((memory[address + 1] & 0xFF) << 8) | ((memory[address + 2] & 0xFF) << 16) | (memory[address + 3] << 24)
    # print("function: ",registers[rd])
    return registers, memory, pc

def lbu(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the LBU (Load Byte Unsigned) instruction
    Logic: rd ← zx(m8(rs1+imm i)), pc ← pc+4
    """
    # print("lbu")
    address = registers[rs1] + imm
    registers[rd] = memory[address]
    # print("function: ",registers[rd])
    return registers, memory, pc

def lhu(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the LHU (Load Halfword Unsigned) instruction
    Logic: rd ← zx(m16(rs1+imm i)), pc ← pc+4
    """
    # print("lhu")
    address = registers[rs1] + imm
    registers[rd] = (memory[address] & 0xFF) | (memory[address + 1] << 8)
    # print("function: ",registers[rd])
    return registers, memory, pc

def sb(rs1, rs2, imm, registers, memory, pc):
    """
    Description: simulate the SB (Store Byte) instruction
    Logic: m8(rs1+imm s) ← rs2[7:0], pc ← pc+4
    """
    # print("sb")
    address = registers[rs1] + imm
    memory[address] = registers[rs2] & 0xFF
    # print(memory[address])
    return registers, memory, pc

def sh(rs1, rs2, imm, registers, memory, pc):
    """
    Description: simulate the SH (Store Halfword) instruction
    Logic: m16(rs1+imm s) ← rs2[15:0], pc ← pc+4
    """
    # print("sh")
    address = registers[rs1] + imm
    memory[address] = registers[rs2] & 0xFF
    memory[address + 1] = (registers[rs2] >> 8) & 0xFF
    # print(memory[address])
    return registers, memory, pc

def sw(rs1, rs2, imm, registers, memory, pc):
    """
    Description: simulate the SW (Store Word) instruction
    Logic: m32(rs1+imm s) ← rs2[31:0], pc ← pc+4
    """
    # print("sw")
    address = registers[rs1] + imm
    memory[address] = registers[rs2] & 0xFF
    # memory[address + 1] = (registers[rs2] >> 8) & 0xFF
    # memory[address + 2] = (registers[rs2] >> 16) & 0xFF
    # memory[address + 3] = (registers[rs2] >> 24)
    # print(memory[address])
    return registers, memory, pc

def addi(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the ADDI (Add Immediate) instruction
    Logic: rd ← rs1 + imm i, pc ← pc+4
    """
    # print("addi")
    registers[rd] = registers[rs1] + imm
    # print("function: ",registers[rd])
    return registers, memory, pc

def slti(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the SLTI (Set Less Than Immediate) instruction
    Logic: rd ← (rs1 < imm i) ? 1 : 0, pc ← pc+4
    """
    # print("slti")
    registers[rd] = 1 if registers[rs1] < imm else 0
    # print("function: ",registers[rd])
    return registers, memory, pc

def sltiu(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the SLTIU (Set Less Than Immediate Unsigned) instruction
    Logic: rd ← (rs1 < imm i) ? 1 : 0, pc ← pc+4
    """
    # print("sltiu")
    registers[rd] = 1 if (registers[rs1] & 0xFFFFFFFF) < (imm & 0xFFFFFFFF) else 0
    # print("function: ",registers[rd])
    return registers, memory, pc

def xori(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the XORI (XOR Immediate) instruction
    Logic: rd ← rs1 ⊕ imm i, pc ← pc+4
    """
    # print("xori")
    registers[rd] = registers[rs1] ^ imm
    # print("function: ",registers[rd])
    return registers, memory, pc

def ori(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the ORI (OR Immediate) instruction
    Logic: rd ← rs1 ∨ imm i, pc ← pc+4
    """
    # print("ori")
    registers[rd] = registers[rs1] | imm
    # print("function: ",registers[rd])
    return registers, memory, pc

def andi(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the ANDI (AND Immediate) instruction
    Logic: rd ← rs1 ∧ imm i, pc ← pc+4
    """
    # print("andi")
    registers[rd] = registers[rs1] & imm
    # print("function: ",registers[rd])
    return registers, memory, pc

def slli(rd, rs1, shamt, registers, memory, pc):
    """
    Description: simulate the SLLI (Shift Left Logical Immediate) instruction
    Logic: rd ← rs1 << shamt i, pc ← pc+4
    """
    registers[rd] = registers[rs1] << shamt
    # print("function: ",registers[rd])
    return registers, memory, pc

def srli(rd, rs1, shamt, registers, memory, pc):
    """
    Description: simulate the SRLI (Shift Right Logical Immediate) instruction
    Logic: rd ← rs1 >> shamt i, pc ← pc+4
    """
    # print("srli")
    registers[rd] = registers[rs1] >> shamt
    # print("function: ",registers[rd])
    return registers, memory, pc

def srai(rd, rs1, shamt, registers, memory, pc):
    """
    Description: simulate the SRAI (Shift Right Arithmetic Immediate) instruction
    Logic: rd ← rs1 >> shamt i, pc ← pc+4
    """
    # print("srai")
    registers[rd] = registers[rs1] >> shamt
    # print("function: ",registers[rd])
    return registers, memory, pc

def add(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the ADD (Add) instruction
    Logic: rd ← rs1 + rs2, pc ← pc+4
    """
    print("add")
    registers[rd] = registers[rs1] + registers[rs2]
    # print("function: ",registers[rd])
    return registers, memory, pc

def sub(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the SUB (Subtract) instruction
    Logic: rd ← rs1 - rs2, pc ← pc+4
    """
    # print("sub")
    registers[rd] = registers[rs1] - registers[rs2]
    # print("function: ",registers[rd])
    return registers, memory, pc

def sll(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the SLL (Shift Left Logical) instruction
    Logic: rd ← rs1 << (rs2%XLEN), pc ← pc+4
    """
    # print("sll")
    registers[rd] = registers[rs1] << (registers[rs2] & 0x1F)
    # print("function: ",registers[rd])
    return registers, memory, pc
    
def slt(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the SLT (Set Less Than) instruction
    Logic: rd ← (rs1 < rs2) ? 1 : 0, pc ← pc+4
    """
    # print("slt")
    registers[rd] = 1 if registers[rs1] < registers[rs2] else 0
    # print("function: ",registers[rd])
    return registers, memory, pc

def sltu(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the SLTU (Set Less Than Unsigned) instruction
    Logic: rd ← (rs1 < rs2) ? 1 : 0, pc ← pc+4
    """
    # print("sltu")
    registers[rd] = 1 if (registers[rs1] & 0xFFFFFFFF) < (registers[rs2] & 0xFFFFFFFF) else 0
    # print("function: ",registers[rd])
    return registers, memory, pc

def xor(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the XOR (XOR) instruction
    Logic: rd ← rs1 ⊕ rs2, pc ← pc+4
    """
    # print("xor")
    registers[rd] = registers[rs1] ^ registers[rs2]
    # print("function: ",registers[rd])
    return registers, memory, pc

def srl(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the SRL (Shift Right Logical) instruction
    Logic: rd ← rs1 >> (rs2%XLEN), pc ← pc+4
    """
    # print("srl")
    registers[rd] = registers[rs1] >> (registers[rs2] & 0x1F)
    # print("function: ",registers[rd])
    return registers, memory, pc

def sra(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the SRA (Shift Right Arithmetic) instruction
    Logic: rd ← rs1 >> (rs2%XLEN), pc ← pc+4
    """
    # print("sra")
    registers[rd] = (registers[rs1] >> (registers[rs2] & 0x1F)) | (registers[rs1] & 0x80000000)
    # print("function: ",registers[rd])
    return registers, memory, pc

def or_(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the OR (OR) instruction
    Logic: rd ← rs1 ∨ rs2, pc ← pc+4
    """
    # print("or")
    registers[rd] = registers[rs1] | registers[rs2]
    # print("function: ",registers[rd])
    return registers, memory, pc

def and_(rd, rs1, rs2, registers, memory, pc):
    """
    Description: simulate the AND (AND) instruction
    Logic: rd ← rs1 ∧ rs2, pc ← pc+4
    """
    # print("and")
    registers[rd] = registers[rs1] & registers[rs2]
    # print("function: ",registers[rd])
    return registers, memory, pc

def loadnoc(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the LOADNOC instruction
    Logic: Store the data in register rs2 to memory-mapped registers at address (rs1+imm)
    """
    # print("loadnoc")
    address = registers[rs1] + imm
    # Check if the address is within the range of memory-mapped registers
    if 0x4000 <= address <= 0x4013:
        memory[address] = registers[rd]
    else:
        print("Address out of range for memory-mapped registers")
    return registers, memory, pc

def sendnoc(registers, memory, pc):
    """
    Description: simulate the SENDNOC instruction
    Logic: Write the integer 1 to the Memory Mapped Register with address 0x4010
    """
    # print("sendnoc")
    # Hardcode the value 1 to MMR4 (address 0x4010)
    memory[1023] = 1
    return registers, memory, pc
