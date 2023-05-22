import serial
import socket
from time import sleep

# TODO : Impliment Yaesu commanding and integrate with GS

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
        s.listen(1)
    except Exception as e:
        print("Server Error :",e)
        exit()

    return s


if __name__ == "__main__":
    #yaesu = connectToRotator()
    server = makeLocalServer()

    try:

        while True:
            az = "180.00"
            el = "45.00"
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

                    #yaesu.write((DESIRED YAESU COORDS).encode())
                
                elif "p" in recvCommand:
                    #yaesu.write("GET CURRENT DATA")
                    print("Sending: Az = <%s>, El = <%s>" % (az,el))
                    client.send((az + "\n" + el + "\n").encode())
                
                
    except Exception as e:
        print("Encountered exception :",e)
        #yaesu.close()
        server.close()
        assert()
