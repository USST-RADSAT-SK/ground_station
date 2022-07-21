from time import *
from crc import CrcCalculator, Configuration
from numpy import *
import RFileTransfer_pb2 as fileTransfer
import RTelecommands_pb2 as telecommands  

def writeToFile(protoMessage, fileName = "serializedFile"):
    fw = open("./output/" + fileName,"wb")
    fw.write(protoMessage.SerializeToString())  
    fw.close()

def readFileTransferMessage(fileName = "serializedFile"):
    # Read data from file
    fb = open("./output/" + fileName,"rb")
    output = fileTransfer.file_transfer_message()
    output.ParseFromString(fb.read())
    fb.close()

    fc = open("./output/" + fileName + "_out.txt","w")
    fc.write(str(output))
    print(output)

def readTelecommandMessage(fileName = "serializedFile"):
    # Read data from file
    fb = open("./output/" + fileName,"rb")
    output = telecommands.telecommand_message()
    output.ParseFromString(fb.read())
    fb.close()

    fc = open("./output/" + fileName + "_out.txt","w")
    fc.write(str(output))
    print(output)

def makeFileTransferMessage():
    
    message = fileTransfer.file_transfer_message()

    messageType = input("Select message type:\n(1) OBC Telemetry\n(2) Tranceiver Telemetry\n\
(3) Camera Telemetry\n(4) EPS Telemetry\n(5) Battery Telemetry\n(6) Antenna Telemetry\n\
(7) Dosimeter Data\n(8) Image Packet\n(9) Module Error Report\n(10) Component Error Report\n\
(11) Error Report Summary\n")
    
    if messageType == "1":
        message.ObcTelemetry.mode = 0
        message.ObcTelemetry.uptime = 0
        message.ObcTelemetry.rtcTime = 0
        message.ObcTelemetry.rtcTemperature = 0
    
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

    elif messageType == "3":
        message.CameraTelemetry.uptime = 0

    elif messageType == "4":
        message.EpsTelemetry = 0

    elif messageType == "5":
        message.BatteryTelemetry = -1

    elif messageType == "6":
        message.AntennaTelemetry = -1

    elif messageType == "7":
        message.DosimeterData.boardOne.channelZero = 0
        message.DosimeterData.boardOne.channelOne = 0
        message.DosimeterData.boardOne.channelTwo = 0
        message.DosimeterData.boardOne.channelThree = 0  
        message.DosimeterData.boardOne.channelFour = 0
        message.DosimeterData.boardOne.channelFive = 0
        message.DosimeterData.boardOne.channelSix = 0
        message.DosimeterData.boardOne.channelSeven = 0

        message.DosimeterData.boardTwo.channelZero = 0
        message.DosimeterData.boardTwo.channelOne = 0
        message.DosimeterData.boardTwo.channelTwo = 0
        message.DosimeterData.boardTwo.channelThree = 0  
        message.DosimeterData.boardTwo.channelFour = 0
        message.DosimeterData.boardTwo.channelFive = 0
        message.DosimeterData.boardTwo.channelSix = 0
        message.DosimeterData.boardTwo.channelSeven = 0  

    elif messageType == "8":
        message.ImagePacket.id = 0
        message.ImagePacket.type = "FullResolution"
        message.ImagePacket.data = 0

    elif messageType == "9":
        message.ModuleErrorReport.uptime = 0

    elif messageType == "10": 
        message.ComponentErrorReport.uptime = 0

    elif messageType == "11":
        message.ErrorReportSummary.uptime = 0

    writeToFile(message, "fileTransferMessage")

    return message

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
        message.Reset.Obc
        message.Reset.hard = 1
        msgType = "Reset"

    fileName = "telecommandMessage_" + msgType
    writeToFile(message, fileName)

    return message,fileName

def addHeader(fileName = "serializedFile"):
    fb = open("./output/" + fileName,"rb")
    messageData = fb.read()
    
    preamble = int(0x2018).to_bytes(2,byteorder="big")

    length = len(messageData).to_bytes(1,byteorder="big")

    unixTime = int(time()).to_bytes(4,byteorder="big")

    header1 = length + unixTime + messageData
    print("Header data : ", "".join(f"0x{i:02x} " for i in header1)) 

    width = 16
    poly=0x8005
    init_value=0x0000
    final_xor_value=0x0000
    reverse_input=True
    reverse_output=True
    configuration = Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
    crc_calculator = CrcCalculator(configuration, True)
    checksum = int(crc_calculator.calculate_checksum(header1)).to_bytes(2,byteorder="big")
    print("Checksum : 0x" + str(checksum.hex()))

    header = preamble + checksum + header1
    fullMessage = header + messageData

    fh = open("./output/" + fileName + "_header","wb")
    fh.write(bytearray(fullMessage))
    fh.close()

def readBinFile(file):
    with open(file,"rb") as f:
        byte = f.read(1)
        while byte:
            # Do stuff with byte.
            byte = f.read(1)
            print(byte)

messageType = "3" #input("Select message type:\n(1) File Transfer\n(2) Telecommand\n")

if messageType == "1":
    message = makeFileTransferMessage()
    readFileTransferMessage("fileTransferMessage")

elif messageType == "2":
    message,fileName = makeTelecommandMessage()
    readTelecommandMessage(fileName)
    addHeader(fileName)

elif messageType == "3":
    readBinFile("./output/telecommandMessage_BeginFileTransfer_header2")