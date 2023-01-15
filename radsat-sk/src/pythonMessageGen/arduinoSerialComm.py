import serial
import time
from numpy import *
import RRadsat_pb2 as radsat
import google.protobuf.message as pbError

pico = serial.Serial(port='COM9', baudrate=9600, timeout=1)

""" Get binary data from pre-made test files and write to pico """

def getBinFromFile(filename):   # TODO - Make more user friendly (GUI?)
    fb = open("./output/" + filename,"rb")
    encryptedMessage = fb.read()
    fb.close()
    return encryptedMessage
    
def write(message):
    time.sleep(0.05)
    pico.write(message)
    
""" Read response back from pico and decode/decrypt response (Ack?) """

def read():
    time.sleep(0.05)
    data = pico.readline()
    return data

def decodeMessage(encryptedMessage, msgClass = radsat.radsat_message()):
    decryptedMessage = []
    with open("./xorCipher/new_key","rb") as fk:
        key = fk.read()
    for i in encryptedMessage:
        decryptedMessage.append(i ^key[0])

    removedHeader = bytes(decryptedMessage[9:])
    output = msgClass
    output.ParseFromString(removedHeader)
    print(output)
    return output

def telecommandTest():
    """ Get test structs """

    ack = getBinFromFile("protocol_ack_header")
    nack = getBinFromFile("protocol_nack_header")

    beginFileTransfer = getBinFromFile("telecommandMessage_BeginFileTransfer_header")
    beginPass = getBinFromFile("telecommandMessage_BeginPass_header")
    ceaseTransmission = getBinFromFile("telecommandMessage_CeaseTransmission_header")
    reset = getBinFromFile("telecommandMessage_Reset_header")
    resumeTransmission = getBinFromFile("telecommandMessage_ResumeTransmission_header")
    updateTime = getBinFromFile("telecommandMessage_UpdateTime_header")

    while True:
        testCase = input("Select test Case:\n1. BeginPass\n2. BeginPass, FileTransfer, Ack\n\
3. BeginPass, CeaseTransmission\n")
        if testCase == "1":
            print("Running test case 1")
            commands = [beginPass]
            break
        elif testCase == "2":
            print("Running test case 2")
            commands = [beginPass,beginFileTransfer,ack]
            break
        elif testCase == "3":
            print("Running test case 3")
            commands = [beginPass,ceaseTransmission]
            break
        elif testCase == "4":
            print("Running test case 4")
            commands = [beginPass,beginFileTransfer,ack]
            break
        else:
            print("Invalid Entry\n")


    for i in range(0,1):
        input
        for command in commands:
            input("Send?")
            print("Sent:", command)
            write(command)

            #RxMessage = read()
            #try:
            #    decoded = decodeMessage(RxMessage)
            #except pbError.DecodeError:
            #    decoded = "!!Error decoding!!"
            
            #if RxMessage != ack:
            #    print("Ack not received")
            #    print("Received :",RxMessage)
            #    print("Decoded :",decoded)
                

telecommandTest()

"""
fileName = "./output/telecommandMessage_BeginPass_header"

TxMessage = getBinFromFile(fileName)
print(TxMessage)
write(TxMessage)

RxMessage = read()
print(RxMessage)
outStruct = decodeMessage(RxMessage)        
"""

"""
Telecommand Tests:

Send "Begin Pass"
Recv "Ack"

loop:
    Send Telecommand
    Recv "Ack"

"""

"""
File Transfer Tests:

Send "Begin File Transfer"

loop:
    Recv "Transfer File"
    Send "Ack"
Recv "End Pass"
"""

"""
For loops, try:
    - Single message
    - Multiple messages
    - Bad message
    - No messages (Move directly from Telecommand to Transfer)

For file transfer, do the loopback from python through Pico to get a filetransfer message back.
Then if on decoding we get a type error for the proto decode, send "Nack". If we get a solid
response, send nack

error = False
try:
    RxMessage = read()
    outStruct = decodeMessage(RxMessage)

except <proto formatting error>
    error = True

if not error:
    write(Ack)

else:
    write(Nack)
"""
"""
Size Testing :

beginPass
beginFileTransfer
Ack


"""