class Functions:
    def __init__(self, registers, memory, pc):
        # RISC-V registers
        self.registers = registers
        # memory (an array)
        self.memory = memory
        # program counter
        self.pc = pc
        
    def lui(self, rd, imm):
        """
        Description: simulate the LUI (Load Upper Immediate) instruction
        Logic: rd ← imm u, pc ← pc+4
        """
        self.registers[rd] = imm << 12

    def auipc(self, rd, imm):
        """
        Description: simulate the AUIPC (Add Upper Immediate to PC) instruction
        Logic: rd ← pc + imm u, pc ← pc+4
        """
        self.registers[rd] = (imm << 12) + self.pc

    def jal(self, rd, imm):
        """
        Description: simulate the JAL (Jump and Link) instruction
        Logic: rd ← pc+4, pc ← pc+imm j
        """
        self.registers[rd] = pc + 4
        pc += imm

    def jalr(self, rd, rs1, imm):
        """
        Description: simulate the JALR (Jump and Link Register) instruction
        Logic: rd ← pc+4, pc ← (rs1+imm i) & ∼1
        """
        self.registers[rd] = pc + 4
        pc = (self.registers[rs1] + imm) & -2

    def beq(self, rs1, rs2, imm):
        """
        Description: simulate the BEQ (Branch Equal) instruction
        Logic: pc ← pc + ((rs1==rs2) ? imm b : 4)
        """
        if self.registers[rs1] == self.registers[rs2]:
            pc += imm
        else:
            pc += 4

    def bne(self, rs1, rs2, imm):
        """
        Description: simulate the BNE (Branch Not Equal) instruction
        Logic: pc ← pc + ((rs1!=rs2) ? imm b : 4)
        """
        if self.registers[rs1] != self.registers[rs2]:
            pc += imm
        else:
            pc += 4

    def blt(self, rs1, rs2, imm):
        """
        Description: simulate the BLT (Branch Less Than) instruction
        Logic: pc ← pc + ((rs1<rs2) ? imm b : 4)
        """
        if self.registers[rs1] < self.registers[rs2]:
            pc += imm
        else:
            pc += 4

    def bge(self, rs1, rs2, imm):
        """
        Description: simulate the BGE (Branch Greater Than or Equal) instruction
        Logic: pc ← pc + ((rs1>=rs2) ? imm b : 4)
        """
        if self.registers[rs1] >= self.registers[rs2]:
            pc += imm
        else:
            pc += 4

    def bltu(self, rs1, rs2, imm):
        """
        Description: simulate the BLTU (Branch Less Than Unsigned) instruction
        Logic: pc ← pc + ((rs1<rs2) ? imm b : 4)
        """
        if self.registers[rs1] < self.registers[rs2]:
            pc += imm
        else:
            pc += 4

    def bgeu(self, rs1, rs2, imm):
        """
        Description: simulate the BGEU (Branch Greater Than or Equal Unsigned) instruction
        Logic: pc ← pc + ((rs1>=rs2) ? imm b : 4)
        """
        if self.registers[rs1] >= self.registers[rs2]:
            pc += imm
        else:
            pc += 4

    def lb(self, rd, rs1, imm):
        """
        Description: simulate the LB (Load Byte) instruction
        Logic: rd ← sx(m8(rs1+imm i)), pc ← pc+4
        """
        address = self.registers[rs1] + imm
        self.registers[rd] = self.memory[address]

    def lh(self, rd, rs1, imm):
        """
        Description: simulate the LH (Load Halfword) instruction
        Logic: rd ← sx(m16(rs1+imm i)), pc ← pc+4
        """
        address = self.registers[rs1] + imm
        self.registers[rd] = (self.memory[address] & 0xFF) | (self.memory[address + 1] << 8)

    def lw(self, rd, rs1, imm):
        """
        Description: simulate the LW (Load Word) instruction
        Logic: rd ← sx(m32(rs1+imm i)), pc ← pc+4
        """
        address = self.registers[rs1] + imm
        self.registers[rd] = (self.memory[address] & 0xFF) | ((self.memory[address + 1] & 0xFF) << 8) | ((self.memory[address + 2] & 0xFF) << 16) | (self.memory[address + 3] << 24)

    def lbu(self, rd, rs1, imm):
        """
        Description: simulate the LBU (Load Byte Unsigned) instruction
        Logic: rd ← zx(m8(rs1+imm i)), pc ← pc+4
        """
        address = self.registers[rs1] + imm
        self.registers[rd] = self.memory[address]

    def lhu(self, rd, rs1, imm):
        """
        Description: simulate the LHU (Load Halfword Unsigned) instruction
        Logic: rd ← zx(m16(rs1+imm i)), pc ← pc+4
        """
        address = self.registers[rs1] + imm
        self.registers[rd] = (self.memory[address] & 0xFF) | (self.memory[address + 1] << 8)

    def sb(self, rs1, rs2, imm):
        """
        Description: simulate the SB (Store Byte) instruction
        Logic: m8(rs1+imm s) ← rs2[7:0], pc ← pc+4
        """
        address = self.registers[rs1] + imm
        self.memory[address] = self.registers[rs2] & 0xFF

    def sh(self, rs1, rs2, imm):
        """
        Description: simulate the SH (Store Halfword) instruction
        Logic: m16(rs1+imm s) ← rs2[15:0], pc ← pc+4
        """
        address = self.registers[rs1] + imm
        self.memory[address] = self.registers[rs2] & 0xFF
        self.memory[address + 1] = (self.registers[rs2] >> 8) & 0xFF

    def sw(self, rs1, rs2, imm):
        """
        Description: simulate the SW (Store Word) instruction
        Logic: m32(rs1+imm s) ← rs2[31:0], pc ← pc+4
        """
        address = self.registers[rs1] + imm
        self.memory[address] = self.registers[rs2] & 0xFF
        self.memory[address + 1] = (self.registers[rs2] >> 8) & 0xFF
        self.memory[address + 2] = (self.registers[rs2] >> 16) & 0xFF
        self.memory[address + 3] = (self.registers[rs2] >> 24)

    def addi(self, rd, rs1, imm):
        """
        Description: simulate the ADDI (Add Immediate) instruction
        Logic: rd ← rs1 + imm i, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] + imm

    def slti(self, rd, rs1, imm):
        """
        Description: simulate the SLTI (Set Less Than Immediate) instruction
        Logic: rd ← (rs1 < imm i) ? 1 : 0, pc ← pc+4
        """
        self.registers[rd] = 1 if self.registers[rs1] < imm else 0

    def sltiu(self, rd, rs1, imm):
        """
        Description: simulate the SLTIU (Set Less Than Immediate Unsigned) instruction
        Logic: rd ← (rs1 < imm i) ? 1 : 0, pc ← pc+4
        """
        self.registers[rd] = 1 if self.registers[rs1] < imm else 0

    def xori(self, rd, rs1, imm):
        """
        Description: simulate the XORI (XOR Immediate) instruction
        Logic: rd ← rs1 ⊕ imm i, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] ^ imm

    def ori(self, rd, rs1, imm):
        """
        Description: simulate the ORI (OR Immediate) instruction
        Logic: rd ← rs1 ∨ imm i, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] | imm

    def andi(self, rd, rs1, imm):
        """
        Description: simulate the ANDI (AND Immediate) instruction
        Logic: rd ← rs1 ∧ imm i, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] & imm

    def slli(self, rd, rs1, shamt):
        """
        Description: simulate the SLLI (Shift Left Logical Immediate) instruction
        Logic: rd ← rs1 << shamt i, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] << shamt

    def srli(self, rd, rs1, shamt):
        """
        Description: simulate the SRLI (Shift Right Logical Immediate) instruction
        Logic: rd ← rs1 >> shamt i, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] >> shamt

    def srai(self, rd, rs1, shamt):
        """
        Description: simulate the SRAI (Shift Right Arithmetic Immediate) instruction
        Logic: rd ← rs1 >> shamt i, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] >> shamt

    def add(self, rd, rs1, rs2):
        """
        Description: simulate the ADD (Add) instruction
        Logic: rd ← rs1 + rs2, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] + self.registers[rs2]

    def sub(self, rd, rs1, rs2):
        """
        Description: simulate the SUB (Subtract) instruction
        Logic: rd ← rs1 - rs2, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] - self.registers[rs2]

    def sll(self, rd, rs1, rs2):
        """
        Description: simulate the SLL (Shift Left Logical) instruction
        Logic: rd ← rs1 << (rs2%XLEN), pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] << (self.registers[rs2] & 0x1F)
        
    def slt(self, rd, rs1, rs2):
        """
        Description: simulate the SLT (Set Less Than) instruction
        Logic: rd ← (rs1 < rs2) ? 1 : 0, pc ← pc+4
        """
        self.registers[rd] = 1 if self.registers[rs1] < self.registers[rs2] else 0

    def sltu(self, rd, rs1, rs2):
        """
        Description: simulate the SLTU (Set Less Than Unsigned) instruction
        Logic: rd ← (rs1 < rs2) ? 1 : 0, pc ← pc+4
        """
        self.registers[rd] = 1 if (self.registers[rs1] & 0xFFFFFFFF) < (self.registers[rs2] & 0xFFFFFFFF) else 0

    def xor(self, rd, rs1, rs2):
        """
        Description: simulate the XOR (XOR) instruction
        Logic: rd ← rs1 ⊕ rs2, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]

    def srl(self, rd, rs1, rs2):
        """
        Description: simulate the SRL (Shift Right Logical) instruction
        Logic: rd ← rs1 >> (rs2%XLEN), pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] >> (self.registers[rs2] & 0x1F)

    def sra(self, rd, rs1, rs2):
        """
        Description: simulate the SRA (Shift Right Arithmetic) instruction
        Logic: rd ← rs1 >> (rs2%XLEN), pc ← pc+4
        """
        self.registers[rd] = (self.registers[rs1] >> (self.registers[rs2] & 0x1F)) | (self.registers[rs1] & 0x80000000)

    def or_(self, rd, rs1, rs2):
        """
        Description: simulate the OR (OR) instruction
        Logic: rd ← rs1 ∨ rs2, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] | self.registers[rs2]

    def and_(self, rd, rs1, rs2):
        """
        Description: simulate the AND (AND) instruction
        Logic: rd ← rs1 ∧ rs2, pc ← pc+4
        """
        self.registers[rd] = self.registers[rs1] & self.registers[rs2]

if __name__ == "__main__":
    print("This is a module for RISC-V simulator.")
    print("It contains all logics for instructions to simulate them.")
    print("Please run 'python3 Simulator/main.py' to start the simulator.")