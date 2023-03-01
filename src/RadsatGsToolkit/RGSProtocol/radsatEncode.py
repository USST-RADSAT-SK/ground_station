import os
from time import *
from datetime import datetime
from crc import CrcCalculator, Configuration

rxHeader = [["recvTime","preamble","checkSum","length","timestamp","msgID"],
            ["supervisorUptime","obcUptime","obcResetCount","adcUpdateFlag","adcsTemperature","adcsVoltage_3v3in","adcsVoltage_3v3","adcsVoltage_2v5","adcsVoltage_1v8","adcsVoltage_1v0","adcsCurrent_3v3","adcsCurrent_1v8","adcsCurrent_1v0","adcsVoltage_rtc"],
            ["rxDoppler","rxRssi","busVoltage","totalCurrent","txCurrent","rxCurrent","powerAmplifierCurrent","powerAmplifierTemperature","boardTemperature","uptime","frames",
             "reflectedPower","forwardPower","busVoltage","totalCurrent","txCurrent","rxCurrent","powerAmplifierCurrent","powerAmplifierTemperature","boardTemperature","uptime"],
            ["uptime","current_3V3","current_5V","current_SRAM_1","current_SRAM_2","overcurrent_SRAM_1","overcurrent_SRAM_2",
             "camera1DetectionThreshold","camera1AutoAdjustMode","camera1Exposure","camera1AutoGainControl","camera1BlueGain","camera1RedGain",
             "camera2DetectionThreshold","camera2AutoAdjustMode","camera2Exposure","camera2AutoGainControl","camera2BlueGain","camera2RedGain"],
            ["outputVoltageBCR","outputVoltageBatteryBus","outputVoltage5VBus","outputVoltage3V3Bus","outputCurrentBCR_mA","outputCurrentBatteryBus","outputCurrent5VBus","outputCurrent3V3Bus","PdbTemperature","sunSensorBCR1Voltage",\
             "sunSensorSA1ACurrent","sunSensorSA1BCurrent","sunSensorBCR2Voltage",
             "sunSensorSA2ACurrent","sunSensorSA2BCurrent","sunSensorBCR3Voltage",
             "sunSensorSA3ACurrent","sunSensorSA3BCurrent"],
            ["outputVoltageBatteryBus","outputVoltage5VBus","outputVoltage3V3Bus","outputCurrentBatteryBus","outputCurrent5VBus","outputCurrent3V3Bus","batteryCurrentDirection","motherboardTemp","daughterboardTemp1","daughterboardTemp2","daughterboardTemp3"],
            ["deployedAntenna1","deployedAntenna2","deployedAntenna3","deployedAntenna4","armed","boardTemp","uptime",
             "deployedAntenna1","deployedAntenna2","deployedAntenna3","deployedAntenna4","armed","boardTemp","uptime"],
            ["channelZero","channelOne","channelTwo","channelThree","channelFour","channelFive","channelSix","channelSeven",
             "channelZero","channelOne","channelTwo","channelThree","channelFour","channelFive","channelSix","channelSeven"],
            ["moduleId","moduleError","moduleTimeRecorded","moduleCount"],
            ["componentId","componentError","componentTimeRecorded","componentCount"],
            ["moduleCount","componentCount"],
            ["timeRecorded","count"],
            [""]] # TODO - Fix ADCS stuff and impliment finalized versions of messages

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

def sendToFile(fileName,msgGenerated,preamble,checkSum,length,timeStamp):
    if os.path.isfile(fileName) == False:
        with open(fileName,"w") as f:
            f.write("RADSAT-SK Data Log : " + getDateString() + "\n")
            for i in range(0,len(rxHeader)):
                for j in range(0,len(rxHeader[i])):
                    f.write(rxHeader[i][j] + ",")
            f.write("\n")

    rowWrite = [str(int(time())),str(preamble),str(checkSum),str(length),str(timeStamp),str(msgGenerated.ID)]
    
    msgDataList = (msgGenerated.log()).split(",")

    for i in range(1,len(rxHeader)):
        for j in range(0,len(rxHeader[i])):
            if i == msgGenerated.ID:
                msgDataList[j]
                rowWrite.append(str(msgDataList[j]))
            else:
                rowWrite.append("")

    with open(fileName,"a") as f:
        for i in rowWrite:
            f.write(i + ",")
        f.write("\n")

def getDateString(time = False):
    now = datetime.now()
    
    if time:
        timeString = now.strftime("%m/%d/%Y %H:%M:%S")
    else:
        timeString = now.strftime("%Y_%m_%d")
    return(timeString)