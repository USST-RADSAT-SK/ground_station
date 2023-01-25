class Nrzi:
    def __init__(self):
        self.modState = 1
        self.demodState = 0

    def encode(self, values):
        output = []
        for i in values:
            self.modState = self.modState ^ i ^ 1
            output.append(self.modState)
        return output

    def decode(self, values):
        output = []
        for i in values:
            output.append(self.demodState ^ i ^ 1)
            self.demodState = i
        return output


class G3ruh:
    def __init__(self):
        self.ecBuffer = 0
        self.dcBuffer = 0

    def encode(self, values):
        output = []
        for i in values:
            val = (self.ecBuffer ^ (self.ecBuffer >> 5) ^ i) & 1
            self.ecBuffer = ((self.ecBuffer | (val << 17)) >> 1)
            output.append(val)
        return output

    def decode(self, values):
        output = []
        for i in values:
            self.dcBuffer  = self.dcBuffer >> 1 | i & 1) << 17
            output.append((self.dcBuffer ^ self.dcBuffer >> 5 ^ i) & 1)
        return output
