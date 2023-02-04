class Generator:
    from .protoPy import RRadsat_pb2 as radsat
    import google

    def __init__(self):
        self.processFiles()

    def __repr__(self):
        return f"<RADSAT proto generator>"
    
    def processFiles(self):
        self.message = self.radsat.radsat_message()

    def protocol(self, ack = True):
        msg = self.message
        if ack:
            msg.ProtocolMessage.Ack.resp = 1
        else:
            msg.ProtocolMessage.Nack.resp = 1
        return msg.SerializeToString()

    def beginPass(self, passLength):
        msg = self.message
        msg.TelecommandMessage.BeginPass.passLength = passLength
        return msg.SerializeToString()

    def beginFileTransfer(self):
        msg = self.message
        msg.TelecommandMessage.BeginFileTransfer.resp = 0
        return msg.SerializeToString()
    
    def ceaseTransmission(self, duration):
        msg = self.message
        msg.TelecommandMessage.CeaseTransmission.duration = duration
        return msg.SerializeToString()

    def resumeTransmission(self):
        msg = self.message
        msg.TelecommandMessage.ResumeTransmission.resp = 0
        return msg.SerializeToString()
    
    def updateTime(self, unixTime):
        msg = self.message
        msg.TelecommandMessage.UpdateTime.unixTime = unixTime
        return msg.SerializeToString()

    def reset(self, device, hard = 0):
        """Device: Obc = 0, Transmitter = 1, Receiver = 2, AntennaSideA = 3, AntennaSideB = 4"""
        msg = self.message
        msg.TelecommandMessage.Reset.device = device
        msg.TelecommandMessage.Reset.hard = hard
        return msg.SerializeToString()
    
if __name__ == "__main__":
    from radsatEncode import *
    
    gen = Generator()
    msgObj = gen.message

    msg1 = gen.protocol(True)
    print("Input message:", msg1)
    print("Message size:", msg1.__sizeof__())
    print("Type : ", type(msg1))

    msg2 = addHeader(msg1)
    print("Header message:", msg2)
    print("Message with header size:", msg2.__sizeof__())
    print("Type : ", type(msg2))

    decode1 = stripHeader(msg2)
    print("Decoded bytes:", decode1)
    print("Message size:", decode1.__sizeof__())
    print("Type : ", type(decode1))    

    msgObj.ParseFromString(decode1)
    print("Decoded struct:\n",msgObj)
    print("Type : ", type(msgObj))    
    
    encodedMsg = xorCipher(msg2)
    print("XOR'ed message:", encodedMsg)