import zmq
from time import sleep
import pmt

class GSConnect:
    def __init__(self, addr="127.0.0.1", sendPort=15530, recvPort=15531):
        self.addr = addr
        self.sendPort = sendPort
        self.recvPort = recvPort

        pubContext = zmq.Context()
        self.pubSock = pubContext.socket(zmq.PUB)
        self.pubSock.connect(f"tcp://{addr}:{sendPort}")

        """
        subContext = zmq.Context()
        self.subSock = subContext.socket(zmq.SUB)
        self.subSock.setsockopt(zmq.SUBSCRIBE, b"")
        self.subSock.bind(f"tcp://{addr}:{recvPort}")
        """

        pullContext = zmq.Context()
        self.pullSock = pullContext.socket(zmq.PULL)
        self.pullSock.connect(f"tcp://{addr}:{recvPort}")

    def send(self, data):
        bytesData = bytes(data)
        sizeof = len(bytesData)
        dataSerial = bytes((0x02,(sizeof >> 8) & 0xff, sizeof & 0xff)) + bytesData
        #dataSerial = pmt.serialize_str(pmt.intern(data))
        self.pubSock.send(dataSerial)

    def recv(self):
        num = self.pullSock.poll(10)
        if num != 0:
            return self.pullSock.recv()
        return
        """
        return self.subSock.recv()
        if socket.poll(10) != 0:
            return subSock.recv()
        return
        """


if __name__ == "__main__":
    connection = GSConnect()
    while 1:
        try:
            result = connection.recv()
            if result:
                print(result)
        except KeyboardInterrupt as e:
            msg = input("\rEnter Message > ")
            connection.send(bytes(msg, "ascii"))

