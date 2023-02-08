from time import *
from crc import CrcCalculator, Configuration

def xorCipher(msgBytes):
    with open("./RadsatGsToolkit/RGSProtocol/xor_key","rb") as fk:
        key = fk.read()
    msgEncoded = []

    for i in msgBytes:
        msgEncoded.append(i^key[0])

    return bytes(msgEncoded)

def addHeader(msg, manualTime = 0):
    preamble = int(0x2018).to_bytes(2,byteorder="little")

    length = len(msg).to_bytes(1,byteorder="little")

    if manualTime == 0:
        unixTime = int(time()).to_bytes(4,byteorder="little")
    else:
        unixTime = manualTime.to_bytes(4,byteorder="little")

    header = length + unixTime + msg

    configuration = Configuration(16, 0x8005, 0x0000, 0x0000, True, True)
    crc_calculator = CrcCalculator(configuration, True)
    checksum = int(crc_calculator.calculate_checksum(header)).to_bytes(2,byteorder="little")
    
    return(bytes(preamble + checksum + header))

def stripHeader(msg):
    return(msg[9:])

if __name__ == "__main__":
    xorCipher(bytes([0,1,0,1,0,1,0,1]))
