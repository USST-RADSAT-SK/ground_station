import os
from time import *
from datetime import date
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
    message = msg[9:]
    preamble = msg[0:2].hex()
    checkSum = msg[2:4].hex()
    length = int.from_bytes(msg[4:5],byteorder="little")
    timeStamp = int.from_bytes(msg[5:9],byteorder="little")
    return(message,preamble,checkSum,length,timeStamp)

def sendToFile(fileName,msg_header,msg_stripped,preamble,checkSum,length,timeStamp):
    msg_header = msg_header.hex()
    msg_stripped = msg_stripped.hex()
    
    if os.path.isfile(fileName) == False:
        with open(fileName,"w") as f:
            f.write("RADSAT-SK Data Log : " + getDateString() + "\nReceive Time,Preamble,Checksum,Length,Time Stamp, Message, Recv Data\n")
    
    with open(fileName,"a") as f:
        f.write('"' + str(int(time())) + '","' + str(preamble) + '","' + str(checkSum) + '","' + str(length) + '","' + str(timeStamp) + '","' + str(msg_stripped) + '","' + str(msg_header) + '",\n')

def getDateString():
    now = date.today().strftime("%Y_%m_%d")
    return(now)
