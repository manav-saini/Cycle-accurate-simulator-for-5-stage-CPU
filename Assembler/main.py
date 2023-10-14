import sys
from TABLES import opcode_table
from TABLES import type_table

# address: 0 based indexing, error generation: 1 based indexing

program = [] # input assembly program
bin_program = [] # output binary code
# address_table = {} # address of vars and labels. {name: (address, isVariable)}
registers = registers = {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
}


# location_counter = 0  reset in every pass
instruction_location = 0 # reset in every pass
last_valid_instruction_count = 0

# checks if immediate is a valid immediate
def validImmediate(immediate):
	if len(immediate) == 0:
		return False
	
	if not immediate[1:].isdecimal():
		return False
	
	return -2048 <= int(immediate) <= 2047


# checks if it is a valid register name and wheter it can be FLAGS
def validRegister(name):
	if name in registers:
		return True
	return False

def is_valid_shamt(shamt, max_shamt=31):
    """Check if shamt is a valid shifting amount for RV32I."""
    return 0 <= shamt <= max_shamt

def decimal_to_12bit_binary(imm):
    return format(imm if imm >= 0 else (1 << 12) + imm, '012b')

def s_type_to_binary(opcode, funct3, rs1, rs2, imm):
    if (
		imm < -2048 or imm > 2047
    ):
        raise ValueError("Input values are out of range for S-type instruction.")
    
    # Ensure imm is in the valid range and convert to 12-bit binary
    imm = imm & 0xFFF

    # Format each field and combine them into the final binary representation
    opcode_str = opcode
    funct3_str = funct3
    rs1_str = rs1
    rs2_str = rs2
    imm_high_str = format((imm >> 5) & 0x7F, '07b')
    imm_low_str = format(imm & 0x1F, '05b')
    
    binary = f"{imm_high_str}{rs2_str}{rs1_str}{funct3_str}{imm_low_str}{opcode_str}"
    
    return binary

def sb_type_to_binary(opcode, funct3, rs1, rs2, imm):
    if imm < -2048 or imm > 2047:
        raise ValueError("imm must be a 12-bit signed value (-2048 to 2047)")

    # Ensure that the immediate value is within a valid range for SB-type
    if imm % 2 != 0:
        raise ValueError("Immediate value must be even for SB-type instructions")

    # Create the binary representation
    imm_11 = (imm >> 11) & 1
    imm_4_1 = (imm >> 1) & 0b1111
    imm_10_5 = (imm >> 5) & 0b111111
    imm_12 = (imm >> 12) & 1
    opcode_bits = opcode
    funct3_bits = funct3
    rs1_bits = rs1
    rs2_bits = rs2
    # Concatenate all the binary fields
    binary = f"{imm_12}{imm_10_5}{rs2_bits}{rs1_bits}{funct3_bits}{imm_4_1}{imm_11}{opcode_bits}"
    return binary

def u_type_assembly_to_binary(imm, rd, opcode):
    if imm < 0 or imm > 1048575:  # Validate that imm is within the range 0 to 2^20-1
        raise ValueError("Immediate value must be in the range 0 to 1048575 for U-type instruction.")
    # Convert the values to binary strings
    imm_binary = format(imm, '020b')  # 20 bits for imm[31:12]
    rd_binary = rd   # 5 bits for rd
    opcode_binary = opcode  # 7 bits for opcode

    # Concatenate the binary strings to form the U-type instruction
    u_type_binary = imm_binary + rd_binary + opcode_binary

    return u_type_binary


def decimal_to_21bit_signed_binary(decimal):
    if decimal < -1048576 or decimal > 1048575:
        raise ValueError("Decimal value must be in the range -1048576 to 1048575 for 21-bit representation.")

    # Ensure that the immediate value is a multiple of 2 (bit 0 is always zero)
    if decimal % 2 != 0:
        raise ValueError("Decimal value must be a multiple of 2 (bit 0 must be zero) for 21-bit representation.")

    if decimal < 0:
        binary = bin((1 << 21) + decimal)[2:]  # Convert negative number to 21-bit two's complement
    else:
        binary = bin(decimal)[2:]  # Convert positive number to binary

    # Ensure the binary representation is exactly 21 bits long with leading zeros
    binary = binary.rjust(21, '0')

    return binary

def uj_type_assembly_to_binary(imm,rd,opcode):
	imm_bin = decimal_to_21bit_signed_binary(imm)
	return f"{imm_bin[20]}{imm_bin[10:1]}{imm_bin[11]}{imm_bin[19:12]}{rd}{opcode}"

def convert_binary():
	global program
	global opcode_table
	global type_table
	for line in program:
		line_tokens = line.split(" ")
		operation = line_tokens[0]
		if operation in opcode_table:
			values = opcode_table[operation]
			opcode = values[0]
			type = values[1]
			function_3_value = -1
			function_7_values = -1
			if len(values)==3:
				function_3_value = values[2]
			elif len(values)==4:
				function_7_values = values[3]
			if type in type_table:
				type_data = type_table[type]
				no_of_operands = type_data[0]
				if type == "R":
					sub_bin = ""
					sub_bin += function_7_values
					register_2 = line_tokens[no_of_operands]
					register_1 = line_tokens[no_of_operands-1]
					store_register = line_tokens[no_of_operands-2]
					if validRegister(register_2) and validRegister(register_1) and validRegister(store_register):
						sub_bin += f"{registers[register_2]}{registers[register_1]}{function_3_value}{registers[store_register]}{opcode}"
					else:
						try:
							if is_valid_shamt(int(register_2)):
								sub_bin += format(int(register_2), '05b')
								sub_bin += registers[register_1]
								sub_bin += function_3_value
								sub_bin += registers[store_register]
								sub_bin += opcode
						except:
							continue
					bin_program.append(sub_bin)
				elif type == "I":
					sub_bin = ""
					imm = line_tokens[no_of_operands]
					register_1 = line_tokens[no_of_operands-1]
					dest_register = line_tokens[no_of_operands-2]
					imm_bin = decimal_to_12bit_binary(int(imm))
					sub_bin = f"{imm_bin}{registers[register_1]}{function_3_value}{dest_register}{opcode}"
					bin_program.append(sub_bin)
				elif type == "S":
					sub_bin=""
					imm = line_tokens[no_of_operands]
					register_2 = line_tokens[no_of_operands-1]
					register_1 = line_tokens[no_of_operands-2]
					sub_bin = s_type_to_binary(opcode, function_3_value, registers[register_1], registers[register_2], int(imm))
					bin_program.append(sub_bin)
				elif type == "SB":
					sub_bin = ""
					imm = line_tokens[no_of_operands]
					register_2 = line_tokens[no_of_operands-1]
					register_1 = line_tokens[no_of_operands-2]
					sub_bin = sb_type_to_binary(opcode, function_3_value, registers[register_1], registers[register_2], int(imm))
					bin_program.append(sub_bin)
				elif type == "U":
					sub_bin=""
					imm = line_tokens[no_of_operands]
					dest_register = line_tokens[no_of_operands-1]
					sub_bin = u_type_assembly_to_binary(int(imm), registers[dest_register], opcode)
					bin_program.append(sub_bin)
				elif type == "UJ":
					sub_bin=""
					imm = line_tokens[no_of_operands]
					dest_register = line_tokens[no_of_operands-1]
					sub_bin = uj_type_assembly_to_binary(int(imm),registers[dest_register],opcode)
					bin_program.append(sub_bin)

def main():
	global program
	global bin_program
	file_path = input()
	with open(file_path, "r") as file:
		program = file.readlines()
	convert_binary()
	output_file_path = "output.bin"
	# Open the binary file for writing in binary mode
	print(bin_program)
	with open(output_file_path, "wb") as binary_file:
		for binary_str in bin_program:
			# Convert the binary string to bytes and write it to the binary file
			binary_data = int(binary_str, 2).to_bytes((len(binary_str) + 7) // 8, byteorder='big')
			binary_file.write(binary_data)
main()


					

				

