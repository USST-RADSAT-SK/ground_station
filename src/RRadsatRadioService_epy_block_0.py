"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr
import pmt

from RadsatGsToolkit import *
from skyfield.api import load, wgs84
import serial

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, upBaseFreq=100e6, dnBaseFreq=100e6, gsLat=52.144176, gsLon=-106.612910, noradId=25544):
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Doppler Block',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        
        self.uplinkFreq = upBaseFreq
        self.dnlinkFreq = dnBaseFreq
        self.controller = rigControl(gsLat, gsLon, noradId)
        
        # Register message ports
        self.message_port_register_out(pmt.intern('uplk_freq_msg'))
        self.message_port_register_out(pmt.intern('dnlk_freq_msg'))
        self.message_port_register_out(pmt.intern('pass_msg'))
        self.message_port_register_in(pmt.intern('update_msg'))
        self.set_msg_handler(pmt.intern('update_msg'), self.sendInfo)
        
    def sendInfo(self, msg):
        upFreq, dnFreq = self.controller.getDoppler(self.uplinkFreq, self.dnlinkFreq)
        isInPass = self.controller.isPass()
        self.message_port_pub(pmt.intern('uplk_freq_msg'), pmt.cons(pmt.intern('value'),    pmt.to_pmt(upFreq)))
        self.message_port_pub(pmt.intern('dnlk_freq_msg'), pmt.cons(pmt.intern('value'),    pmt.to_pmt(dnFreq)))
        self.message_port_pub(pmt.intern('pass_msg'),      pmt.cons(pmt.intern('pass_msg'), pmt.to_pmt(isInPass)))
        
    def stop(self):
        return True

