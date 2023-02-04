from RadsatGsToolkit import *

gen = Generator()
connect = GSConnect()
msg = gen.message

def RxUI():
    while True:
        try:
            print("\nWaiting for message ...")
            sleep(1)
            msgHeader = connect.recv()
            print(msgHeader)
            if msgHeader :
                msgIn = stripHeader(msgHeader)

                msg.ParseFromString(msgIn)
                print("Message:\n",msg)

                msgOut = gen.protocol(True)
                msgHeader = addHeader(msgOut)
                msgXor = xorCipher(msgHeader)
                connect.send(msgXor)
        except Generator.google.protobuf.message.DecodeError:
            print("Decode Error!\n")
            print("Received: ", msgHeader.decode("ascii",errors="backslashreplace"))
            pass

        except KeyboardInterrupt:
            break


if __name__ == "__main__":  
    print("######################## RADSAT Rx UI ########################")
    RxUI()
        
