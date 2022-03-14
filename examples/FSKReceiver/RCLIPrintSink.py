import numpy as np
from gnuradio import gr


def limitChr(chars):
    """
    Routine to convert a intiger to a ASCII character but exclude non-visual SCHII codes.

        chars: a integer or a list of integers representing a ASCII code.

       return: a string of converted ASCII characters.
    """
    if not isinstance(chars, list):
        chars = [chars]
    output = ""
    for i in chars:
        if ((0x1F < i < 0x7F) and i != 0x8D) or i == 10 or (0xA0 < i <= 0xFF):
            output += chr(i)
    return output


class blk(gr.sync_block):
    def __init__(self, flag=0b01111110, maxLen=255, minLen=0):
        gr.sync_block.__init__(
            self,
            name="CLI Print Sink",
            in_sig=[np.int8],
            out_sig=None,
        )
        self._flag = flag
        self._max = maxLen - 16  # subtract flag lengths
        self._min = minLen - 16
        self.__startFlag = 0
        self.__endFlag = 0
        self.__body = []

    def work(self, input_items, output_items):
        """
        This is where the work is done in the GNURadio block.

        algorith: double slidding window searching for start/end flag with both windows
        encapsulating the message body implemented as state mechine.
        """
        inputLength = len(input_items)
        i = 0
        while i < inputLength:  # Recursive like algorithm.
            if (
                len(self.__body) > self._max
            ):  # Reset window message body to bigger them max.
                self.__startFlag = 0
                self.__endFlag = 0
                self.__body = []
            if self.__startFlag != self._flag:  # Case: first flas search.
                self.__startFlag = ((self.__startFlag << 1) + input_items[0][i]) & 0xFF
            elif self.__endFlag != self._flag:  # Case: last flag search.
                self.__body.append(str((self.__endFlag & 0b10000000) >> 7))
                self.__endFlag = ((self.__endFlag << 1) + input_items[0][i]) & 0xFF
            elif (
                self.__startFlag == self._flag and self.__endFlag == self._flag
            ):  # Case: message found and validation.
                if not len(self.__body) % 8 and len(self.__body) > self._min:
                    print(f'{len(input_items[0]): 4} - {"".join(self.__body[8:])}')
                self.__startFlag = 0
                self.__endFlag = 0
                self.__body = []
            i += 1
        self.consume(0, inputLength)  # empty input. fixes overflow
        return 0
