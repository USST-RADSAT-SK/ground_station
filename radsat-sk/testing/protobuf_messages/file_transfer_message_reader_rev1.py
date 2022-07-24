from time import *
from numpy import *
import RFileTransfer_pb2 as fileTransfer
import RTelecommands_pb2 as telecommands  
from crc import CrcCalculator, Configuration

########################## Read / Write Message Functions ##########################

def writeToFile(protoMessage, fileName = "serializedFile"):
    fw = open("./output/" + fileName,"wb")
    fw.write(protoMessage.SerializeToString())  
    fw.close()

def readMessage(msgClass, fileName = "serializedFile", withHeader = False):
    # Read data from file
    if withHeader:
        fileName += "_header"
        fb = open("./output/" + fileName,"rb")
        removedHeader = fb.read()[9:]
        output = msgClass
        output.ParseFromString(removedHeader)
        fb.close()
        print("Data from file :\n#########################\n")

    elif not withHeader:
        fb = open("./output/" + fileName,"rb")
        output = msgClass
        output.ParseFromString(fb.read())
        fb.close()
        print("Data into file :\n#########################\n")

    print(output)
    print("#########################\n")

def addHeader(fileName = "serializedFile", checkHeader=False):
    fb = open("./output/" + fileName,"rb")
    messageData = fb.read()
    
    preamble = int(0x2018).to_bytes(2,byteorder="big")

    length = len(messageData).to_bytes(1,byteorder="big")

    unixTime = int(time()).to_bytes(4,byteorder="big")

    header = length + unixTime + messageData
    

    width = 16
    poly=0x8005
    init_value=0x0000
    final_xor_value=0x0000
    reverse_input=True
    reverse_output=True
    configuration = Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
    crc_calculator = CrcCalculator(configuration, True)
    checksum = int(crc_calculator.calculate_checksum(header)).to_bytes(2,byteorder="big")
    
    if checkHeader:
        print("Header data : ", "".join(f"0x{i:02x} " for i in header))
        print("Checksum : 0x" + str(checksum.hex()).upper())

    fullMessage = preamble + checksum + header

    fh = open("./output/" + fileName + "_header","wb")
    fh.write(bytearray(fullMessage))
    fh.close()

def xorCipher(inString):
    xorKey = 'P'
    length = len(inString)

    for i in range(length):
        inString = (inString[:i] + chr(ord(inString[i]) ^ ord(xorKey)) + inString[i + 1:])
        print(inString[i], end = "")
     
    return inString

############################ Populate Message Functions ############################

def makeFileTransferMessage():
    
    message = fileTransfer.file_transfer_message()

    messageType = input("Select message type:\n(1) OBC Telemetry\n(2) Tranceiver Telemetry\n\
(3) Camera Telemetry\n(4) EPS Telemetry\n(5) Battery Telemetry\n(6) Antenna Telemetry\n\
(7) Dosimeter Data\n(8) Image Packet\n(9) Module Error Report\n(10) Component Error Report\n\
(11) Error Report Summary\n")
    
    if messageType == "1":
        message.ObcTelemetry.mode = 1
        message.ObcTelemetry.uptime = 12
        message.ObcTelemetry.rtcTime = 23423
        message.ObcTelemetry.rtcTemperature = 32
        msgType = "ObcTelemetry"
    
    elif messageType == "2":
        message.TransceiverTelemetry.receiver.rxDoppler = 1.02
        message.TransceiverTelemetry.receiver.rxRssi = 34.56
        message.TransceiverTelemetry.receiver.busVoltage = 5.9
        message.TransceiverTelemetry.receiver.totalCurrent = 2.50
        message.TransceiverTelemetry.receiver.txCurrent = 1.98
        message.TransceiverTelemetry.receiver.rxCurrent = 2.01
        message.TransceiverTelemetry.receiver.powerAmplifierCurrent = 28.4
        message.TransceiverTelemetry.receiver.powerAmplifierTemperature = 29.8
        message.TransceiverTelemetry.receiver.boardTemperature = 30.2
        message.TransceiverTelemetry.receiver.uptime = 1092
        message.TransceiverTelemetry.receiver.frames = 234

        message.TransceiverTelemetry.transmitter.reflectedPower = 1.23
        message.TransceiverTelemetry.transmitter.forwardPower = 26.98
        message.TransceiverTelemetry.transmitter.busVoltage = 4.5
        message.TransceiverTelemetry.transmitter.totalCurrent = 3.1
        message.TransceiverTelemetry.transmitter.txCurrent = 2.21
        message.TransceiverTelemetry.transmitter.rxCurrent = 2.23
        message.TransceiverTelemetry.transmitter.powerAmplifierCurrent = 5.9
        message.TransceiverTelemetry.transmitter.powerAmplifierTemperature = 6.11
        message.TransceiverTelemetry.transmitter.boardTemperature = 28.6
        message.TransceiverTelemetry.transmitter.uptime = 1191
        msgType = "TransceiverTelemetry"

    elif messageType == "3":
        message.CameraTelemetry.uptime = 5744
        msgType = "CameraTelemetry"

    elif messageType == "4":
        message.EpsTelemetry.uptime = 2344
        msgType = "EpsTelemetry"

    elif messageType == "5":
        message.BatteryTelemetry.uptime = 3423
        msgType = "BatteryTelemetry"

    elif messageType == "6":
        message.AntennaTelemetry.uptime = 9368
        msgType = "AntennaTelemetry"

    elif messageType == "7":
        message.DosimeterData.boardOne.channelZero = 1
        message.DosimeterData.boardOne.channelOne = 1
        message.DosimeterData.boardOne.channelTwo = 1
        message.DosimeterData.boardOne.channelThree = 1  
        message.DosimeterData.boardOne.channelFour = 1
        message.DosimeterData.boardOne.channelFive = 1
        message.DosimeterData.boardOne.channelSix = 1
        message.DosimeterData.boardOne.channelSeven = 1

        message.DosimeterData.boardTwo.channelZero = 2
        message.DosimeterData.boardTwo.channelOne = 2
        message.DosimeterData.boardTwo.channelTwo = 2
        message.DosimeterData.boardTwo.channelThree = 2  
        message.DosimeterData.boardTwo.channelFour = 2
        message.DosimeterData.boardTwo.channelFive = 2
        message.DosimeterData.boardTwo.channelSix = 2
        message.DosimeterData.boardTwo.channelSeven = 2  
        msgType = "DosimeterData"

    elif messageType == "8":
        message.ImagePacket.id = 124122
        message.ImagePacket.type = 1
        message.ImagePacket.data = b'0x01'
        msgType = "ImagePacket"

    elif messageType == "9":
        message.ModuleErrorReport.module = 1231
        message.ModuleErrorReport.error = 1231
        msgType = "ModuleErrorReport"

    elif messageType == "10": 
        message.ComponentErrorReport.component = 5231
        message.ComponentErrorReport.error = 2231
        msgType = "ComponentErrorReport"

    elif messageType == "11":
        message.ErrorReportSummary.moduleErrorCount.extend([1,2])
        message.ErrorReportSummary.componentErrorCount.extend([3,4,5,6])
        msgType = "ErrorReportSummary"

    fileName = "fileTransferMessage" + msgType
    writeToFile(message, fileName)

    return message,fileName

def makeTelecommandMessage():

    message = telecommands.telecommand_message()

    messageType = input("Select message type:\n(1) Begin Pass\n(2) Begin File Transfer\n\
(3) Cease Transmission\n(4) Resume Transmission\n(5) Update Time\n(6) Reset\n")

    if messageType == "1":
        message.BeginPass.passLength = 10
        msgType = "BeginPass"
    
    elif messageType == "2":
        message.BeginFileTransfer.begin = True
        msgType = "BeginFileTransfer"

    elif messageType == "3":
        message.CeaseTransmission.duration = 1
        msgType = "CeaseTransmission"

    elif messageType == "4":
        message.ResumeTransmission.resume = True
        msgType = "ResumeTransmission"

    elif messageType == "5":
        message.UpdateTime.unixTime = 1123
        msgType = "UpdateTime"

    elif messageType == "6":
        message.Reset.device = "Obc"
        message.Reset.hard = 1
        msgType = "Reset"

    fileName = "telecommandMessage" + msgType
    writeToFile(message, fileName)

    return message,fileName

################################# Script Interface #################################

messageType = "2"#input("Select message type:\n(1) File Transfer\n(2) Telecommand\n")

if messageType == "1":
    message,fileName = makeFileTransferMessage()
    readMessage(fileTransfer.file_transfer_message(), fileName)
    addHeader(fileName)
    readMessage(fileTransfer.file_transfer_message(), fileName,withHeader=True)

elif messageType == "2":
    message,fileName = makeTelecommandMessage()
    readMessage(telecommands.telecommand_message(), fileName)
    addHeader(fileName)
    readMessage(telecommands.telecommand_message(), fileName,withHeader=True)