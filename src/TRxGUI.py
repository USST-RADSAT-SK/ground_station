from RadsatGsToolkit import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal
import sys

genTx = Generator()
genRx = Generator()
msgTx = genTx.message
msgRx = genRx.message

connect = GSConnect()

def append_text(text, dev=False):
    if dev:
        devconsole.append(str(text))
        devconsole.ensureCursorVisible()
    else:
        outconsole.append("-----")
        outconsole.append(str(text))
        outconsole.ensureCursorVisible()

class RX_Thread(QThread):
    rx_signal = pyqtSignal(bytes)

    def __init__(self, parent=None):
        super(RX_Thread, self).__init__(parent)

    def run(self):
        while True:
            try:
                sleep(1)
                msgHeader = connect.recv()

                if msgHeader:
                    msgIn = stripHeader(msgHeader)
                    msgRx.ParseFromString(msgIn)
                    stopTime = time()
                    
                    msgType = genRx.whichType()
                    if msgType == 1:
                        append_text("Received Protocol")
                    if msgType == 2:
                        append_text("Received Telecommand")
                    if msgType == 3:
                        append_text("Received File Transfer")
                    if msgType not in [1,2,3]:
                        append_text("Received Unknown")

                    append_text("Message: " + str(msgRx) + "Time: " + str(stopTime-startTime) + "s")
        
            except Generator.google.protobuf.message.DecodeError:
                append_text("Message: " + str(msgHeader))
            
            self.exit()


def quit_window(app):
    sys.exit(app.exec_())

def get_confirmation():
    global msgOut
    if msgOut == None:
        raise TypeError("Error: Message type cannot be none!!!")
    msgTx.ParseFromString(msgOut)
    append_text("Message: " + str(msgTx), dev=True)
    append_text("Encoded: " + str(msgOut), dev=True)
    append_text("click confirm to send!", dev=True)

def post_confirmation():
    global startTime 
    msgHeader = addHeader(msgOut)
    msgXor = xorCipher(msgHeader)
    connect.send(msgXor)
    startTime = time()
    append_text("Tx message sent!", dev=True)

def onclick_ack():
    global msgOut
    append_text("generating ack...", dev=True)
    append_text("-" * 40, dev=True)
    msgOut = genTx.protocol(True)
    get_confirmation()

def onclick_nack():
    global msgOut
    append_text("generating nack...", dev=True)
    append_text("-" * 40, dev=True)
    msgOut = genTx.protocol(False)
    get_confirmation()

def onclick_beginPass():
    global msgOut
    passLen = int(int_input.text())
    append_text("generating begin pass...", dev=True)
    append_text("pass length: " + str(passLen), dev=True)
    append_text("-" * 40, dev=True)
    msgOut = genTx.beginPass(passLen)
    get_confirmation()

def onclick_beginFTP():
    global msgOut
    append_text("generating begin ftp...", dev=True)
    append_text("-" * 40, dev=True)
    msgOut = genTx.beginFileTransfer()
    get_confirmation()

def onclick_ceaseTransmission():
    global msgOut
    duartion = int(int_input.text())
    append_text("generating cease transmission...", dev=True)
    append_text("duartion: " + str(duartion), dev=True)
    append_text("-" * 40, dev=True)
    msgOut = genTx.ceaseTransmission(duartion)
    get_confirmation()

def onclick_resumeTransmission():
    global msgOut
    append_text("generating resume transmission...", dev=True)
    append_text("-" * 40, dev=True)
    msgOut = genTx.resumeTransmission()
    get_confirmation()

def onclick_unixtime():
    global msgOut
    append_text("setting unixtime...", dev=True)
    append_text("-" * 40, dev=True)
    try:
        unixtime = int(int_input.text())
    except ValueError:
        unixtime = int(time())
    append_text("unixtime: " + str(unixtime), dev=True)

    msgOut = genTx.updateTime(unixtime)
    get_confirmation()

def onclick_reboot():
    global msgOut
    device = device_dropdown.currentIndex()
    reset = reset_dropdown.currentIndex()
    append_text("rebooting...", dev=True)
    append_text("device: " + str(device), dev=True)
    append_text("reset: " + str(reset), dev=True)
    append_text("-" * 40, dev=True)
    msgOut = genTx.reset(device, reset)
    get_confirmation()


##################################################################
#                             GUI
##################################################################
textLabel = ""
global msgOut
msgOut = None

app = QApplication(sys.argv)
win = QMainWindow()
win.setGeometry(1000, 1000, 1500, 1500)
win.setWindowTitle("Telecomm GUI")

layout = QHBoxLayout()
btnlayout = QVBoxLayout()
btnlayout.setSpacing(1)

add_btn = QPushButton("Add")
btnlayout.addWidget(add_btn)
add_btn.clicked.connect(lambda: append_text("hello"))

##################################################################
#                        Ack and Nack 
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
beginftp_btn.clicked.connect(lambda: onclick_beginFTP())

ceasetrans_btn = QPushButton("Cease Transmission")
btnlayout.addWidget(ceasetrans_btn)
ceasetrans_btn.clicked.connect(lambda: onclick_ceaseTransmission())

resumetrans_btn = QPushButton("Resume Transmission")
btnlayout.addWidget(resumetrans_btn)
resumetrans_btn.clicked.connect(lambda: onclick_resumeTransmission())

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

other_label = QLabel("Others")
other_label.setContentsMargins(0, 0, 0, 0)
btnlayout.addWidget(other_label)
other_label.show()

confirm_btn = QPushButton("Confirm")
btnlayout.addWidget(confirm_btn)
confirm_btn.clicked.connect(lambda: post_confirmation())

quit_btn = QPushButton("Quit")
btnlayout.addWidget(quit_btn)
quit_btn.clicked.connect(lambda: quit_window(app))

outconsole = QTextEdit()
outconsole.setReadOnly(True)
outconsole.append(textLabel)
outconsole.ensureCursorVisible()

devconsole = QTextEdit()
devconsole.setReadOnly(True)
devconsole.append("Dev Console")
devconsole.ensureCursorVisible()

layout.addLayout(btnlayout)
layout.addWidget(devconsole)
layout.addWidget(outconsole)

central_widget = QWidget()
central_widget.setLayout(layout)
win.setCentralWidget(central_widget)
win.move(0,0)

##################################################################
#                         Threads
##################################################################

thread = RX_Thread()
thread.start()
thread.rx_signal.connect(append_text)

win.show()
sys.exit(app.exec_())