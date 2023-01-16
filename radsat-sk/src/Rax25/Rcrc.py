import crc

def crcAugCcitt():
    width = 16
    poly=0x1021
    init_value=0xFFFF
    final_xor_value=0xFFFF
    reverse_input=True
    reverse_output=True
    configuration = crc.Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
    return crc.CrcCalculator(configuration, True)
