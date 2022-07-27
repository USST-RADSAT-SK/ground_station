from crc import CrcCalculator, Configuration

data = bytes([0x00,0x01,0x02,0x03,0x04,0x05])
width = 16
poly=0x8005
init_value=0x0000
final_xor_value=0x0000
reverse_input=True
reverse_output=True

configuration = Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
use_table = True

crc_calculator = CrcCalculator(configuration, use_table)

checksum = crc_calculator.calculate_checksum(data)
print(hex(checksum))