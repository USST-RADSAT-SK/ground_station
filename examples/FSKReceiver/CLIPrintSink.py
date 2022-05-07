"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


def limitChr(chars):
    if not isinstance(chars, list):
        chars = [chars]
    output = ''
    for i in chars:
        if ((0x1f < i < 0x7f) and i != 0x8d) or i == 10 or (0xa0 < i <= 0xff):
            output += chr(i)
    return output



class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, flag=0b01111110, maxLen=255, minLen=0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='CLI Print Sink',   # will show up in GRC
            in_sig=[np.int8],
            out_sig=None  # out_sig=[np.uint8]
        )
        self.flag = flag
        self.max = maxLen - 16
        self.min = minLen - 16
        self.startFlag = 0
        self.endFlag = 0
        self.body = []
        self.bodySize = 0
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).


    def work(self, input_items, output_items):
        inputLength = len(input_items)
        i = 0
        while i < inputLength:
            if len(self.body) > self.max:
                self.startFlag = 0
                self.endFlag = 0
                self.body = []
            if self.startFlag != self.flag:
                self.startFlag = ((self.startFlag << 1) + input_items[0][i]) & 0xff
            elif self.endFlag != self.flag:
                self.body.append(str((self.endFlag & 0b10000000) >> 7))
                self.endFlag = ((self.endFlag << 1) + input_items[0][i]) & 0xff
            elif self.startFlag == self.flag and self.endFlag == self.flag:
                if not len(self.body) % 8 and len(self.body) > self.min:
                    
                    print(f'{len(input_items[0]): 4} - {"".join(self.body[8:])}')
                self.startFlag = 0
                self.endFlag = 0
                self.body = []
            i += 1
        self.consume(0,inputLength) # empty input. fixes overflow
        return 0
        
