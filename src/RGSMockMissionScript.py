from RadsatGsToolkit import *

gen = Generator()
connect = GSConnect()
msg = gen.message

def TxUI():
    while True:
        msgOut = None
        print("\nSend Commands:\n1) Ack\n2) Nack\n3) Telecommand\nq) Quit")
        choice = input(">> ")

        if choice.lower() == "q":
            print("Exiting...")
            break

        elif choice == "1":
            print("Generating Ack...\n")
            msgOut = gen.protocol(True)
        
        elif choice == "2":
            print("Generating Nack...\n")
            msgOut = gen.protocol(False)

        elif choice == "3":
            print("\nSelect Telecommand:\n1) beginPass\n2) beginFileTransfer\n3) ceaseTransmission\n4) resumeTransmission\n5) updateTime\n6) reset\nb) Back")
            choice = input(">> ")

            if choice == "1":
                    passLength = int(input("passLength = "))
                    print("Generating beginPass...\n")
                    msgOut = gen.beginPass(passLength)

            elif choice == "2":
                    print("Generating beginFileTransfer...\n")
                    msgOut = gen.beginFileTransfer()

            elif choice == "3":
                    duration = int(input("duration = "))
                    print("Generating ceaseTransmission...\n")
                    msgOut = gen.ceaseTransmission(duration)

            elif choice == "4":
                    print("Generating resumeTransmission...\n")
                    msgOut = gen.resumeTransmission()

            elif choice == "5":
                choice = input("Manual time entry? (Y/N)")
                if choice.lower() == "Y":
                    unixTime = int(input("unixTime = "))
                else:
                    unixTime = int(time())
                    print("Generating updateTime...\n")
                    msgOut = gen.updateTime(unixTime)                

            elif choice == "6":
                device = int(input("0) OBC\n1) Transmitter\n2) Receiver\n3) AntennaSideA\n4) AntennaSideB\n>> "))
                hard = int(input("0) Soft reboot\n1) Hard obc reboot\n>> "))
                print("Generating reset...\n")
                msgOut = gen.reset(device, hard)        
        
        if msgOut != None:
                msg.ParseFromString(msgOut)                        
                print("Message:\n",msg)
                print("Encoded:\n",msgOut)
                confirm = input("\nSend? (Y/N)\n>> ")
                if confirm.lower() == "y":
                    msgHeader = addHeader(msgOut)
                    msgXor = xorCipher(msgHeader)
                    # TODO add ax25 + other message formatting...? 
                    connect.send(msgXor)
                    print("Sent!")
                else:
                     print("Not sending!")
        
        else:
            print("Invalid input. Please try again!")
            pass

def RxUI():
    while True:
        try:
            print("\nWaiting for message ...")
            msgHeader = connect.recv()
            if result:
                # TODO remove ax25 + other message formatting...? 
                msgIn = stripHeader(msgHeader)
                msg.ParseFromString(msgIn)
                print("Message:\n",msg)

                msgOut = gen.protocol(True)
                msgHeader = addHeader(msgOut)
                msgXor = xorCipher(msgHeader)
                # TODO add ax25 + other message formatting...? 
                connect.send(msgXor)
        except:
            msgOut = gen.protocol(False)
            msgHeader = addHeader(msgOut)
            msgXor = xorCipher(msgHeader)
            # TODO add ax25 + other message formatting...?                 connect.send(msgXor)

if __name__ == "__main__":  
    print("######################## RADSAT GS Message UI ########################")
    TxUI()
    #RxUI() TODO test RxUI with OBC sending messages
        
