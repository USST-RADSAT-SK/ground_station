from RadsatGsToolkit import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal
import sys

connect = GSConnect()

obcTelem = ObcTelemetry()
trxvuTelem = TransceiverTelemetry()
cameraTelem = CameraTelemetry()
epsTelem = EpsTelemetry()
batteryTelem = BatteryTelemetry()
antennaTelem = AntennaTelemetry()
dosimeterData = DosimeterData()
imgPacket = ImagePacket()
modError = ModuleErrorReport()
compError = ComponentErrorReport()
errSummary = ErrorReportSummary()
ack = Ack()
nack = Nack()
beginPass = BeginPass()
beginFileTransfer = BeginFileTransfer()
ceaseTransmission = CeaseTransmission()
updateTime = UpdateTime()
rst = Reset()

ftMode = False
startTime = 0
FT = False

def append_text(text, dev=False, timeStamp = False):
    stamp = ""
    if timeStamp:
        stamp = getDateString(time=True) + " : "
    
    if dev:
        devconsole.append(stamp + str(text))
        devconsole.ensureCursorVisible()
    else:
        outconsole.append(stamp + str(text))
        outconsole.ensureCursorVisible()

def printRxMessage(msgIn):
    msg,preamble,checkSum,length,timeStamp = stripHeader(msgIn)
    try:
        msgObj = generator(msg)
        append_text("From : RADSAT-SK")
        append_text("Message Time : " + getDateString(time=True))
        append_text("Raw : " + str(msg))
        append_text("CRC : " + str(checkSum))
        append_text("Size : " + str(length))
        append_text("Time Stamp : " + str(timeStamp))
        append_text("Msg Type : " + str(msgObj.ID))
        append_text("Message : " + str(msgObj))
        append_text("")

        sendToFile("rawDataLogger\RADSAT-" + getDateString() + ".csv",msgObj,preamble,checkSum,length,timeStamp)

    except Exception as e:
        append_text("")
        append_text("Decode Error : " + str(msgIn),dev=True,timeStamp=True)
        append_text("Error Print : " + str(e),dev=True)
        append_text("",dev=True)
    
class RX_Thread(QThread):
    rx_signal = pyqtSignal(bytes)

    def __init__(self, parent=None):
        super(RX_Thread, self).__init__(parent)

    def run(self):
        global ftMode,startTime
        while True:
            try:
                msgHeader = connect.recv()

                if not ftMode:
                    if msgHeader != None:
                        msg,_,_,_,_ = stripHeader(msgHeader)
                        printRxMessage(msgHeader)

                else:
                    if msgHeader != None:
                        msg,_,_,_,_ = stripHeader(msgHeader)
                        if isinstance(generator(msg), Nack):
                            ftMode = False
                            append_text("Nack received. Disabling FT mode!", dev=True)

                        else:
                            printRxMessage(msgHeader)
                            
                            ack.resp = 0
                            append_text("FT Received! Sending Ack", dev=True,timeStamp=True)
                            connect.send(xorCipher(addHeader(ack.encoder())))
                            startTime = time()
                            
                    else:
                        if time() - startTime > 5:
                            append_text("No FT received in > 5s. Sending Ack!",dev=True,timeStamp=True)
                            connect.send(xorCipher(addHeader(ack.encoder())))
                            startTime = time()
                        sleep(0.001)
            
            except Exception as e:
                append_text("Receive Error: " + str(e), dev=True,timeStamp=True)
            
            self.exit()


def quit_window(app):
    sys.exit(app.exec_())

def get_confirmation(msgOut):
    global confirmMessage
    if msgOut == None:
        raise TypeError("Error: Message type cannot be none!!!")
    append_text("Message: " + str(generator(msgOut)), dev=True)
    append_text("Encoded: " + str(msgOut.hex()), dev=True)
    append_text("click confirm to send!", dev=True)
    append_text("",dev=True)
    confirmMessage = msgOut

def post_confirmation(toSend):
    msgHeader = addHeader(toSend)
    msg,preamble,checkSum,length,timeStamp = stripHeader(msgHeader)
    msgXor = xorCipher(msgHeader)
    msgObj = generator(msg)
    append_text("Message sent!",dev=True,timeStamp=True)
    append_text("From : Ground Station")
    append_text("Message Time : " + getDateString(time=True))
    append_text("Raw : " + str(msg))
    append_text("CRC : " + str(checkSum))
    append_text("Size : " + str(length))
    append_text("Time Stamp : " + str(timeStamp))
    append_text("Msg Type : " + str(msgObj.ID))
    append_text("Message : " + str(msgObj))
    append_text("")
    connect.send(msgXor)
    sendToFile("rawDataLogger\RADSAT-" + getDateString() + ".csv",msgObj,preamble,checkSum,length,timeStamp)

    if isinstance(msgObj, BeginFileTransfer):
        global ftMode,startTime
        ftMode = True
        startTime = time()

def onclick_ack():
    append_text("Generating Ack...", dev=True,timeStamp=True)
    ack.resp = 0
    msgOut = ack.encoder()
    get_confirmation(msgOut)

def onclick_nack():
    append_text("Generating Nack...", dev=True,timeStamp=True)
    nack.resp = 0
    msgOut = nack.encoder()
    get_confirmation(msgOut)

def onclick_beginPass():
    append_text("Generating BeginPass...", dev=True,timeStamp=True)
    try:
        passLen = int(int_input.text())
    except ValueError:
        passLen = 0
    append_text("pass length: " + str(passLen), dev=True)
    beginPass.passLength = passLen
    msgOut = beginPass.encoder()
    get_confirmation(msgOut)

def onclick_beginFileTransfer():
    append_text("Generating BeginFileTransfer...", dev=True,timeStamp=True)
    beginFileTransfer.resp = 1
    msgOut = beginFileTransfer.encoder()
    get_confirmation(msgOut)

def onclick_ceaseTransmission():
    append_text("Generating CeaseTransmission...", dev=True,timeStamp=True)
    try:
        duration = int(int_input.text())
    except ValueError:
        duration = 0
    append_text("duration: " + str(duration), dev=True)
    ceaseTransmission.duration = duration
    msgOut = ceaseTransmission.encoder()    
    get_confirmation(msgOut)

def onclick_unixtime():
    append_text("Generating SetUnixtime...", dev=True,timeStamp=True)
    try:
        unixtime = int(int_input.text())
    except ValueError:
        unixtime = int(time())
    append_text("unixtime: " + str(unixtime), dev=True)
    updateTime.unixTime = unixtime
    msgOut = updateTime.encoder()
    get_confirmation(msgOut)

def onclick_reboot():
    device = device_dropdown.currentIndex()
    reset = reset_dropdown.currentIndex()
    append_text("Generating Reset...", dev=True,timeStamp=True)
    append_text("device: " + str(device), dev=True)
    append_text("reset: " + str(reset), dev=True)
    rst.device = device
    rst.hard = reset
    msgOut = rst.encoder()
    get_confirmation(msgOut)

def onclick_restartFileTransfer():
    global ftMode
    ftMode = False
    append_text("FT mode reset",dev=True,timeStamp=True)

##################################################################
#                             GUI
##################################################################
msgOut = None

app = QApplication(sys.argv)
win = QMainWindow()
win.setGeometry(1000, 1000, 1500, 1500)
win.setWindowTitle("RADSAT-SK - Ground Station GUI")

layout = QHBoxLayout()
btnlayout = QVBoxLayout()
btnlayout.setSpacing(1)


##################################################################
#                           Protocol
##################################################################

sendcmd_label = QLabel("Send Command")
sendcmd_label.setContentsMargins(0, 0, 0, 0)
btnlayout.addWidget(sendcmd_label)
sendcmd_label.show()

ack_btn = QPushButton("Ack")
btnlayout.addWidget(ack_btn)
ack_btn.clicked.connect(lambda: onclick_ack())

nack_btn = QPushButton("Nack")
btnlayout.addWidget(nack_btn)
nack_btn.clicked.connect(lambda: onclick_nack())


##################################################################
#                         Telecommands
##################################################################

telecmd_label = QLabel("Telecommands")
telecmd_label.setContentsMargins(0, 0, 0, 0)
btnlayout.addWidget(telecmd_label)
telecmd_label.show()

passlen_label = QLabel("Input")
passlen_label.setContentsMargins(0, 0, 0, 0)
btnlayout.addWidget(passlen_label)
passlen_label.show()

int_input = QLineEdit()
int_input.setPlaceholderText("Enter integer...")
btnlayout.addWidget(int_input)
int_input.show()

beginPass_btn = QPushButton("Begin Pass")
btnlayout.addWidget(beginPass_btn)
beginPass_btn.clicked.connect(lambda: onclick_beginPass())

beginftp_btn = QPushButton("Begin File Transfer")
btnlayout.addWidget(beginftp_btn)
beginftp_btn.clicked.connect(lambda: onclick_beginFileTransfer())

ceasetrans_btn = QPushButton("Cease Transmission")
btnlayout.addWidget(ceasetrans_btn)
ceasetrans_btn.clicked.connect(lambda: onclick_ceaseTransmission())

unixtime_btn = QPushButton("Set Unixtime")
btnlayout.addWidget(unixtime_btn)
unixtime_btn.clicked.connect(lambda: onclick_unixtime())


##################################################################
#                         Reboot
##################################################################

device_dropdown = QComboBox()
device_dropdown.addItem("OBC", 0)
device_dropdown.addItem("Transmitter", 1)
device_dropdown.addItem("Receiver", 2)
device_dropdown.addItem("AntennaSideA", 3)
device_dropdown.addItem("AntennaSideB", 4)
btnlayout.addWidget(device_dropdown)

reset_dropdown = QComboBox()
reset_dropdown.addItem("Soft Reboot", 0)
reset_dropdown.addItem("Hard OBC Reboot", 1)
btnlayout.addWidget(reset_dropdown)

reboot_btn = QPushButton("Reboot")
btnlayout.addWidget(reboot_btn)
reboot_btn.clicked.connect(lambda: onclick_reboot())


##################################################################
#                         Others
##################################################################

confirmMessage = None

other_label = QLabel("Others")
other_label.setContentsMargins(0, 0, 0, 0)
btnlayout.addWidget(other_label)
other_label.show()

confirm_btn = QPushButton("Confirm")
btnlayout.addWidget(confirm_btn)
confirm_btn.clicked.connect(lambda: post_confirmation(confirmMessage))

rstFt_btn = QPushButton("Reset FT Mode")
btnlayout.addWidget(rstFt_btn)
rstFt_btn.clicked.connect(lambda: onclick_restartFileTransfer())

quit_btn = QPushButton("Quit")
btnlayout.addWidget(quit_btn)
quit_btn.clicked.connect(lambda: quit_window(app))

outconsole = QTextEdit()
outconsole.setReadOnly(True)
outconsole.append("------------------------ Message Thread ------------------------")
outconsole.ensureCursorVisible()

devconsole = QTextEdit()
devconsole.setReadOnly(True)
devconsole.append("---------------------- Debug/Error Thread ----------------------")
devconsole.ensureCursorVisible()

layout.addLayout(btnlayout)
layout.addWidget(devconsole)
layout.addWidget(outconsole)

central_widget = QWidget()
central_widget.setLayout(layout)
win.setCentralWidget(central_widget)
win.move(0,0)
win.resize(940,450)


##################################################################
#                         Threads
##################################################################

thread = RX_Thread()
thread.start()
thread.rx_signal.connect(append_text)

win.show()
sys.exit(app.exec_())