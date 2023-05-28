import serial
import socket

def connectToRotator():
    try:
        s = serial.Serial(port = "/dev/ttyUSB0", baudrate = 9600, timeout = 1)
        s.write(("\r\n\r\n\r\n\r\n\r\n\r\n").encode())
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
            # Initial values to init with before getting real ones
            az = "180.00"
            el = "45.00"
            yaz = "180"
            yel = "045"

            # Number of posotion requests from Gpredict to avoid overwhelming yaesu buffer
            nReq = 0

            client,address = server.accept()
            
            while True:
                recvCommand = client.recv(1024).decode().strip("\n")
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

                    yaesu.write(("W" + f'{int(float(az)):03}' + " " + f'{int(float(el)):03}' + "\r\n").encode())
                    yaesu.readline(1024)

                elif "p" in recvCommand:
                    if nReq == 0:
                        nReq = 10
                        yaesu.write(("c2\r\n").encode())
                        azel = yaesu.readline(1024).decode().strip("\n")                    
                        if "?>" in azel:
                            yaesu.write(("c2\r\n").encode())
                            azel = yaesu.readline(1024).decode().strip("\n")
                        
                            print("Yaesu :",azel)

                        if azel[3:6] != "" or azel[11:] != "":
                            yaz = azel[3:6]
                            yel = azel[11:]

                        print("Sending: Az = <%s>, El = <%s>" % (yaz,yel))

                    nReq = nReq-1

                    client.send((yaz + "\n" + yel + "\n").encode())
                

    except Exception as e:
        print("Encountered exception :",e)
        yaesu.close()
        server.close()
        exit()