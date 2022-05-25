import numpy as np
from gnuradio import gr


def limitChr(chars):
    """
    Routine to convert a intiger to a ASCII character but exclude non-visual SCHII codes.

        chars: a integer or a list of integers representing a ASCII code.

       return: a string of converted ASCII characters.
    """
    if not isinstance(chars, (list, np.ndarray)):
        chars = [chars]
    output = ""
    for i in chars:
        if ((0x1F < i < 0x7F) and i != 0x8D) or i == 10 or (0xA0 < i <= 0xFF):
            output += chr(i)
    return output

def insertBit(val, boolVal):
    return (val << type(val)(1)) + boolVal


class deframer:
    def __init__(self, flag=0b01111110, maxLen=255, minLen=0):
        self._flag = flag
        self._max = maxLen - 8  # subtract flag lengths
        self._min = minLen - 8
        self.__startFlag = np.uint8(0)
        self.__endFlag = np.uint8(0)
        self.__body = np.zeros((maxLen,), dtype=np.uint8)
        self.__bodyLen = -8
        self.__outputBuffer = []


    def work(self, input_items):
        """
        This is where the work is done in the GNURadio block.

        algorith: double slidding window searching for start/end flag with both windows
        encapsulating the message body implemented as state mechine.
        """
        inputLength = len(input_items)
        output = []
        i = 0
        while i < inputLength:  # Recursive like algorithm.
            if self.__bodyLen >= self._max:  # Reset window message body to bigger them max.
                self.__startFlag = np.uint8(0)
                self.__endFlag = np.uint8(0)
                self.__bodyLen = -8
            if self.__startFlag != self._flag:  # Case: first flas search.
                self.__startFlag = insertBit(self.__startFlag, input_items[i])
            elif self.__endFlag != self._flag:  # Case: last flag search.
                if self.__bodyLen >= 0:
                    self.__body[self.__bodyLen // 8] = insertBit(self.__body[self.__bodyLen // 8], self.__endFlag >> np.uint8(7))
                self.__endFlag = insertBit(self.__endFlag, input_items[i])
                self.__bodyLen += 1
            elif (self.__startFlag == self._flag and self.__endFlag == self._flag):  # Case: message found and validation.
                if not self.__bodyLen % 8 and self.__bodyLen >= self._min:
                    output.append(self.__body[0:self.__bodyLen//8])
                self.__startFlag = np.uint8(0)
                self.__endFlag = np.uint8(0)
                self.__bodyLen = -8
            i += 1
        return output
        
        
class blk(gr.sync_block):
    def __init__(self, flag=0b01111110, maxLen=255, minLen=0):
        gr.sync_block.__init__(
            self,
            name="CLI Print Sink",
            in_sig=[np.uint8],
            out_sig=None,
        )
        self.deframerObj = deframer(flag, maxLen, minLen)
        
    def work(self, input_items, output_items):
        for i in self.deframerObj.work(input_items[0]):
            # print(('{:02X}'*len(i)).format(*i))
            print(limitChr(i))
            # print('{:<.60s}'.format(''.join([f"{J:02X}" for J in i])))
        self.consume(0, len(input_items[0]))  # empty input. fixes overflow
        return 0

if __name__ == "__main__":
    testobj = deframer() 
    
    flag = f'{0x7e:08b}'
    body = "000000000000000"+flag
    bodyText = "test text 1234"
    hexBody =  ''
    for i in bodyText:
        hexBody += f'{ord(i):02X}'
        body += f'{ord(i):08b}'
    body += flag+"00000000000000000"
    data = []
    for i in body:
        data.append(np.uint8(int(i)))
    print(hexBody)
    testobj.work((data,),data)
    
    
