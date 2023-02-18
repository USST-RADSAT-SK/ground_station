import struct

class RadsatMessage():
    recipe = ""
    name = ""
    size = 0

    def encoder(self):
        pass
    
    def decoder(self, value):
        pass

    def __str__(self):
        return "Incomplete RadsatMessage recipe"
    
    def log(self):
        return ""

def generator(bytes):
    recipes = {
        1 : ObcTelemetry,
        2 : TransceiverTelemetry,
        3 : CameraTelemetry,
        4 : EpsTelemetry,
        5 : BatteryTelemetry,
        6 : AntennaTelemetry,
        7 : DosimeterData,
        8 : ImagePacket,
        9 : ModuleErrorReport,
        10 : ComponentErrorReport,
        11 : ErrorReportSummary,
        12 : Ack,
        13 : Nack,
        14 : BeginPass,
        15 : BeginFileTransfer,
        16 : CeaseTransmission,
        17 : UpdateTime,
        18 : Reset
    }
    
    messageType = bytes[0]
    if messageType in recipes:
        messageObject = recipes[messageType]
        print(messageObject)
        try:
            return messageObject(bytes[1:messageObject.size + 1])
        except:
            print("Decode Error")
            pass
        
    else:
        print("<",messageType,"> not in recipes")

###############################################
#                File Transfer                #
###############################################

class ObcTelemetry(RadsatMessage):
    recipe = "IIIBHHHHHHHHHH"
    name = "OBC Telemetry"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 1
        self.supervisorUptime = 0
        self.obcUptime = 0
        self.obcResetCount = 0
        self.adcUpdateFlag = 0
        self.adcsTemperature = 0
        self.adcsVoltage_3v3in = 0
        self.adcsVoltage_3v3 = 0
        self.adcsVoltage_2v5 = 0
        self.adcsVoltage_1v8 = 0
        self.adcsVoltage_1v0 = 0
        self.adcsCurrent_3v3 = 0
        self.adcsCurrent_1v8 = 0
        self.adcsCurrent_1v0 = 0
        self.adcsVoltage_rtc = 0

        if convert:
            self.decoder(convert)        

    def decoder(self, value):
        self.supervisorUptime,\
        self.obcUptime,\
        self.obcResetCount,\
        self.adcUpdateFlag,\
        self.adcsTemperature,\
        self.adcsVoltage_3v3in,\
        self.adcsVoltage_3v3,\
        self.adcsVoltage_2v5,\
        self.adcsVoltage_1v8,\
        self.adcsVoltage_1v0,\
        self.adcsCurrent_3v3,\
        self.adcsCurrent_1v8,\
        self.adcsCurrent_1v0,\
        self.adcsVoltage_rtc = struct.unpack(ObcTelemetry.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(ObcTelemetry.recipe,
            self.supervisorUptime,
            self.obcUptime,
            self.obcResetCount,
            self.adcUpdateFlag,
            self.adcsTemperature,
            self.adcsVoltage_3v3in,
            self.adcsVoltage_3v3,
            self.adcsVoltage_2v5,
            self.adcsVoltage_1v8,
            self.adcsVoltage_1v0,
            self.adcsCurrent_3v3,
            self.adcsCurrent_1v8,
            self.adcsCurrent_1v0,
            self.adcsVoltage_rtc))

    def __str__(self):
        return f"""obcTelemetry = {{
            Supervisor Uptime = {self.supervisorUptime},
            OBC Uptime = {self.obcUptime},
            OBS Reset Count = {self.obcResetCount},
            ADCS Update Flag = {self.adcUpdateFlag},
            ADCS Temperature = {self.adcsTemperature},
            ADCS Voltage Inout 3v3 = {self.adcsVoltage_3v3in},
            ADCS Voltage 3v3 = {self.adcsVoltage_3v3},
            ADCS Voltage 2v5 = {self.adcsVoltage_2v5},
            ADCS Voltage 1v8 = {self.adcsVoltage_1v8},
            ADCS Voltage 1v0 = {self.adcsVoltage_1v0},
            ADCS Current 3v3 = {self.adcsCurrent_3v3},
            ADCS Current 1v8 = {self.adcsCurrent_1v8},
            ADCS Current 1v0 = {self.adcsCurrent_1v0},
            ADCS Voltage rtc = {self.adcsVoltage_rtc} 
        }}"""
    
    def log(self):
        return f"{self.supervisorUptime},{self.obcUptime},{self.obcResetCount},\
{self.adcUpdateFlag},{self.adcsTemperature},{self.adcsVoltage_3v3in},{self.adcsVoltage_3v3},\
{self.adcsVoltage_2v5},{self.adcsVoltage_1v8},{self.adcsVoltage_1v0},{self.adcsCurrent_3v3},\
{self.adcsCurrent_1v8},{self.adcsCurrent_1v0},{self.adcsVoltage_rtc}"
    
class TransceiverTelemetry(RadsatMessage):
    recipe = "ffffffffffIIfffffffffI"
    name = "Transceiver Telemetry"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 2
        self.txverRxDoppler = 0
        self.txverRxRssi = 0
        self.txverBusVoltage = 0
        self.txverTotalCurrent = 0
        self.txverTxCurrent = 0
        self.txverRxCurrent = 0
        self.txverPowerAmplifierCurrent = 0
        self.txverPowerAmplifierTemperature = 0
        self.txverBoardTemperature = 0
        self.txverUptime = 0
        self.txverFrames = 0
        self.rxverReflectedPower = 0
        self.rxverForwardPower = 0
        self.rxverBusVoltage = 0
        self.rxverTotalCurrent = 0
        self.rxverTxCurrent = 0
        self.rxverRxCurrent = 0
        self.rxverPowerAmplifierCurrent = 0
        self.rxverPowerAmplifierTemperature = 0
        self.rxverBoardTemperature = 0
        self.rxverUptime = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
            self.txverRxDoppler,\
            self.txverRxRssi,\
            self.txverBusVoltage,\
            self.txverTotalCurrent,\
            self.txverTxCurrent,\
            self.txverRxCurrent,\
            self.txverPowerAmplifierCurrent,\
            self.txverPowerAmplifierTemperature,\
            self.txverBoardTemperature,\
            self.txverUptime,\
            self.txverFrames,\
            self.rxverReflectedPower,\
            self.rxverForwardPower,\
            self.rxverBusVoltage,\
            self.rxverTotalCurrent,\
            self.rxverTxCurrent,\
            self.rxverRxCurrent,\
            self.rxverPowerAmplifierCurrent,\
            self.rxverPowerAmplifierTemperature,\
            self.rxverBoardTemperature,\
            self.rxverUptime = struct.unpack(TransceiverTelemetry.recipe, value)

    def encoder(self):
        return(bytes([self.ID]) + struct.pack(TransceiverTelemetry.recipe,
            self.txverRxDoppler,
            self.txverRxRssi,
            self.txverBusVoltage,
            self.txverTotalCurrent,
            self.txverTxCurrent,
            self.txverRxCurrent,
            self.txverPowerAmplifierCurrent,
            self.txverPowerAmplifierTemperature,
            self.txverBoardTemperature,
            self.txverUptime,
            self.txverFrames,
            self.rxverReflectedPower,
            self.rxverForwardPower,
            self.rxverBusVoltage,
            self.rxverTotalCurrent,
            self.rxverTxCurrent,
            self.rxverRxCurrent,
            self.rxverPowerAmplifierCurrent,
            self.rxverPowerAmplifierTemperature,
            self.rxverBoardTemperature,
            self.rxverUptime))
            
    def __str__(self):
        return f"""TransceiverTelemetry = {{
            Txver Rx Doppler = {self.txverRxDoppler},
            Txver Rssi = {self.txverRxRssi},
            Txver Bus Voltage = {self.txverBusVoltage},
            Txver Total Current = {self.txverTotalCurrent},
            Txver Tx Current = {self.txverTxCurrent},
            Txver Rx Current = {self.txverRxCurrent},
            Txver Power Amp Current = {self.txverPowerAmplifierCurrent},
            Txver Power Amp Temp = {self.txverPowerAmplifierTemperature},
            Txver Board Temp = {self.txverBoardTemperature},
            Txver Uptime = {self.txverUptime},
            Txver Frames = {self.txverFrames},
            Rxver Reflected Power = {self.rxverReflectedPower},
            Rxver FWD Power = {self.rxverForwardPower},
            Rxver Bus Voltage = {self.rxverBusVoltage},
            Rxver Total Current = {self.rxverTotalCurrent},
            Rxver Tx Current = {self.rxverTxCurrent},
            Rxver Rx Current = {self.rxverRxCurrent},
            Rxver Power Amp Current = {self.rxverPowerAmplifierCurrent},
            Rxver Power Amp Temp = {self.rxverPowerAmplifierTemperature},
            Rxver Board Temp = {self.rxverBoardTemperature},
            Rxver Uptime = {self.rxverUptime}
            }}"""
    
    def log(self):
        return f"{self.txverRxDoppler},{self.txverRxRssi},{self.txverBusVoltage},{self.txverTotalCurrent},\
{self.txverTxCurrent},{self.txverRxCurrent},{self.txverPowerAmplifierCurrent},{self.txverPowerAmplifierTemperature},\
{self.txverBoardTemperature},{self.txverUptime},{self.txverFrames},{self.rxverReflectedPower},{self.rxverForwardPower},\
{self.rxverBusVoltage},{self.rxverTotalCurrent},{self.rxverTxCurrent},{self.rxverRxCurrent},{self.rxverPowerAmplifierCurrent},\
{self.rxverPowerAmplifierCurrent},{self.rxverBoardTemperature},{self.uptime}"

class CameraTelemetry(RadsatMessage):
    recipe = "Iffff" # TODO
    name = "Camera Telemetry"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 3
        self.uptime = 0
        self.current_3V3 = 0
        self.current_5V = 0
        self.current_SRAM_1 = 0
        self.current_SRAM_2 = 0
        self.overcurrent_SRAM_1 = 0
        self.overcurrent_SRAM_2 = 0
        self.camera1DetectionThreshold = 0
        self.camera1AutoAdjustMode = 0
        self.camera1Exposure = 0
        self.camera1AutoGainControl = 0
        self.camera1BlueGain = 0
        self.camera1RedGain = 0
        self.camera2DetectionThreshold = 0
        self.camera2AutoAdjustMode = 0
        self.camera2Exposure = 0
        self.camera2AutoGainControl = 0
        self.camera2BlueGain = 0
        self.camera2RedGain = 0

        if convert:
            self.decode(convert)

    def decoder(self, value):
            self.uptime,\
            self.current_3V3,\
            self.current_5V,\
            self.current_SRAM_1,\
            self.current_SRAM_2,\
            self.overcurrent_SRAM_1,\
            self.overcurrent_SRAM_2,\
            self.camera1DetectionThreshold,\
            self.camera1AutoAdjustMode,\
            self.camera1Exposure,\
            self.camera1AutoGainControl,\
            self.camera1BlueGain,\
            self.camera1RedGain,\
            self.camera2DetectionThreshold,\
            self.camera2AutoAdjustMode,\
            self.camera2Exposure,\
            self.camera2AutoGainControl,\
            self.camera2BlueGain,\
            self.camera2RedGain = struct.unpack(CameraTelemetry.recipe, value)

    def encoder(self):
        return(bytes([self.ID]) + struct.pack(CameraTelemetry.recipe,
            self.uptime,
            self.current_3V3,
            self.current_5V,
            self.current_SRAM_1,
            self.current_SRAM_2,
            self.overcurrent_SRAM_1,
            self.overcurrent_SRAM_2,
            self.camera1DetectionThreshold,
            self.camera1AutoAdjustMode,
            self.camera1Exposure,
            self.camera1AutoGainControl,
            self.camera1BlueGain,
            self.camera1RedGain,
            self.camera2DetectionThreshold,
            self.camera2AutoAdjustMode,
            self.camera2Exposure,
            self.camera2AutoGainControl,
            self.camera2BlueGain,
            self.camera2RedGain))
            
    def __str__(self):
        return f"""CameraTelemetry = {{
            Uptime = {self.uptime},
            3V3 Current = {self.current_3V3},
            5V Current = {self.current_5V},
            SRAM1 Current = {self.current_SRAM_1},
            SRAM2 Current = {self.current_SRAM_2},
            SRAM1 Overcurrent = {self.overcurrent_SRAM_1},
            SRAM2 Overcurrent = {self.overcurrent_SRAM_2},
            Cam1 Detection Threshold = {self.camera1DetectionThreshold},
            Cam1 Auto Adjust mode = {self.camera1AutoAdjustMode},
            Cam1 Exposure = {self.camera1Exposure},
            Cam1 Auto Gain Control = {self.camera1AutoGainControl},
            Cam1 Blue Gain = {self.camera1BlueGain},
            Cam1 Red Gain = {self.camera1RedGain},
            Cam2 Detection Threshold = {self.camera2DetectionThreshold},
            Cam2 Auto Adjust mode = {self.camera2AutoAdjustMode},
            Cam2 Exposure = {self.camera2Exposure},
            Cam2 Auto Gain Control = {self.camera2AutoGainControl},
            Cam2 Blue Gain = {self.camera2BlueGain},
            Cam2 Red Gain = {self.camera2RedGain}
            }}"""
    
    def log(self):
        return f"{self.uptime},{self.current_3V3},{self.current_5V},{self.current_SRAM_1},\
{self.current_SRAM_2},{self.overcurrent_SRAM_1},{self.overcurrent_SRAM_2},\
{self.camera1DetectionThreshold},{self.camera1AutoAdjustMode},{self.camera1Exposure},\
{self.camera1AutoGainControl},{self.camera1BlueGain},{self.camera1RedGain},\
{self.camera2DetectionThreshold},{self.camera2AutoAdjustMode},{self.camera2Exposure},\
{self.camera2AutoGainControl},{self.camera2BlueGain},{self.camera2RedGain}"

class EpsTelemetry(RadsatMessage):
    recipe = "fffffffffffffff"
    name = "EPS Telemetry"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 4
        self.xPos = 0
        self.xNeg = 0
        self.yPos = 0
        self.yNeg = 0
        self.zPos = 0
        self.zNeg = 0
        self.outputVoltageBCR = 0
        self.outputVoltageBatteryBus = 0
        self.outputVoltage5VBus = 0
        self.outputVoltage3V3Bus = 0
        self.outputCurrentBCR_mA = 0
        self.outputCurrentBatteryBus = 0
        self.outputCurrent5VBus = 0
        self.outputCurrent3V3Bus = 0
        self.PdbTemperature = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.xPos,\
        self.xNeg,\
        self.yPos,\
        self.yNeg,\
        self.zPos,\
        self.zNeg,\
        self.outputVoltageBCR,\
        self.outputVoltageBatteryBus,\
        self.outputVoltage5VBus,\
        self.outputVoltage3V3Bus,\
        self.outputCurrentBCR_mA,\
        self.outputCurrentBatteryBus,\
        self.outputCurrent5VBus,\
        self.outputCurrent3V3Bus,\
        self.PdbTemperature = struct.unpack(EpsTelemetry.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(EpsTelemetry.recipe,
        self.xPos,
        self.xNeg,
        self.yPos,
        self.yNeg,
        self.zPos,
        self.zNeg,
        self.outputVoltageBCR,
        self.outputVoltageBatteryBus,
        self.outputVoltage5VBus,
        self.outputVoltage3V3Bus,
        self.outputCurrentBCR_mA,
        self.outputCurrentBatteryBus,
        self.outputCurrent5VBus,
        self.outputCurrent3V3Bus,
        self.PdbTemperature))

    def __str__(self):
        return f"""EpsTelemetry = {{
        xPos = {self.xPos},
        xNeg = {self.xNeg},
        yPos = {self.yPos},
        yNeg = {self.yNeg},
        zPos = {self.zPos},
        zNeg = {self.zNeg},
        BCR Output Voltage = {self.outputVoltageBCR},
        Battery Bus Voltage{self.outputVoltageBatteryBus},
        5V Bus Voltage = {self.outputVoltage5VBus},
        3V3 Bus Voltage = {self.outputVoltage3V3Bus},
        BCR Output Current = {self.outputCurrentBCR_mA},
        Battery Bus Current = {self.outputCurrentBatteryBus},
        5V Bus Current = {self.outputCurrent5VBus},
        3V3 Bus Current = {self.outputCurrent3V3Bus},
        PDB Temperature = {self.PdbTemperature}
        }}"""
    
    def log(self):
        return f"{self.xPos},{self.xNeg},{self.yPos},{self.yNeg},{self.zPos},{self.zNeg},\
{self.outputVoltageBCR},{self.outputVoltageBatteryBus},{self.outputVoltage5VBus},\
{self.outputVoltage3V3Bus},{self.outputCurrentBCR_mA},{self.outputCurrentBatteryBus},\
{self.outputCurrent5VBus},{self.outputCurrent3V3Bus},{self.PdbTemperature}"

class BatteryTelemetry(RadsatMessage):
    recipe = "fffffffffff"
    name = "Battery Telemetry"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 5
        self.outputVoltageBatteryBus = 0
        self.outputVoltage5VBus = 0
        self.outputVoltage3V3Bus = 0
        self.outputCurrentBatteryBus = 0
        self.outputCurrent5VBus = 0
        self.outputCurrent3V3Bus = 0
        self.batteryCurrentDirection = 0
        self.motherboardTemp = 0
        self.daughterboardTemp1 = 0
        self.daughterboardTemp2 = 0
        self.daughterboardTemp3 = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.outputVoltageBatteryBus,\
        self.outputVoltage5VBus,\
        self.outputVoltage3V3Bus,\
        self.outputCurrentBatteryBus,\
        self.outputCurrent5VBus,\
        self.outputCurrent3V3Bus,\
        self.batteryCurrentDirection,\
        self.motherboardTemp,\
        self.daughterboardTemp1,\
        self.daughterboardTemp2,\
        self.daughterboardTemp3 = struct.unpack(BatteryTelemetry.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(BatteryTelemetry.recipe,
        self.outputVoltageBatteryBus,
        self.outputVoltage5VBus,
        self.outputVoltage3V3Bus,
        self.outputCurrentBatteryBus,
        self.outputCurrent5VBus,
        self.outputCurrent3V3Bus,
        self.batteryCurrentDirection,
        self.motherboardTemp,
        self.daughterboardTemp1,
        self.daughterboardTemp2,
        self.daughterboardTemp3))

    def __str__(self):
        return f"""BatteryTelemetry = {{
        Battery Bus Output Voltage = {self.outputVoltageBatteryBus},
        5V Bus Voltage = {self.outputVoltage5VBus},
        3V3 Bus Voltage = {self.outputVoltage3V3Bus},
        Battery Bus Current = {self.outputCurrentBatteryBus},
        5V Bus Current = {self.outputCurrent5VBus},
        3V3 Bus Current = {self.outputCurrent3V3Bus},
        Battery Current Direction = {self.batteryCurrentDirection},
        Motherboard Temperature = {self.motherboardTemp},
        Daugherboard 1 Temperature = {self.daughterboardTemp1},
        Daugherboard 2 Temperature = {self.daughterboardTemp2},
        Daugherboard 3 Temperature = {self.daughterboardTemp3}        
        }}"""
    
    def log(self):
        return f"{self.outputVoltageBatteryBus},{self.outputVoltage5VBus},{self.outputVoltage3V3Bus},\
{self.outputCurrentBatteryBus},{self.outputCurrent5VBus},{self.outputCurrent3V3Bus},{self.batteryCurrentDirection},\
{self.motherboardTemp},{self.daughterboardTemp1},{self.daughterboardTemp2},{self.daughterboardTemp3}"

class AntennaTelemetry(RadsatMessage):
    recipe = "HHHHHfIHHHHHfI"
    name = "Antenna Telemetry"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 6
        self.antennaADeployedAntenna1 = 0
        self.antennaADeployedAntenna2 = 0
        self.antennaADeployedAntenna3 = 0
        self.antennaADeployedAntenna4 = 0
        self.antennaAArmed = 0
        self.antennaABoardTemp = 0
        self.antennaAUptime = 0
        self.antennaBDeployedAntenna1 = 0
        self.antennaBDeployedAntenna2 = 0
        self.antennaBDeployedAntenna3 = 0
        self.antennaBDeployedAntenna4 = 0
        self.antennaBArmed = 0
        self.antennaBBoardTemp = 0
        self.antennaBUptime = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.antennaADeployedAntenna1,
        self.antennaADeployedAntenna2,
        self.antennaADeployedAntenna3,
        self.antennaADeployedAntenna4,
        self.antennaAArmed,
        self.antennaABoardTemp,
        self.antennaAUptime,
        self.antennaBDeployedAntenna1,
        self.antennaBDeployedAntenna2,
        self.antennaBDeployedAntenna3,
        self.antennaBDeployedAntenna4,
        self.antennaBArmed,
        self.antennaBBoardTemp,
        self.antennaBUptime = struct.unpack(AntennaTelemetry.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(AntennaTelemetry.recipe,
        self.antennaADeployedAntenna1,
        self.antennaADeployedAntenna2,
        self.antennaADeployedAntenna3,
        self.antennaADeployedAntenna4,
        self.antennaAArmed,
        self.antennaABoardTemp,
        self.antennaAUptime,
        self.antennaBDeployedAntenna1,
        self.antennaBDeployedAntenna2,
        self.antennaBDeployedAntenna3,
        self.antennaBDeployedAntenna4,
        self.antennaBArmed,
        self.antennaBBoardTemp,
        self.antennaBUptime))

    def __str__(self):
        return f"""AntennaTelemetry = {{
        Side A Deployed Antenna1 = {self.antennaADeployedAntenna1},
        Side A Deployed Antenna2 = {self.antennaADeployedAntenna2},
        Side A Deployed Antenna3 = {self.antennaADeployedAntenna3},
        Side A Deployed Antenna4 = {self.antennaADeployedAntenna4},
        Side A Armed = {self.antennaAArmed},
        Side A Board Temp = {self.antennaABoardTemp},
        Side A Uptime = {self.antennaAUptime},
        Side B Deployed Antenna1 ={self.antennaBDeployedAntenna1},
        Side B Deployed Antenna2 ={self.antennaBDeployedAntenna2},
        Side B Deployed Antenna3 ={self.antennaBDeployedAntenna3},
        Side B Deployed Antenna4 ={self.antennaBDeployedAntenna4},
        Side B Armed = {self.antennaBArmed},
        Side B Board Temp = {self.antennaBBoardTemp},
        Side B Uptime = {self.antennaBUptime}
        }}"""
    
    def log(self):
        return f"{self.antennaADeployedAntenna1},{self.antennaADeployedAntenna2},{self.antennaADeployedAntenna3},\
{self.antennaADeployedAntenna4},{self.antennaAArmed},{self.antennaABoardTemp},{self.antennaAUptime},\
{self.antennaBDeployedAntenna1},{self.antennaBDeployedAntenna2},{self.antennaBDeployedAntenna3},{self.antennaBDeployedAntenna4},\
{self.antennaBArmed},{self.antennaBBoardTemp},{self.antennaBUptime}"

class DosimeterData(RadsatMessage):
    recipe = "ffffffffffffffff"
    name = "Dosimeter Data"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 7
        self.boardOneChannelZero = 0
        self.boardOneChannelOne = 0
        self.boardOneChannelTwo = 0
        self.boardOneChannelThree = 0
        self.boardOneChannelFour = 0
        self.boardOneChannelFive = 0
        self.boardOneChannelSix = 0
        self.boardOneChannelSeven = 0
        self.boardTwoChannelZero = 0
        self.boardTwoChannelOne = 0
        self.boardTwoChannelTwo = 0
        self.boardTwoChannelThree = 0
        self.boardTwoChannelFour = 0
        self.boardTwoChannelFive = 0
        self.boardTwoChannelSix = 0
        self.boardTwoChannelSeven = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.boardOneChannelZero,\
        self.boardOneChannelOne,\
        self.boardOneChannelTwo,\
        self.boardOneChannelThree,\
        self.boardOneChannelFour,\
        self.boardOneChannelFive,\
        self.boardOneChannelSix,\
        self.boardOneChannelSeven,\
        self.boardTwoChannelZero,\
        self.boardTwoChannelOne,\
        self.boardTwoChannelTwo,\
        self.boardTwoChannelThree,\
        self.boardTwoChannelFour,\
        self.boardTwoChannelFive,\
        self.boardTwoChannelSix ,\
        self.boardTwoChannelSeven = struct.unpack(DosimeterData.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(DosimeterData.recipe,
        self.boardOneChannelZero,
        self.boardOneChannelOne,
        self.boardOneChannelTwo,
        self.boardOneChannelThree,
        self.boardOneChannelFour,
        self.boardOneChannelFive,
        self.boardOneChannelSix,
        self.boardOneChannelSeven,
        self.boardTwoChannelZero,
        self.boardTwoChannelOne,
        self.boardTwoChannelTwo,
        self.boardTwoChannelThree,
        self.boardTwoChannelFour,
        self.boardTwoChannelFive,
        self.boardTwoChannelSix,
        self.boardTwoChannelSeven))

    def __str__(self):
        return f"""DosimeterData = {{
        Board 1 Channel 0 = {self.boardOneChannelZero}
        Board 1 Channel 1 = {self.boardOneChannelOne}
        Board 1 Channel 2 = {self.boardOneChannelTwo}
        Board 1 Channel 3 = {self.boardOneChannelThree}        
        Board 1 Channel 4 = {self.boardOneChannelFour}        
        Board 1 Channel 5 = {self.boardOneChannelFive}        
        Board 1 Channel 6 = {self.boardOneChannelSix}        
        Board 1 Channel 7 = {self.boardOneChannelSeven}        
        Board 2 Channel 0 = {self.boardTwoChannelZero}        
        Board 2 Channel 1 = {self.boardTwoChannelOne}        
        Board 2 Channel 2 = {self.boardTwoChannelTwo}        
        Board 2 Channel 3 = {self.boardTwoChannelThree}        
        Board 2 Channel 4 = {self.boardTwoChannelFour}        
        Board 2 Channel 5 = {self.boardTwoChannelFive}        
        Board 2 Channel 6 = {self.boardTwoChannelSix}        
        Board 2 Channel 7 = {self.boardTwoChannelSeven}        
        }}"""
    
    def log(self):
        return f"{self.boardOneChannelZero},{self.boardOneChannelOne},{self.boardOneChannelTwo},\
{self.boardOneChannelThree},{self.boardOneChannelFour},{self.boardOneChannelFive},\
{self.boardOneChannelSix},{self.boardOneChannelSeven},{self.boardTwoChannelZero},\
{self.boardTwoChannelOne},{self.boardTwoChannelTwo},{self.boardTwoChannelThree},\
{self.boardTwoChannelFour},{self.boardTwoChannelFive},{self.boardTwoChannelSix},\
{self.boardTwoChannelSeven}"

class ImagePacket(RadsatMessage):
    recipe = "ffffffffffffffff" # TODO
    name = "Image Packet"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 8
        self.id = 0
        self.type = 0
        self.data = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.id,\
        self.type,\
        self.data = struct.unpack(ImagePacket.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(ImagePacket.recipe,
        self.id,
        self.type,
        self.data
        ))

    def __str__(self):
        return f"""ImagePacket = {{
        Image ID = {self.id},
        Image Type = {self.type},
        Image Bytes = {self.data}
        }}"""
    
    def log(self):
        return f"{self.id},{self.type},{self.data}"

class ModuleErrorReport(RadsatMessage):
    recipe = "ffffffffffffffff" # TODO
    name = "Module Error Report"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 9
        self.moduleId = 0
        self.moduleError = 0
        self.moduleTimeRecorded = 0
        self.moduleCount = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.moduleId,\
        self.moduleError,\
        self.moduleTimeRecorded,\
        self.moduleCount = struct.unpack(ModuleErrorReport.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(ModuleErrorReport.recipe,
            self.moduleId,
            self.moduleError,
            self.moduleTimeRecorded,
            self.moduleCount
            ))

    def __str__(self):
        return f"""ModuleErrorReport = {{
            Module ID = {self.moduleId},
            Module Error = {self.moduleError},
            Module Time Recorded = {self.moduleTimeRecorded},
            Module Error Count = {self.moduleCount}
        }}"""
    
    def log(self):
        return f"{self.moduleId},{self.moduleError},{self.moduleTimeRecorded},{self.moduleCount}"

class ComponentErrorReport(RadsatMessage):
    recipe = "ffffffffffffffff" # TODO
    name = "Component Error Report"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 10
        self.componentId = 0
        self.componentError = 0
        self.componentTimeRecorded = 0
        self.componentCount = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.componentId,\
        self.componentError,\
        self.componentTimeRecorded,\
        self.componentCount = struct.unpack(ComponentErrorReport.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(ComponentErrorReport.recipe,
            self.componentId,
            self.componentError,
            self.componentTimeRecorded,
            self.componentCount
            ))

    def __str__(self):
        return f"""ComponentErrorReport = {{
            Component ID = {self.componentId},
            Component Error = {self.componentError},
            Component Time Recorded = {self.componentTimeRecorded},
            Component Error Count = {self.componentCount}
        }}"""
    
    def log(self):
        return f"{self.componentId},{self.componentError},{self.componentTimeRecorded},{self.componentCount}"
    
class ErrorReportSummary(RadsatMessage):
    recipe = "ffffffffffffffff" # TODO
    name = "Error Report Summary"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 11
        self.moduleErrorCount = 0
        self.componentErrorCount = 0

    def decoder(self, value):
        self.moduleErrorCount,\
        self.componentErrorCount = struct.unpack(ErrorReportSummary.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(ErrorReportSummary.recipe,
            self.moduleErrorCount,
            self.componentErrorCount
            ))

    def __str__(self):
        return f"""ErrorReportSummary = {{
            Module Error Count = {self.moduleErrorCount},
            Component Error Count = {self.componentErrorCount},
        }}"""
    
    def log(self):
        return f"{self.moduleErrorCount},{self.componentErrorCount}"

###############################################
#                  Protocol                   #
###############################################

class Ack(RadsatMessage):
    recipe = "H"
    name = "Acknowledge"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 12
        self.resp = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
            self.resp = struct.unpack(Ack.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(Ack.recipe,
            self.resp
            ))

    def __str__(self):
        return f"""Ack = {{
            Response = {self.resp},
        }}"""
    
    def log(self):
        return f"{self.resp}"
    
class Nack(RadsatMessage):
    recipe = "H"
    name = "Not Acknowledge"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 13
        self.resp = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
            self.resp = struct.unpack(Nack.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(Nack.recipe,
            self.resp
            ))

    def __str__(self):
        return f"""Nack = {{
            Response = {self.resp},
        }}"""
    
    def log(self):
        return f"{self.resp}"
    
###############################################
#                Telecommand                  #
###############################################

class BeginPass(RadsatMessage):
    recipe = "H"
    name = "Begin Pass"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 14
        self.passLength = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.passLength = struct.unpack(BeginPass.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(BeginPass.recipe,
            self.passLength
            ))

    def __str__(self):
        return f"""BeginPass = {{
            Pass Length = {self.passLength},
        }}"""
    
    def log(self):
        return f"{self.passLength}"
    
class BeginFileTransfer(RadsatMessage):
    recipe = "H"
    name = "Begin File Transfer"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 15
        self.resp = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.resp = struct.unpack(BeginFileTransfer.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(BeginFileTransfer.recipe,
            self.resp
            ))

    def __str__(self):
        return f"""BeginFileTransfer = {{
            Response = {self.resp},
        }}"""
    
    def log(self):
        return f"{self.resp}"
    
class CeaseTransmission(RadsatMessage):
    recipe = "H"
    name = "Cease Transmission"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 16
        self.duration = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
            self.duration = struct.unpack(CeaseTransmission.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(CeaseTransmission.recipe,
            self.duration
            ))

    def __str__(self):
        return f"""CeaseTransmission = {{
            Response = {self.duration},
        }}"""
    
    def log(self):
        return f"{self.duration}"
    
    recipe = "ffffffffffffffff"
    name = "Resume Transmission"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.resp = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
            self.resp = struct.unpack(ResumeTransmission.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(ResumeTransmission.recipe,
            self.resp
            ))

    def __str__(self):
        return f"""ResumeTransmission = {{
            Response = {self.resp},
        }}"""
    
    def log(self):
        return f"{self.resp}"
    
class UpdateTime(RadsatMessage):
    recipe = "H"
    name = "Update Time"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 17
        self.unixTime = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
            self.unixTime = struct.unpack(UpdateTime.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(UpdateTime.recipe,
            self.unixTime
            ))

    def __str__(self):
        return f"""UpdateTime = {{
            Unix Time = {self.unixTime},
        }}"""
    
    def log(self):
        return f"{self.unixTime}"
    
class Reset(RadsatMessage):
    recipe = "BB"
    name = "Reset"
    size = struct.calcsize(recipe)

    def __init__(self, convert=None):
        self.ID = 18
        self.device = 0
        self.hard = 0

        if convert:
            self.decoder(convert)

    def decoder(self, value):
        self.device,\
        self.hard = struct.unpack(Reset.recipe, value)
        
    def encoder(self):
        return(bytes([self.ID]) + struct.pack(Reset.recipe,
            self.device,
            self.hard
            ))

    def __str__(self):
        return f"""Reset = {{
            Reset Device = {self.device},
            Hard Reset  = {self.hard}
        }}"""
    
    def log(self):
        return f"{self.device},{self.hard}"
    
if __name__ == "__main__":
    import random
    radsatMsg = RadsatMessage()
    dosData = DosimeterData()

    dosData.boardOneChannelZero = 100*random.random()
    dosData.boardOneChannelOne = 100*random.random()
    dosData.boardOneChannelTwo = 100*random.random()
    dosData.boardOneChannelThree = 100*random.random()
    dosData.boardOneChannelFour = 100*random.random()
    dosData.boardOneChannelFive = 100*random.random()
    dosData.boardOneChannelSix = 100*random.random()
    dosData.boardOneChannelSeven = 100*random.random()
    dosData.boardTwoChannelZero = 100*random.random()
    dosData.boardTwoChannelOne = 100*random.random()
    dosData.boardTwoChannelTwo = 100*random.random()
    dosData.boardTwoChannelThree = 100*random.random()
    dosData.boardTwoChannelFour = 100*random.random()
    dosData.boardTwoChannelFive = 100*random.random()
    dosData.boardTwoChannelSix = 100*random.random()
    dosData.boardTwoChannelSeven = 100*random.random()

    print(dosData)

    encodedBytes = dosData.encoder()
    print(encodedBytes)
    
    print(generator(encodedBytes))