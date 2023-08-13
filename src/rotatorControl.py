from RadsatGsToolkit import *
from time import sleep
from os import path,remove
import sys

gsLat = 52.144176
gsLon = -106.612910

try:
    ISS = int(sys.argv[1])

except IndexError:
    ISS = 25544

cmdDelay = 3
degToler = 1.5

if path.isfile("active.txt"):
    remove("active.txt")

try:
    rot = rotControl()
    rad = rigControl(gsLat,gsLon,ISS)
    sleep(2)

except Exception as e:
    print(e)
    exit()

while True:
    loopNum = 0
    try:
        sleep(cmdDelay)
        print("\n################################\n")
        
        if loopNum == 50:
            rad.updateTles()
            loopNum = 0
        loopNum += 1

        setAz,setEl = rad.getAzEl()
        getAz,getEl = rot.getPos()

        print("Get: Az=%s / El=%s" % (getAz,getEl))
        print("Set: Az=%s / El=%s" % (setAz,setEl))

        if -10 <= setEl < 0:
            rot.setPos(setAz,0)

        elif setEl < -10:
            continue

        else:
            if (setAz - degToler) <= getAz <= (setAz + degToler) and (setEl - degToler) <= getEl <= (setEl + degToler):
                print("Within tolerance!")

            else:
                print("Adjusting rotator...")
                rot.setPos(setAz,setEl)

    except Exception as e:
        print(e)
        rot.close()
        exit()