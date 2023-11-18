from registerfile import temp_registers
from memory import memory_dict

def lui(rd, imm):
    """
    Description: simulate the LUI (Load Upper Immediate) instruction
    Logic: rd ← imm u, pc ← pc+4
    """
    temp_registers[rd] = imm
    return [temp_registers[rd]]

def auipc(rd, imm, pc):
    """
    Description: simulate the AUIPC (Add Upper Immediate to PC) instruction
    Logic: rd ← pc + imm u, pc ← pc+4
    """
    temp_registers[rd] = imm + pc
    return [temp_registers[rd]]

def jalr(rd, rs1, imm, pc):
    """
    Description: simulate the JALR (Jump and Link Register) instruction
    """
    result = pc*4 + 4
    pc = ((temp_registers[rs1] + imm) & ~1)//4
    temp_registers[rd] = result
    return [result,pc]

def beq(rs1, rs2, imm, pc):
    """
    Description: simulate the BEQ (Branch Equal) instruction
    Logic: pc ← pc + ((rs1==rs2) ? imm b : 4)
    """
    branch_taken = False
    if temp_registers[rs1] ==temp_registers[rs2]:
        pc += (imm//4)
        branch_taken = True
    else:
        pc += 1
    return [pc,branch_taken]

def bne(rs1, rs2, imm, pc):
    """
    Description: simulate the BNE (Branch Not Equal) instruction
    Logic: pc ← pc + ((rs1!=rs2) ? imm b : 4)
    """
    branch_taken = False
    if temp_registers[rs1] != temp_registers[rs2]:
        pc += (imm//4)
        branch_taken = True
    else:
        pc += 1
    return [pc,branch_taken]

def blt(rs1, rs2, imm, pc):
    """
    Description: simulate the BLT (Branch Less Than) instruction
    Logic: pc ← pc + ((rs1<rs2) ? imm b : 4)
    """
    branch_taken = False
    if temp_registers[rs1] < temp_registers[rs2]:
        pc += (imm//4)
        branch_taken = True
    else:
        pc += 1
    return [pc,branch_taken]

def bge(rs1, rs2, imm, pc):
    """
    Description: simulate the BGE (Branch Greater Than or Equal) instruction
    Logic: pc ← pc + ((rs1>=rs2) ? imm b : 4)
    """
    branch_taken = False
    if temp_registers[rs1] >= temp_registers[rs2]:
        pc += (imm//4)
        branch_taken = True
    else:
        pc += 1
    return [pc,branch_taken]

def bltu(rs1, rs2, imm, pc):
    """
    Description: simulate the BLTU (Branch Less Than Unsigned) instruction
    Logic: pc ← pc + ((rs1<rs2) ? imm b : 4)
    """
    branch_taken = False
    if abs(temp_registers[rs1]) < abs(temp_registers[rs2]):
        pc += (imm//4)
        branch_taken = True
    else:
        pc += 1
    return [pc,branch_taken]

def bgeu(rs1, rs2, imm, pc):
    """
    Description: simulate the BGEU (Branch Greater Than or Equal Unsigned) instruction
    Logic: pc ← pc + ((rs1>=rs2) ? imm b : 4)
    """
    branch_taken = False
    if abs(temp_registers[rs1]) >= abs(temp_registers[rs2]):
        pc += (imm//4)
        branch_taken = True
    else:
        pc += 1
    return [pc,branch_taken]

def lb(rd, rs1, imm):
    """
    Description: simulate the LB (Load Byte) instruction
    """
    address = temp_registers[rs1] + imm
    # result = memory_dict[address]
    # temp_registers[rd] = result
    return [address]

def lh(rd, rs1, imm):
    """
    Description: simulate the LH (Load Halfword) instruction
    """
    address = temp_registers[rs1] + imm
    # result = memory_dict[address]
    # temp_registers[rd] = result
    return [address]

def lw(rd, rs1, imm):
    """
    Description: simulate the LW (Load Word) instruction
    Logic: rd ← sx(m32(rs1+imm i)), pc ← pc+4
    """
    address = temp_registers[rs1] + imm
    # result = memory_dict[address]
    # temp_registers[rd] = result
    return [address]

def lbu(rd, rs1, imm):
    """
    Description: simulate the LBU (Load Byte Unsigned) instruction
    Logic: rd ← zx(m8(rs1+imm i)), pc ← pc+4
    """
    address =temp_registers[rs1] + imm
    # result = memory_dict[address]
    # temp_registers[rd] = result
    return [address]

def lhu(rd, rs1, imm):
    """
    Description: simulate the LHU (Load Halfword Unsigned) instruction
    Logic: rd ← zx(m16(rs1+imm i)), pc ← pc+4
    """
    address =temp_registers[rs1] + imm
    # result = memory_dict[address]
    # temp_registers[rd] = result
    return [address]

def sb(rs1, rs2, imm):
    """
    Description: simulate the SB (Store Byte) instruction
    Logic: m8(rs1+imm s) ← rs2[7:0], pc ← pc+4
    """
    address =temp_registers[rs1] + imm
    result =temp_registers[rs2]
    return [result,address]

def sh(rs1, rs2, imm):
    """
    Description: simulate the SH (Store Halfword) instruction
    Logic: m16(rs1+imm s) ← rs2[15:0], pc ← pc+4
    """
    address =temp_registers[rs1] + imm
    result =temp_registers[rs2]
    return [result,address]

def sw(rs1, rs2, imm):
    """
    Description: simulate the SW (Store Word) instruction
    Logic: m32(rs1+imm s) ← rs2[31:0], pc ← pc+4
    """
    address =temp_registers[rs1] + imm
    result =temp_registers[rs2]
    return [result,address]

def addi(rd, rs1, imm):
    """
    Description: simulate the ADDI (Add Immediate) instruction
    """
    result =temp_registers[rs1] + imm
    temp_registers[rd] = result
    return [result]

def slti(rd, rs1, imm):
    """
    Description: simulate the SLTI (Set Less Than Immediate) instruction
    """
    result = 1 if temp_registers[rs1] < imm else 0
    temp_registers[rd] = result
    return [result]

def sltiu(rd, rs1, imm):
    """
    Description: simulate the SLTIU (Set Less Than Immediate Unsigned) instruction
    """
    result = 1 if abs(temp_registers[rs1]) < abs(imm) else 0
    temp_registers[rd] = result
    return [result]

def count(n) :
    c = 0
    while (n != 0) :
        c += 1
        n = n >> 1
    return c

def xori(rd, rs1, imm):
    """
    Description: simulate the XORI (XOR Immediate) instruction
    Logic: rd ← rs1 ⊕ imm i, pc ← pc+4
    """
    c = min(temp_registers[rs1], imm)
    d = max(temp_registers[rs1], imm)
    if (count(c) < count(d)) :
        c = c << ( count(d) - count(c) ) 
     
    result = c ^ d
    temp_registers[rd] = result
    return [result]

def ori(rd, rs1, imm):
    """
    Description: simulate the ORI (OR Immediate) instruction
    Logic: rd ← rs1 ∨ imm i, pc ← pc+4
    """
    result =temp_registers[rs1] | imm
    temp_registers[rd] = result
    return [result]

def andi(rd, rs1, imm):
    """
    Description: simulate the ANDI (AND Immediate) instruction
    Logic: rd ← rs1 ∧ imm i, pc ← pc+4
    """
    result =temp_registers[rs1] & imm
    temp_registers[rd] = result
    return [result]

def slli(rd, rs1, shamt):
    """
    Description: simulate the SLLI (Shift Left Logical Immediate) instruction
    Logic: rd ← rs1 << shamt i, pc ← pc+4
    """
    shift_amount =temp_registers[shamt] & 0b11111
    result =temp_registers[rs1] << shift_amount
    temp_registers[rd] = result
    return [result]

def srli(rd, rs1, shamt):
    """
    Description: simulate the SRLI (Shift Right Logical Immediate) instruction
    Logic: rd ← rs1 >> shamt i, pc ← pc+4
    """
    shift_amount =temp_registers[shamt] & 0b11111
    result =temp_registers[rs1] >> shift_amount
    temp_registers[rd] = result
    return [result]

def srai(rd, rs1, shamt):
    """
    Description: simulate the SRAI (Shift Right Arithmetic Immediate) instruction
    Logic: rd ← rs1 >> shamt i, pc ← pc+4
    """
    result =temp_registers[rs1] // (2**temp_registers[shamt])
    temp_registers[rd] = result
    return [result]

def add(rd, rs1, rs2):
    """
    Description: simulate the ADD (Add) instruction
    """
    result =temp_registers[rs1] +temp_registers[rs2]
    temp_registers[rd] = result
    return [result]

def sub(rd ,rs1, rs2):
    """
    Description: simulate the SUB (Subtract) instruction
    """
    result =temp_registers[rs1] -temp_registers[rs2]
    temp_registers[rd] = result
    return [result]

def sll(rd, rs1, rs2):
    """
    Description: simulate the SLL (Shift Left Logical) instruction
    """
    shift_amount =temp_registers[rs2] & 0b11111
    result =temp_registers[rs1] << shift_amount
    temp_registers[rd] = result
    return [result]
    
def slt(rd, rs1, rs2):
    """
    Description: simulate the SLT (Set Less Than) instruction
    """
    result = 1 if temp_registers[rs1] <temp_registers[rs2] else 0
    temp_registers[rd] = result
    return [result]

def sltu(rd, rs1, rs2):
    """
    Description: simulate the SLTU (Set Less Than Unsigned) instruction
    """
    result = 1 if abs(temp_registers[rs1]) < abs(temp_registers[rs2]) else 0
    temp_registers[rd] = result
    return [result]

def xor(rd, rs1, rs2):
    """
    Description: simulate the XOR (XOR) instruction
    """
    c = min(temp_registers[rs1],temp_registers[rs2])
    d = max(temp_registers[rs1],temp_registers[rs2])
    if (count(c) < count(d)) :
        c = c << ( count(d) - count(c) ) 
     
    result = c ^ d
    temp_registers[rd] = result
    return [result]

def srl(rd, rs1, rs2):
    """
    Description: simulate the SRL (Shift Right Logical) instruction
    """
    shift_amount =temp_registers[rs2] & 0b11111
    result =temp_registers[rs1] >> shift_amount
    temp_registers[rd] = result
    return [result]

def sra(rd, rs1, rs2):
    """
    Description: simulate the SRA (Shift Right Arithmetic) instruction
    """
    result =temp_registers[rs1] // (2**temp_registers[rs2])
    temp_registers[rd] = result
    return [result]

def or_(rd, rs1, rs2):
    """
    Description: simulate the OR (OR) instruction
    """
    result =temp_registers[rs1] |temp_registers[rs2]
    temp_registers[rd] = result
    return [result]

def and_(rd, rs1, rs2):
    """
    Description: simulate the AND (AND) instruction
    """
    result =temp_registers[rs1] &temp_registers[rs2]
    temp_registers[rd] = result
    return [result]

def loadnoc(rd, rs1, imm, registers, memory, pc):
    """
    Description: simulate the LOADNOC instruction
    Logic: Store the data in register rs2 to memory-mapped registers at address (rs1+imm)
    """
    # print("loadnoc")
    address =temp_registers[rs1] + imm
    # Check if the address is within the range of memory-mapped registers
    if 0x4000 <= address <= 0x4013:
        memory[address] =temp_registers[rd]
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
