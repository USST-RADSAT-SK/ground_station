import zmq
from time import sleep
import pmt
from numpy import array, uint8

class GSConnect:
    def __init__(self, addr="127.0.0.1", sendPort=15530, recvPort=15531):
        self.addr = addr
        self.sendPort = sendPort
        self.recvPort = recvPort

        pubContext = zmq.Context()
        self.pubSock = pubContext.socket(zmq.PUB)
        self.pubSock.connect(f"tcp://{addr}:{sendPort}")

        pullContext = zmq.Context()
        self.pullSock = pullContext.socket(zmq.PULL)
        self.pullSock.connect(f"tcp://{addr}:{recvPort}")

    def send(self, data):
        try:
            if isinstance(data, str):
                bytesData = pmt.to_pmt(array(bytearray(data, "ascii"), dtype=uint8))
            else:
                bytesData = pmt.to_pmt(array(bytearray(data), dtype=uint8))
        except Exception as e:
            raise e
        self.pubSock.send(pmt.serialize_str(bytesData))

    def recv(self):
        num = self.pullSock.poll(10)
        if num != 0:
            data = bytearray(pmt.to_python(pmt.deserialize_str(self.pullSock.recv()))
            return data
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
            connection.send(msg)
            
            #connection.send(bytes(msg, "ascii"))

