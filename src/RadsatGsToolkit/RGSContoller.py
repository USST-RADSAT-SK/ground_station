from skyfield.api import load, wgs84
import serial
import time
import numpy as np
import os

class rigControl:
    def __init__(self,lat,lon,satNum):
        self.satNum = satNum
        self.ts = load.timescale()

        self.gs = wgs84.latlon(lat,lon)

        self.url = 'http://celestrak.org/NORAD/elements/active.txt'
        self.path = "/home/radsat-gs/Desktop/austinsWorkspace/ground_station/src/active.txt"
        
        self.updateTles()


    def updateTles(self):
        
        noFile = False

        try:
            fileTimeDelta = round((time.time() - os.path.getmtime(self.path))/86400,3)
            print("%s days since TLE file update" % fileTimeDelta)
        
        except FileNotFoundError:
            print("TLE file not found! Regenerating...")
            fileTimeDelta = 100

        if fileTimeDelta > 1 or noFile:
            satellites = load.tle_file(self.url)
            print("Loaded %s satellites from new file" % len(satellites))
        else:
            satellites = load.tle_file(self.path)

        catalog = {sat.model.satnum: sat for sat in satellites}
        self.satellite = catalog[self.satNum]
        print(self.satellite)


    def getAzEl(self):
        dist = self.satellite - self.gs
        position = dist.at((self.ts).now())

        el, az, _ = position.altaz()

        print('Azimuth:', az)
        print('Elevation:', el)
        return int(az.degrees), int(el.degrees)

    def isPass(self):
        _, el = self.getAzEl()
        
        print("Elevation = %s degrees" % el)

        if el >= 0:
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


class rotControl:
    def __init__(self):
        connected = False
        while not connected:
            try:
                self.s = serial.Serial(port = "/dev/ttyUSB0", baudrate = 9600, timeout = 1)
                self.s.flush()
                self.s.write(("c2\r\n").encode())
                resp = self.s.readline(1024).decode().strip("\n\r") 
                print("<%s>" % resp)

                if resp != "":
                    connected = True
                    print("Connection succesful")

            except Exception as e:
                print("Rotator Error :",e)
                exit()            
        


    def setPos(self,az,el):
        self.s.write(("W" + f'{int(float(az)):03}' + " " + f'{int(float(el)):03}' + "\r\n").encode())
        self.s.readline(1024)

    def getPos(self):
        az = el = ""
        while az == "" or el == "":
            try:
                self.s.write(("c2\r\n").encode())
                azel = (self.s.readline(1024).decode().strip("\n")).split(" ")
                az = azel[0][3:]
                el = azel[2][3:]

            except Exception as e:
                print(e)
                self.s.flush()
                print("<%s>" % azel)
                az = el = ""

        return int(az),int(el)
    
    def rotateRight(self):
        self.s.write(("r\r\n").encode())
        self.s.readline(1024)

    def rotateLeft(self):
        self.s.write(("l\r\n").encode())
        self.s.readline(1024)

    def rotateUp(self):
        self.s.write(("u\r\n").encode())
        self.s.readline(1024)

    def rotateDown(self):
        self.s.write(("d\r\n").encode())
        self.s.readline(1024)

    def rotateStop(self):
        self.s.write(("s\r\n").encode())
        self.s.readline(1024)

    def close(self):
        print("Closing rotator")
        self.s.close()

if __name__ == "__main__" :    
    from time import sleep

    UL_FREQ = 145.83E6
    DL_FREQ = 435.4E6

    gsLat = 52.144176
    gsLon = -106.612910
    ISS = 25544
    
    radsat = rigControl(gsLat,gsLon,ISS)
