from time import *
from numpy import *
import RRadsat_pb2 as radsat
#import RProtocol_pb2 as protocol
#import RFileTransfer_pb2 as fileTransfer
#import RTelecommands_pb2 as telecommands
from crc import CrcCalculator, Configuration

####################################### Read / Write Message Functions #######################################

def writeToFile(protoMessage, fileName = "serializedFile"):
    fw = open("./output/" + fileName,"wb")
    fw.write(protoMessage.SerializeToString())  
    fw.close()

def readMessage(msgClass, fileName = "serializedFile", xorCipher = True, withHeader = False):
    # Read data from file
    if withHeader:
        fileName += "_header"
        fb = open("./output/" + fileName,"rb")

        encryptedMessage = list(fb.read())


        if xorCipher:
            decryptedMessage = []
            with open("./xorCipher/new_key","rb") as fk:
                key = fk.read()
            for i in encryptedMessage:
                decryptedMessage.append(i ^key[0])

        else: 
            decryptedMessage = encryptedMessage

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

def addHeader(fileName = "serializedFile", xorCipher = True, checkHeader=False):
    
    # Make header
    fb = open("./output/" + fileName,"rb")
    messageData = fb.read()
    
    preamble = int(0x2018).to_bytes(2,byteorder="little")

    length = len(messageData).to_bytes(1,byteorder="little")

    unixTime= int(time()).to_bytes(4,byteorder="little")

    header = length + unixTime + messageData

    width = 16
    poly=0x8005
    init_value=0x0000
    final_xor_value=0x0000
    reverse_input=True
    reverse_output=True
    configuration = Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
    crc_calculator = CrcCalculator(configuration, True)
    checksum = int(crc_calculator.calculate_checksum(header)).to_bytes(2,byteorder="little")
    checksum_reversed = bytes(reversed(checksum))
    
    if checkHeader:
        print("Header data : ", "".join(f"0x{i:02x} " for i in header))
        print("Checksum : 0x" + str(checksum_reversed.hex()).upper())

    headerMessage = list(preamble + checksum + header)
    
    if xorCipher:

        with open("./xorCipher/new_key","rb") as fk:
            key = fk.read()

        fullMessage = []
    
        for i in headerMessage:
            fullMessage.append(i ^key[0])

    else:
        fullMessage = headerMessage

    fh = open("./output/" + fileName + "_header","wb")
    fh.write(bytearray(fullMessage))
    print("Length = ",len(fullMessage))
    fh.close()

def printDataAsHex(fileName, header = False):
    if header:
        fileName = fileName + "_header"
    with open(fileName,'rb') as fr:
        out = bytearray(fr.read())
    hexData = ("".join(f"0x{i:02x}, " for i in out))
    return hexData

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
            message.FileTransferMessage.CameraTelemetry.uptime = 5

            message.FileTransferMessage.CameraTelemetry.powerTelemetry.current_3V3 = 5.3
            message.FileTransferMessage.CameraTelemetry.powerTelemetry.current_5V = 5.3
            message.FileTransferMessage.CameraTelemetry.powerTelemetry.current_SRAM_1 = 5.3
            message.FileTransferMessage.CameraTelemetry.powerTelemetry.current_SRAM_2 = 5.3
            message.FileTransferMessage.CameraTelemetry.powerTelemetry.overcurrent_SRAM_1 = 5
            message.FileTransferMessage.CameraTelemetry.powerTelemetry.overcurrent_SRAM_2 = 5
            
            message.FileTransferMessage.CameraTelemetry.cameraOneTelemetry.detectionThreshold = 5
            message.FileTransferMessage.CameraTelemetry.cameraOneTelemetry.autoAdjustMode = 5
            message.FileTransferMessage.CameraTelemetry.cameraOneTelemetry.exposure = 5
            message.FileTransferMessage.CameraTelemetry.cameraOneTelemetry.autoGainControl = 5
            message.FileTransferMessage.CameraTelemetry.cameraOneTelemetry.blueGain = 5
            message.FileTransferMessage.CameraTelemetry.cameraOneTelemetry.redGain = 5

            message.FileTransferMessage.CameraTelemetry.cameraTwoTelemetry.detectionThreshold = 5
            message.FileTransferMessage.CameraTelemetry.cameraTwoTelemetry.autoAdjustMode = 5
            message.FileTransferMessage.CameraTelemetry.cameraTwoTelemetry.exposure = 5
            message.FileTransferMessage.CameraTelemetry.cameraTwoTelemetry.autoGainControl = 5
            message.FileTransferMessage.CameraTelemetry.cameraTwoTelemetry.blueGain = 5
            message.FileTransferMessage.CameraTelemetry.cameraTwoTelemetry.redGain = 5
            
            msgType = "CameraTelemetry"
            break

        elif messageType == "4":
            message.FileTransferMessage.EpsTelemetry.sunSensorData.xPos = 2344
            message.FileTransferMessage.EpsTelemetry.sunSensorData.xNeg = 2344
            message.FileTransferMessage.EpsTelemetry.sunSensorData.yPos = 2344
            message.FileTransferMessage.EpsTelemetry.sunSensorData.yNeg = 2344
            message.FileTransferMessage.EpsTelemetry.sunSensorData.zPos = 2344
            message.FileTransferMessage.EpsTelemetry.sunSensorData.zNeg = 2344
            message.FileTransferMessage.EpsTelemetry.outputVoltageBCR = 2344
            message.FileTransferMessage.EpsTelemetry.outputVoltageBatteryBus = 2344
            message.FileTransferMessage.EpsTelemetry.outputVoltage5VBus = 2344
            message.FileTransferMessage.EpsTelemetry.outputVoltage3V3Bus = 2344
            message.FileTransferMessage.EpsTelemetry.outputCurrentBCR_mA = 2344
            message.FileTransferMessage.EpsTelemetry.outputCurrentBatteryBus = 2344
            message.FileTransferMessage.EpsTelemetry.outputCurrent5VBus = 2344
            message.FileTransferMessage.EpsTelemetry.outputCurrent3V3Bus = 2344
            message.FileTransferMessage.EpsTelemetry.PdbTemperature = 2344
            msgType = "EpsTelemetry"
            break

        elif messageType == "5":
            message.FileTransferMessage.BatteryTelemetry.outputVoltageBatteryBus = 3423
            message.FileTransferMessage.BatteryTelemetry.outputVoltage5VBus = 3423
            message.FileTransferMessage.BatteryTelemetry.outputVoltage3V3Bus = 3423
            message.FileTransferMessage.BatteryTelemetry.outputCurrentBatteryBus = 3423
            message.FileTransferMessage.BatteryTelemetry.outputCurrent5VBus = 3423
            message.FileTransferMessage.BatteryTelemetry.outputCurrent3V3Bus = 3423
            message.FileTransferMessage.BatteryTelemetry.batteryCurrentDirection = 3423
            message.FileTransferMessage.BatteryTelemetry.motherboardTemp = 3423
            message.FileTransferMessage.BatteryTelemetry.daughterboardTemp1 = 3423
            message.FileTransferMessage.BatteryTelemetry.daughterboardTemp2 = 3423
            message.FileTransferMessage.BatteryTelemetry.daughterboardTemp3 = 3423
            msgType = "BatteryTelemetry"
            break

        elif messageType == "6":
            message.FileTransferMessage.AntennaTelemetry.sideA.deployedAntenna1 = 9368
            message.FileTransferMessage.AntennaTelemetry.sideA.deployedAntenna2 = 9368
            message.FileTransferMessage.AntennaTelemetry.sideA.deployedAntenna3 = 9368
            message.FileTransferMessage.AntennaTelemetry.sideA.deployedAntenna4 = 9368
            message.FileTransferMessage.AntennaTelemetry.sideA.armed = 9368
            message.FileTransferMessage.AntennaTelemetry.sideA.boardTemp = 9368
            message.FileTransferMessage.AntennaTelemetry.sideA.uptime = 9368

            message.FileTransferMessage.AntennaTelemetry.sideB.deployedAntenna1 = 9368
            message.FileTransferMessage.AntennaTelemetry.sideB.deployedAntenna2 = 9368
            message.FileTransferMessage.AntennaTelemetry.sideB.deployedAntenna3 = 9368
            message.FileTransferMessage.AntennaTelemetry.sideB.deployedAntenna4 = 9368
            message.FileTransferMessage.AntennaTelemetry.sideB.armed = 9368
            message.FileTransferMessage.AntennaTelemetry.sideB.boardTemp = 9368
            message.FileTransferMessage.AntennaTelemetry.sideB.uptime = 9368            
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
            message.TelecommandMessage.BeginPass.passLength = 11
            msgType = "BeginPass"
            break
    
        elif messageType == "2":
            message.TelecommandMessage.BeginFileTransfer.resp = 0
            msgType = "BeginFileTransfer"
            break

        elif messageType == "3":
            message.TelecommandMessage.CeaseTransmission.duration = 1
            msgType = "CeaseTransmission"
            break

        elif messageType == "4":
            message.TelecommandMessage.ResumeTransmission.resp = 0
            msgType = "ResumeTransmission"
            break

        elif messageType == "5":
            message.TelecommandMessage.UpdateTime.unixTime = 1123
            msgType = "UpdateTime"
            break

        elif messageType == "6":
            message.TelecommandMessage.Reset.device = 1
            message.TelecommandMessage.Reset.hard = 1
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

useCipher = True

while True:

    messageType = input("Select message type:\n(1) Protocol\n(2) File Transfer\n\
(3) Telecommand\n(4) Check Cipher Key\n(Q) Quit\n")

    if messageType == "1":
        message,fileName = makeProtocolMessage()
        readMessage(radsat.radsat_message(), fileName, xorCipher = useCipher)
        print("Pre-scramble data : " + printDataAsHex("./output/" + fileName))
        addHeader(fileName,xorCipher = useCipher)
        readMessage(radsat.radsat_message(), fileName, xorCipher = useCipher, withHeader=True)
        print("Post-scramble data : " + printDataAsHex("./output/" + fileName,header = True))

    elif messageType == "2":
        message,fileName = makeFileTransferMessage()
        readMessage(radsat.radsat_message(), fileName, xorCipher = useCipher)
        print("Pre-scramble data : " + printDataAsHex("./output/" + fileName))
        addHeader(fileName,xorCipher = useCipher)
        readMessage(radsat.radsat_message(), fileName, xorCipher = useCipher, withHeader=True)
        print("Post-scramble data : " + printDataAsHex("./output/" + fileName,header = True))

    elif messageType == "3":
        message,fileName = makeTelecommandMessage()
        readMessage(radsat.radsat_message(), fileName, xorCipher = useCipher)
        print("Pre-scramble data : " + printDataAsHex("./output/" + fileName))
        addHeader(fileName,xorCipher = useCipher, checkHeader=True)
        readMessage(radsat.radsat_message(), fileName, xorCipher = useCipher, withHeader=True)
        print("Post-scramble data : " + printDataAsHex("./output/" + fileName,header = True))

    elif messageType == "4":
        print(printDataAsHex("./xorCipher/new_key"))

    elif messageType.upper() == "Q":
        print("Exiting ... ")
        break
    
    else:
        print("Invalid entry\n")