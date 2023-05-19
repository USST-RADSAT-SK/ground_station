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
        s.listen(1)
    except Exception as e:
        print("Server Error :",e)
        exit()

    return s


if __name__ == "__main__":
    yaesu = connectToRotator()
    server = makeLocalServer()

    try:
        while True:
            client,address = server.accept()
            print(client)
            print(address)
            while True:
                client.send(("l\n").encode())
                print("<%s>" % client.recv(1024).decode())
                sleep(0.5)

    except Exception as e:
        print("Encountered exception :",e)
        yaesu.close()
        server.close()
        assert()
