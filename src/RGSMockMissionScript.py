from RadsatGsToolkit import *
gen = Generator()
msg = gen.message


print("######################## RADSAT GS Message UI ########################\n")

while True:
    msgOut = None
    print("Send Commands:\n1) Ack\n2) Nack\n3) Telecommand\nq) Quit")
    choice = input(">> ")

    if choice.lower() == "q":
        print("Exiting...")
        break

    elif choice == "1":
        print("Sending Ack...\n")
        msgOut = gen.protocol(True)
    
    elif choice == "2":
        print("Sending Nack...\n")
        msgOut = gen.protocol(False)

    elif choice == "3":
        print("Select Telecommand:\n1) beginPass\n2) beginFileTransfer\n3) ceaseTransmission\n4) resumeTransmission\n5) updateTime\n6) reset\nb) Back")
        choice = input(">> ")

        if choice == "1":
            passLength = int(input("passLength = "))
            print("Sending beginPass...\n")
            msgOut = gen.beginPass(passLength)

        elif choice == "2":
            print("Sending beginFileTransfer...\n")
            msgOut = gen.beginFileTransfer()

        elif choice == "3":
            duration = int(input("duration = "))
            print("Sending ceaseTransmission...\n")
            msgOut = gen.ceaseTransmission(duration)

        elif choice == "4":
            print("Sending resumeTransmission...\n")
            msgOut = gen.resumeTransmission()

        elif choice == "5":
            choice = input("Manual time entry? (Y/N)")
            if choice.lower() == "Y":
                unixTime = int(input("unixTime = "))
            else:
                unixTime = int(time())
            print("Sending updateTime...\n")
            msgOut = gen.updateTime(unixTime)        

        elif choice == "6":
            device = int(input("0) OBC\n1) Transmitter\n2) Receiver\n3) AntennaSideA\n4) AntennaSideB\n>> "))
            hard = int(input("0) Soft reboot\n1) Hard obc reboot\n>> "))
            print("Sending reset...\n")
            msgOut = gen.reset(device, hard)    
    
    if msgOut != None:
        msg.ParseFromString(msgOut)            
        print("Message:\n",msg)
        print("Encoded:\n",msgOut)
        #send(mesgOut) TODO   
    
    else:
        print("Invalid input. Please try again!")
        pass
    

    
