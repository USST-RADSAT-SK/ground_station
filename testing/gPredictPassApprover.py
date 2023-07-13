from skyfield.api import load, wgs84
import serial
import time

class rigControl:
    def __init__(self,lat,lon,satNum):
        self.ts = load.timescale()

        self.gs = wgs84.latlon(lat,lon)

        url = 'http://celestrak.org/NORAD/elements/active.txt'
        satellites = load.tle_file(url)
        print("Loaded %s satellites" % len(satellites))

        catalog = {sat.model.satnum: sat for sat in satellites}
        self.satellite = catalog[satNum]
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

    def getDoppler(self,UL_FREQ,DL_FREQ,updateFiles = False):
        dist = self.satellite - self.gs
        position = dist.at((self.ts).now())
        _, _, _, _, _, satRate = position.frame_latlon_and_rates(self.gs)

        ul_doppler = satRate.m_per_s * UL_FREQ / 299792458
        dl_doppler = - satRate.m_per_s * DL_FREQ / 299792458

        print('UL Doppler: {:.1f} Hz'.format(ul_doppler))
        print('DL Doppler: {:.1f} Hz'.format(dl_doppler))

        UL_FREQ_shifted = UL_FREQ + ul_doppler
        DL_FREQ_shifted = DL_FREQ + dl_doppler

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
        try:
            self.s = serial.Serial(port = "/dev/ttyUSB0", baudrate = 9600, timeout = 1)
            self.s.write(("\r\n\r\n\r\n\r\n\r\n\r\n").encode())
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
            self.s.write(("c2\r\n").encode())
            azel = self.s.readline(1024).decode().strip("\n") 
            az = azel[3:6]
            el = azel[11:]

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


if __name__ == "__main__" :
    gsLat = 52.144176
    gsLon = -106.612910
    ISS = 25544
    
    radsat = rigControl(gsLat,gsLon,ISS)
    radsat.getPassTimes(2023,7,9)

