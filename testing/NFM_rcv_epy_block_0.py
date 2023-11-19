"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr
import pmt

from skyfield.api import load, wgs84
import serial
import time

class rigControl:
    def __init__(self,lat,lon,satNum):
        self.ts = load.timescale()

        self.gs = wgs84.latlon(lat,lon)

        satellites = load.tle_file("/home/radsat-gs/Desktop/austinsWorkspace/ground_station/src/active.txt")
        print("Loaded %s satellites" % len(satellites))

        catalog = {sat.model.satnum: sat for sat in satellites}
        self.satellite = catalog[satNum]
        print(self.satellite)

    def getAzEl(self):
        dist = self.satellite - self.gs
        position = dist.at((self.ts).now())

        el, az, _ = position.altaz()

        return az.degrees, el.degrees

    def isPass(self):
        _, el = self.getAzEl()

        if el > 5:
            return True
        else:
            return False

    def getDoppler(self,UL_FREQ,DL_FREQ,updateFiles = True):
        dt = 1/86400
        t1 = (self.ts).now() - dt
        t2 = (self.ts).now()
        t3 = (self.ts).now() + dt

        comp1 = self.satellite.at(t1) - self.gs.at(t1)
        comp2 = self.satellite.at(t2) - self.gs.at(t2)
        comp3 = self.satellite.at(t3) - self.gs.at(t3)

        dists = [comp1.distance().m,comp2.distance().m,comp3.distance().m]
        satRate = (np.gradient(dists))[2]

        ul_doppler = satRate * UL_FREQ / 299792458
        dl_doppler = satRate * DL_FREQ / 299792458
 
        print("Sat Rate:",satRate)

        print('UL Doppler: {:.1f} Hz'.format(ul_doppler))
        print('DL Doppler: {:.1f} Hz'.format(dl_doppler))

        if comp3.distance().m <= comp1.distance().m: # Approaching
            UL_FREQ_shifted = UL_FREQ - ul_doppler
            DL_FREQ_shifted = DL_FREQ + dl_doppler
            print("Approaching")

        elif comp3.distance().m > comp1.distance().m: # Leaving
            UL_FREQ_shifted = UL_FREQ + ul_doppler
            DL_FREQ_shifted = DL_FREQ - dl_doppler
            print("Leaving")        

        if updateFiles:
            timeTime = time.time()
            with open("ul_doppler.txt","w") as ul, open("dl_doppler.txt","w") as dl:
                ul.write(str(timeTime) + " " + str(ul_doppler))
                dl.write(str(timeTime) + " " + str(dl_doppler))
                print()


        return UL_FREQ_shifted, DL_FREQ_shifted

    def getPassTimes(self, year, month, day, el = 5):
        start = self.ts.utc(year,month,day)
        stop  = self.ts.utc(year,month,day + 1)

        t,events = self.satellite.find_events(self.gs,start,stop,altitude_degrees = 5.0)
        eventNames = 'rise above %s°' % el, 'culminate', 'set below 5°'
        for ti, event in zip(t, events):
            name = eventNames[event]
            print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

        return t,events


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

