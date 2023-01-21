"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import crc
import os
import sys
import pmt
from gnuradio import gr

def crcAugCcitt():
    width = 16
    poly=0x1021
    init_value=0xFFFF
    final_xor_value=0xFFFF
    reverse_input=True
    reverse_output=True
    configuration = crc.Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
    return crc.CrcCalculator(configuration, True)

pcnt = 0

printFunc = print

def p(*args, **kwargs):
    global pcnt
    printFunc(f'Loc {pcnt}: ', *args, **kwargs)
    pcnt += 1
    
def end():
    global pcnt
    pcnt = 0

#print = p

xmitBuffer = []


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""
    crc_calculator = crcAugCcitt()
    def __init__(self, destinationAddress="RADSAT", destinationIndex=1, sourceAddress="RADSAT", sourceIndex=10, ctl=0xF0, pid=0x03): # UI frame could be 0xf or 0x10
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=None,
            out_sig=[np.byte]
        )
        self.message_port_register_in(pmt.intern('msg_in'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        self.xmitBuffer = []

        self.flag = [(0x7e >> i) & 1 for i in range(8)]
        self.sendFlag = True
        
        self.head = \
        [ord(i)<<1 for i in destinationAddress] + [0b01100000 + ((destinationIndex&0xf)<<1) + 0] + \
        [ord(i)<<1 for i in sourceAddress] + [0b01100000 + ((sourceIndex&0xf)<<1) + 1] + \
        [ctl, pid]
        
        
        
    def handle_msg(self, msg):
        try:
            msgstr = pmt.symbol_to_string(msg)
            if len(msgstr):
                frame = self.head + [ord(i) for i in msgstr]
                checksum = self.crc_calculator.calculate_checksum(bytes(frame))
                frame = frame + [checksum & 0xff, (checksum >> 8) & 0xff]
                buff = self.flag
                ones = 0  # number of consecutive ones
                for byte in frame:
                    for _ in range(8):
                        # Transmit byte LSB first
                        x = byte & 1
                        buff.append(x)
                        ones = ones * x + x
                        if ones == 5:
                            # Bit-stuff
                            buff.append(0)
                            ones = 0
                        byte >>= 1
                        
                frame = buff + self.flag
                self.xmitBuffer.append(frame);
                #print(len(self.xmitBuffer), self.xmitBuffer[-1])
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printFunc(f"Exception {exc_type} on Line {exc_tb.tb_lineno} in {fname}:")
            printFunc(e)
        end()
        
        
    def work(self, input_items, output_items):
        if len(self.xmitBuffer):
            buflen = len(output_items[0])
            _len = len(self.xmitBuffer[0])
            for i in range(min(buflen, _len)):
                output_items[0][i] = self.xmitBuffer[0].pop(0)
            if buflen >= _len:
                self.xmitBuffer.pop(0)
        else:
            _len = 0#min(8*10, len(output_items[0])//8*8)
            out = list(self.flag) * min(10, len(output_items[0])//8)
            #output_items[0][:len(out)] = out
        end()
        return _len
        
if __name__ == "__main__":
    

	data = bytes((0x52, 0x82, 0x88, 0xA6, 0x82, 0xA8, 0xF4, 0xA4, 0x82, 0x88, 0xA6, 0x82, 0xA8, 0x63, 0x03, 0xF0, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20))
	
	data2 = bytes((0xA4, 0x82, 0x88, 0xA6, 0x82, 0xA8, 0xF4, 0xA4, 0x82, 0x88, 0xA6, 0x82, 0xA8, 0x63, 0x03, 0xF0, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20, 0x52, 0x41, 0x44, 0x53, 0x41, 0x54, 0x2D, 0x53, 0x4B, 0x20))
	
	crc_calculator = crcAugCcitt()
	print("False", hex(crc_calculator.calculate_checksum(data)))
	print("True ", hex(crc_calculator.calculate_checksum(data2)))
	
	
	
	
	
	
	
	
	
           
