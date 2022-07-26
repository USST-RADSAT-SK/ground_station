from time import *
from numpy import *
import RRadsat_pb2 as radsat
import RProtocol_pb2 as protocol
import RFileTransfer_pb2 as fileTransfer
import RTelecommands_pb2 as telecommands
from crc import CrcCalculator, Configuration

####################################### Read / Write Message Functions #######################################

def writeToFile(protoMessage, fileName = "serializedFile"):
    fw = open("./output/" + fileName,"wb")
    fw.write(protoMessage.SerializeToString())  
    fw.close()

def readMessage(msgClass, fileName = "serializedFile", withHeader = False):
    # Read data from file
    if withHeader:
        fileName += "_header"
        fb = open("./output/" + fileName,"rb")

        encryptedMessage = list(fb.read())
        decryptedMessage = []

        with open("encryption_key","rb") as fk:
            key = fk.read()
        for i in encryptedMessage:
            decryptedMessage.append(i ^key[0])

        removedHeader = bytes(decryptedMessage[9:])
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
    
    # Make header
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

    headerMessage = list(preamble + checksum + header)
    
    # Encrypt message with header
    with open("encryption_key","rb") as fk:
        key = fk.read()

    fullMessage = []
    
    for i in headerMessage:
        fullMessage.append(i ^key[0])

    fh = open("./output/" + fileName + "_header","wb")
    fh.write(bytearray(fullMessage))
    fh.close()

def printDataAsHex(fileName, header = False):
    if header:
        fileName = fileName + "_header"
    with open('./output/' + fileName,'rb') as fr:
        out = bytearray(fr.read()).hex()
    return out

######################################### Populate Message Functions #########################################

def makeFileTransferMessage():
    
    message = radsat.radsat_message()

    while True:

        messageType = input("Select message type:\n(1) OBC Telemetry\n(2) Tranceiver Telemetry\n\
(3) Camera Telemetry\n(4) EPS Telemetry\n(5) Battery Telemetry\n(6) Antenna Telemetry\n\
(7) Dosimeter Data\n(8) Image Packet\n(9) Module Error Report\n(10) Component Error Report\n\
(11) Error Report Summary\n")
    
        if messageType == "1":
            message.FileTransferMessage.ObcTelemetry.mode = 1
            message.FileTransferMessage.ObcTelemetry.uptime = 12
            message.FileTransferMessage.ObcTelemetry.rtcTime = 23423
            message.FileTransferMessage.ObcTelemetry.rtcTemperature = 32
            msgType = "ObcTelemetry"
            break

        elif messageType == "2":
            message.FileTransferMessage.TransceiverTelemetry.receiver.rxDoppler = 1.02
            message.FileTransferMessage.TransceiverTelemetry.receiver.rxRssi = 34.56
            message.FileTransferMessage.TransceiverTelemetry.receiver.busVoltage = 5.9
            message.FileTransferMessage.TransceiverTelemetry.receiver.totalCurrent = 2.50
            message.FileTransferMessage.TransceiverTelemetry.receiver.txCurrent = 1.98
            message.FileTransferMessage.TransceiverTelemetry.receiver.rxCurrent = 2.01
            message.FileTransferMessage.TransceiverTelemetry.receiver.powerAmplifierCurrent = 28.4
            message.FileTransferMessage.TransceiverTelemetry.receiver.powerAmplifierTemperature = 29.8
            message.FileTransferMessage.TransceiverTelemetry.receiver.boardTemperature = 30.2
            message.FileTransferMessage.TransceiverTelemetry.receiver.uptime = 1092
            message.FileTransferMessage.TransceiverTelemetry.receiver.frames = 234

            message.FileTransferMessage.TransceiverTelemetry.transmitter.reflectedPower = 1.23
            message.FileTransferMessage.TransceiverTelemetry.transmitter.forwardPower = 26.98
            message.FileTransferMessage.TransceiverTelemetry.transmitter.busVoltage = 4.5
            message.FileTransferMessage.TransceiverTelemetry.transmitter.totalCurrent = 3.1
            message.FileTransferMessage.TransceiverTelemetry.transmitter.txCurrent = 2.21
            message.FileTransferMessage.TransceiverTelemetry.transmitter.rxCurrent = 2.23
            message.FileTransferMessage.TransceiverTelemetry.transmitter.powerAmplifierCurrent = 5.9
            message.FileTransferMessage.TransceiverTelemetry.transmitter.powerAmplifierTemperature = 6.11
            message.FileTransferMessage.TransceiverTelemetry.transmitter.boardTemperature = 28.6
            message.FileTransferMessage.TransceiverTelemetry.transmitter.uptime = 1191
            msgType = "TransceiverTelemetry"
            break

        elif messageType == "3":
            message.FileTransferMessage.CameraTelemetry.uptime = 5744
            msgType = "CameraTelemetry"
            break

        elif messageType == "4":
            message.FileTransferMessage.EpsTelemetry.uptime = 2344
            msgType = "EpsTelemetry"
            break

        elif messageType == "5":
            message.FileTransferMessage.BatteryTelemetry.uptime = 3423
            msgType = "BatteryTelemetry"
            break

        elif messageType == "6":
            message.FileTransferMessage.AntennaTelemetry.uptime = 9368
            msgType = "AntennaTelemetry"
            break

        elif messageType == "7":
            message.FileTransferMessage.DosimeterData.boardOne.channelZero = 1
            message.FileTransferMessage.DosimeterData.boardOne.channelOne = 1
            message.FileTransferMessage.DosimeterData.boardOne.channelTwo = 1
            message.FileTransferMessage.DosimeterData.boardOne.channelThree = 1  
            message.FileTransferMessage.DosimeterData.boardOne.channelFour = 1
            message.FileTransferMessage.DosimeterData.boardOne.channelFive = 1
            message.FileTransferMessage.DosimeterData.boardOne.channelSix = 1
            message.FileTransferMessage.DosimeterData.boardOne.channelSeven = 1

            message.FileTransferMessage.DosimeterData.boardTwo.channelZero = 2
            message.FileTransferMessage.DosimeterData.boardTwo.channelOne = 2
            message.FileTransferMessage.DosimeterData.boardTwo.channelTwo = 2
            message.FileTransferMessage.DosimeterData.boardTwo.channelThree = 2  
            message.FileTransferMessage.DosimeterData.boardTwo.channelFour = 2
            message.FileTransferMessage.DosimeterData.boardTwo.channelFive = 2
            message.FileTransferMessage.DosimeterData.boardTwo.channelSix = 2
            message.FileTransferMessage.DosimeterData.boardTwo.channelSeven = 2  
            msgType = "DosimeterData"
            break

        elif messageType == "8":
            message.FileTransferMessage.ImagePacket.id = 124122
            message.FileTransferMessage.ImagePacket.type = 1
            message.FileTransferMessage.ImagePacket.data = b'0x01'
            msgType = "ImagePacket"
            break

        elif messageType == "9":
            message.FileTransferMessage.ModuleErrorReport.module = 1231
            message.FileTransferMessage.ModuleErrorReport.error = 1231
            msgType = "ModuleErrorReport"
            break

        elif messageType == "10": 
            message.FileTransferMessage.ComponentErrorReport.component = 5231
            message.FileTransferMessage.ComponentErrorReport.error = 2231
            msgType = "ComponentErrorReport"
            break

        elif messageType == "11":
            message.FileTransferMessage.ErrorReportSummary.moduleErrorCount.extend([1,2])
            message.FileTransferMessage.ErrorReportSummary.componentErrorCount.extend([3,4,5,6])
            msgType = "ErrorReportSummary"
            break

        else:
            print("Invalid entry\n")

    fileName = "fileTransferMessage_" + msgType
    writeToFile(message, fileName)

    return message,fileName

def makeTelecommandMessage():

    message = radsat.radsat_message()
    while True:
        messageType = input("Select message type:\n(1) Begin Pass\n(2) Begin File Transfer\n\
(3) Cease Transmission\n(4) Resume Transmission\n(5) Update Time\n(6) Reset\n")

        if messageType == "1":
            message.TelecommandMessage.BeginPass.passLength = 10
            msgType = "BeginPass"
            print("MADE IT")
            break
    
        elif messageType == "2":
            message.TelecommandMessage.BeginFileTransfer.begin = True
            msgType = "BeginFileTransfer"
            break

        elif messageType == "3":
            message.TelecommandMessage.CeaseTransmission.duration = 1
            msgType = "CeaseTransmission"
            break

        elif messageType == "4":
            message.TelecommandMessage.ResumeTransmission.resume = True
            msgType = "ResumeTransmission"
            break

        elif messageType == "5":
            message.TelecommandMessage.UpdateTime.unixTime = 1123
            msgType = "UpdateTime"
            break

        elif messageType == "6":
            message.TelecommandMessage.Reset.device = "Obc"
            message.Reset.hard = 1
            msgType = "Reset"
            break

        else:
            print("Invalid entry\n")

    fileName = "telecommandMessage_" + msgType
    writeToFile(message, fileName)

    return message,fileName

def makeProtocolMessage():
    
    message = radsat.radsat_message()
    while True:
        messageType = input("Select message type:\n(1) ACK\n(2) NACK\n")

        if messageType == "1":
            message.ProtocolMessage.Ack.resp = 0
            msgType = "ack"
            break


        elif messageType == "2":
            message.ProtocolMessage.Nack.resp = 0
            msgType = "nack"
            break

        else:
            print("Invalid entry\n")

    fileName = "protocol_" + msgType
    writeToFile(message, fileName)

    return message,fileName

############################################## Script Interface ##############################################

while True:

    messageType = input("Select message type:\n(1) Protocol\n(2) File Transfer\n(3) Telecommand\n(Q) Quit\n")

    if messageType == "1":
        message,fileName = makeProtocolMessage()
        readMessage(radsat.radsat_message(), fileName)
        print("Pre-scramble data : " + printDataAsHex(fileName))
        addHeader(fileName)
        readMessage(radsat.radsat_message(), fileName,withHeader=True)
        print("Post-scramble data : " + printDataAsHex(fileName,header = True))

    elif messageType == "2":
        message,fileName = makeFileTransferMessage()
        readMessage(radsat.radsat_message(), fileName)
        print("Pre-scramble data : " + printDataAsHex(fileName))
        addHeader(fileName)
        readMessage(radsat.radsat_message(), fileName,withHeader=True)
        print("Post-scramble data : " + printDataAsHex(fileName,header = True))

    elif messageType == "3":
        message,fileName = makeTelecommandMessage()
        readMessage(radsat.radsat_message(), fileName)
        print("Pre-scramble data : " + printDataAsHex(fileName))
        addHeader(fileName)
        readMessage(radsat.radsat_message(), fileName,withHeader=True)
        print("Post-scramble data : " + printDataAsHex(fileName,header = True))
        print(type(printDataAsHex(fileName,header = True)))
        print(len(printDataAsHex(fileName,header = True)))



    elif messageType.upper() == "Q":
        print("Exiting ... ")
        break
    
    else:
        print("Invalid entry\n")