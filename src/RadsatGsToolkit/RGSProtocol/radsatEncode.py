import os
from time import *
from datetime import date
from crc import CrcCalculator, Configuration

rxHeader = ["recvTime","preamble","checkSum","length","timestamp","msgClass","dataType",
            "mode","uptime","rtcTime","rtcTemperature",
            "rxDoppler","rxRssi","busVoltage","totalCurrent","txCurrent","rxCurrent","powerAmplifierCurrent","powerAmplifierTemperature","boardTemperature","uptime","frames",
            "reflectedPower","forwardPower","busVoltage","totalCurrent","txCurrent","rxCurrent","powerAmplifierCurrent","powerAmplifierTemperature","boardTemperature","uptime",
            "current_3V3","current_5V","current_SRAM_1","current_SRAM_2","overcurrent_SRAM_1","overcurrent_SRAM_2",
            "detectionThreshold","autoAdjustMode","exposure","autoGainControl","blueGain","redGain",
            "detectionThreshold","autoAdjustMode","exposure","autoGainControl","blueGain","redGain",
            "xPos","xNeg","yPos","yNeg","zPos","zNeg",
            "outputVoltageBCR","outputVoltageBatteryBus","outputVoltage5VBus","outputVoltage3V3Bus","outputCurrentBCR_mA","outputCurrentBatteryBus","outputCurrent5VBus","outputCurrent3V3Bus","PdbTemperature",
            "outputVoltageBatteryBus","outputVoltage5VBus","outputVoltage3V3Bus","outputCurrentBatteryBus","outputCurrent5VBus","outputCurrent3V3Bus","batteryCurrentDirection","motherboardTemp","daughterboardTemp1","daughterboardTemp2","daughterboardTemp3",
            "deployedAntenna1","deployedAntenna2","deployedAntenna3","deployedAntenna4","armed","boardTemp","uptime",
            "deployedAntenna1","deployedAntenna2","deployedAntenna3","deployedAntenna4","armed","boardTemp","uptime",
            "channelZero","channelOne","channelTwo","channelThree","channelFour","channelFive","channelSix","channelSeven",
            "channelZero","channelOne","channelTwo","channelThree","channelFour","channelFive","channelSix","channelSeven",
            "id","type","data",
            "module","error",
            "component","error",
            "timeRecorded","count"]

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

def sendToFile(fileName,msgList,preamble,checkSum,length,timeStamp):
    if os.path.isfile(fileName) == False:
        with open(fileName,"w") as f:
            f.write("RADSAT-SK Data Log : " + getDateString() + "\n")
            for i in rxHeader:
                f.write(i + ",")
            f.write("\n")

    rowWrite = [str(int(time())),str(preamble),str(checkSum),str(length),str(timeStamp),msgList[0],msgList[1]]

    print(msgList)

    for i in range(0,len(rxHeader)):
        for j in range(0,len(msgList)):
            if rxHeader[i] in msgList[j]:
                rowWrite.append("10000")
            else:
                rowWrite.append(" ")
    
    print(rowWrite)

    with open(fileName,"a") as f:
        for i in rowWrite:
            f.write(i + ",")
        f.write("\n")


def getDateString():
    now = date.today().strftime("%Y_%m_%d")
    return(now)
