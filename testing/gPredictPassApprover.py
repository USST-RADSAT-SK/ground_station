import serial
import socket
from time import sleep

def connectToRotator():
    try:
        s = serial.Serial(port = "/dev/ttyUSB0", baudrate = 9600, timeout = 1)
        s.write(("r\r\n").encode())
        sleep(1)
        s.write(("l\r\n").encode())
        sleep(1)
        s.write(("s\r\n").encode())
        print("Connection succesful")
    except Exception as e:
        print("Rotator Error :",e)
        exit()
    return s

def makeLocalServer():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(("localhost",4533))
        print("Server created. Listening for connections...")
        s.listen()
    except Exception as e:
        print("Server Error :",e)
        exit()

    return s


if __name__ == "__main__":
    yaesu = connectToRotator()
    server = makeLocalServer()

    try:

        while True:
            az = "180.00"
            el = "45.00"
            yaz = "180"
            yel = "045"

            client,address = server.accept()
            print(client)
            print(address)
            
            while True:
                recvCommand = client.recv(512).decode().strip("\n")
                print("Got : <%s>" % recvCommand)

                if "S" in recvCommand:
                    client.send(("\n").encode())
                    x = 1/0 

                elif "P" in recvCommand:
                    coords = recvCommand.split(" ")
                    az = (coords[1]).strip()
                    el = (coords[2]).strip()

                    print("Requested Az = <%s>, El = <%s>" % (az,el))
                    client.send(("RPRT 0\n").encode())

                    yaesu.write(("W" + f'{int(float(az)):03}' + " " + f'{int(float(el)):03}' + "\n").encode("ascii"))
                
                elif "p" in recvCommand:
                    yaesu.write(("c2\r\n").encode("ascii"))
                    azel = yaesu.readline(512).decode("ascii").strip("\n")
                    print("Yaesu :",azel)
                    if azel[3:6] != "" or azel[11:] != "":
                        yaz = azel[3:6]
                        yel = azel[11:]
                    print("Sending: Az = <%s>, El = <%s>" % (yaz,yel))
                    client.send((yaz + "\n" + yel + "\n").encode())
                
                yaesu.write(("\r\n").encode("ascii"))

    except Exception as e:
        print("Encountered exception :",e)
        yaesu.close()
        server.close()
        assert()
