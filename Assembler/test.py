imm = 21
imm_high_str = format((imm >> 5) & 0x7F, '07b')
imm_low_str = format(imm & 0x1F, '05b')
print(format(imm,"02b"))
print(imm_high_str)
print(imm_low_str)

def decimal_to_12bit_binary(imm):
    return format(imm if imm >= 0 else (1 << 12) + imm, '012b')

print(decimal_to_12bit_binary(imm))
print(decimal_to_12bit_binary(imm)[11:4:-1])


imm_11 = (imm >> 11) & 1
imm_1_to_4 = (imm >> 1) & 0b1111
imm_12 = (imm >> 12) & 1
imm_5_to_10 = (imm >> 5) & 0b111111


print(imm & 0xFFF << 12)
