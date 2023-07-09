from gPredictPassApprover import rotControl,rigControl
from time import sleep

gsLat = 52.144176
gsLon = -106.612910
ISS = 25544
cmdDelay = 3
degToler = 1.5

try:
    rot = rotControl()
    rad = rigControl(gsLat,gsLon,ISS)
    sleep(2)

except Exception as e:
    print(e)
    exit()

while True:
    setAz,setEl = rad.getAzEl()
    getAz,getEl = rot.getPos()

    print("Get: Az=%s / El=%s" % (getAz,getEl))
    print("Set: Az=%s / El=%s" % (setAz,setEl))

    if setEl <= 0:
        setEl = 0

    if (setAz - degToler) <= getAz <= (setAz + degToler) and (setEl - degToler) <= getEl <= (setEl + degToler):
        print("Within tolerance!")

    else:
        print("Adjusting rotator...")
        rot.setPos(setAz,setEl)
    
    sleep(cmdDelay)

    print("\n################################\n")