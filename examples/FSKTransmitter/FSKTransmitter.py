#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK Transmitter
# Author: austin
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import math, os

from gnuradio import qtgui

class FSKTransmitter(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FSK Transmitter")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FSK Transmitter")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "FSKTransmitter")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samplesPerSymbol = samplesPerSymbol = int(32*4)
        self.baudRate = baudRate = 9600
        self.testFiles = testFiles = "/home/austin/Desktop/ground_station/examples/SampleBinaryFiles/"
        self.sampleRate = sampleRate = baudRate * samplesPerSymbol
        self.radioGain = radioGain = 0
        self.manualModulation = manualModulation = 0
        self.manualMode = manualMode = 1
        self.invertBits = invertBits = 1
        self.frequencyError = frequencyError = 100
        self.frequencyDeviation = frequencyDeviation = 4800
        self.fileName = fileName = "random_32B.bin"
        self.carrierFrequency = carrierFrequency = 915e6

        ##################################################
        # Blocks
        ##################################################
        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'Tx')
        self.tabs_widget_1 = Qt.QWidget()
        self.tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_1)
        self.tabs_grid_layout_1 = Qt.QGridLayout()
        self.tabs_layout_1.addLayout(self.tabs_grid_layout_1)
        self.tabs.addTab(self.tabs_widget_1, 'FSK Mod')
        self.top_grid_layout.addWidget(self.tabs, 10, 0, 1, 4)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._manualModulation_range = Range(-1, 1, 0.05, 0, 200)
        self._manualModulation_win = RangeWidget(self._manualModulation_range, self.set_manualModulation, ' ', "counter_slider", float)
        self.top_grid_layout.addWidget(self._manualModulation_win, 2, 1, 1, 3)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        _manualMode_check_box = Qt.QCheckBox('Manual Mode')
        self._manualMode_choices = {True: 0, False: 1}
        self._manualMode_choices_inv = dict((v,k) for k,v in self._manualMode_choices.items())
        self._manualMode_callback = lambda i: Qt.QMetaObject.invokeMethod(_manualMode_check_box, "setChecked", Qt.Q_ARG("bool", self._manualMode_choices_inv[i]))
        self._manualMode_callback(self.manualMode)
        _manualMode_check_box.stateChanged.connect(lambda i: self.set_manualMode(self._manualMode_choices[bool(i)]))
        self.top_grid_layout.addWidget(_manualMode_check_box, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        _invertBits_check_box = Qt.QCheckBox('Invert Bits')
        self._invertBits_choices = {True: -1, False: 1}
        self._invertBits_choices_inv = dict((v,k) for k,v in self._invertBits_choices.items())
        self._invertBits_callback = lambda i: Qt.QMetaObject.invokeMethod(_invertBits_check_box, "setChecked", Qt.Q_ARG("bool", self._invertBits_choices_inv[i]))
        self._invertBits_callback(self.invertBits)
        _invertBits_check_box.stateChanged.connect(lambda i: self.set_invertBits(self._invertBits_choices[bool(i)]))
        self.top_grid_layout.addWidget(_invertBits_check_box, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._fileName_options = ("1s_32B.bin", "0s_32B.bin", "50p_duty_32B.bin", "pyramid_32B.bin", "random_32B.bin", )
        # Create the labels list
        self._fileName_labels = ('All 1s', 'All 0s', '50% Duty', 'In/Decressing', 'Random', )
        # Create the combo box
        self._fileName_tool_bar = Qt.QToolBar(self)
        self._fileName_tool_bar.addWidget(Qt.QLabel('Transmit' + ": "))
        self._fileName_combo_box = Qt.QComboBox()
        self._fileName_tool_bar.addWidget(self._fileName_combo_box)
        for _label in self._fileName_labels: self._fileName_combo_box.addItem(_label)
        self._fileName_callback = lambda i: Qt.QMetaObject.invokeMethod(self._fileName_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._fileName_options.index(i)))
        self._fileName_callback(self.fileName)
        self._fileName_combo_box.currentIndexChanged.connect(
            lambda i: self.set_fileName(self._fileName_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._fileName_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.stretchTransform = blocks.multiply_const_ff(2 * invertBits)
        self.shiftTransform = blocks.add_const_ff(-1 * invertBits)
        self.repeatToSymbolLength = blocks.repeat(gr.sizeof_float*1, samplesPerSymbol)
        self._radioGain_range = Range(0, 60, 0.1, 0, 200)
        self._radioGain_win = RangeWidget(self._radioGain_range, self.set_radioGain, 'Radio Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._radioGain_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.manualSource = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, manualModulation)
        self.iqTimeOutput = qtgui.time_sink_c(
            1024 * 2, #size
            sampleRate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.iqTimeOutput.set_update_time(0.10)
        self.iqTimeOutput.set_y_axis(-1.2, 1.2)

        self.iqTimeOutput.set_y_label('Amplitude', "")

        self.iqTimeOutput.enable_tags(True)
        self.iqTimeOutput.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.iqTimeOutput.enable_autoscale(False)
        self.iqTimeOutput.enable_grid(True)
        self.iqTimeOutput.enable_axis_labels(True)
        self.iqTimeOutput.enable_control_panel(True)
        self.iqTimeOutput.enable_stem_plot(True)


        labels = ['Tx Binary', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [8, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.iqTimeOutput.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.iqTimeOutput.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.iqTimeOutput.set_line_label(i, labels[i])
            self.iqTimeOutput.set_line_width(i, widths[i])
            self.iqTimeOutput.set_line_color(i, colors[i])
            self.iqTimeOutput.set_line_style(i, styles[i])
            self.iqTimeOutput.set_line_marker(i, markers[i])
            self.iqTimeOutput.set_line_alpha(i, alphas[i])

        self._iqTimeOutput_win = sip.wrapinstance(self.iqTimeOutput.pyqwidget(), Qt.QWidget)
        self.tabs_grid_layout_0.addWidget(self._iqTimeOutput_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.iqOutput = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_HAMMING, #wintype
            0, #fc
            sampleRate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.iqOutput.set_update_time(1.0/10)
        self._iqOutput_win = sip.wrapinstance(self.iqOutput.pyqwidget(), Qt.QWidget)

        self.iqOutput.enable_rf_freq(False)

        self.tabs_grid_layout_0.addWidget(self._iqOutput_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.frequencyModulator = analog.frequency_modulator_fc(2* math.pi * (baudRate / sampleRate))
        self.fileSource = blocks.file_source(gr.sizeof_char*1, testFiles + fileName, True, 0, 0)
        self.fileSource.set_begin_tag(pmt.PMT_NIL)
        self.convertToBinary = blocks.unpack_k_bits_bb(8)
        self.charToFloat = blocks.char_to_float(1, 1)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,manualMode,0)
        self.blocks_selector_0.set_enabled(True)
        self.binDisplay = qtgui.time_sink_f(
            32*8*2, #size
            baudRate, #samp_rate
            "Binary Transmittion", #name
            1 #number of inputs
        )
        self.binDisplay.set_update_time(1/30)
        self.binDisplay.set_y_axis(-0.1, 1.1)

        self.binDisplay.set_y_label('', "")

        self.binDisplay.enable_tags(False)
        self.binDisplay.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.binDisplay.enable_autoscale(False)
        self.binDisplay.enable_grid(True)
        self.binDisplay.enable_axis_labels(False)
        self.binDisplay.enable_control_panel(False)
        self.binDisplay.enable_stem_plot(True)

        self.binDisplay.disable_legend()

        labels = ['Tx Binary', 'TX Binary', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['red', 'blue', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.binDisplay.set_line_label(i, "Data {0}".format(i))
            else:
                self.binDisplay.set_line_label(i, labels[i])
            self.binDisplay.set_line_width(i, widths[i])
            self.binDisplay.set_line_color(i, colors[i])
            self.binDisplay.set_line_style(i, styles[i])
            self.binDisplay.set_line_marker(i, markers[i])
            self.binDisplay.set_line_alpha(i, alphas[i])

        self._binDisplay_win = sip.wrapinstance(self.binDisplay.pyqwidget(), Qt.QWidget)
        self.tabs_grid_layout_1.addWidget(self._binDisplay_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_1.setColumnStretch(c, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_selector_0, 0), (self.frequencyModulator, 0))
        self.connect((self.charToFloat, 0), (self.binDisplay, 0))
        self.connect((self.charToFloat, 0), (self.stretchTransform, 0))
        self.connect((self.convertToBinary, 0), (self.charToFloat, 0))
        self.connect((self.fileSource, 0), (self.convertToBinary, 0))
        self.connect((self.frequencyModulator, 0), (self.iqOutput, 0))
        self.connect((self.frequencyModulator, 0), (self.iqTimeOutput, 0))
        self.connect((self.manualSource, 0), (self.blocks_selector_0, 0))
        self.connect((self.repeatToSymbolLength, 0), (self.blocks_selector_0, 1))
        self.connect((self.shiftTransform, 0), (self.repeatToSymbolLength, 0))
        self.connect((self.stretchTransform, 0), (self.shiftTransform, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FSKTransmitter")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samplesPerSymbol(self):
        return self.samplesPerSymbol

    def set_samplesPerSymbol(self, samplesPerSymbol):
        self.samplesPerSymbol = samplesPerSymbol
        self.set_sampleRate(self.baudRate * self.samplesPerSymbol)
        self.repeatToSymbolLength.set_interpolation(self.samplesPerSymbol)

    def get_baudRate(self):
        return self.baudRate

    def set_baudRate(self, baudRate):
        self.baudRate = baudRate
        self.set_sampleRate(self.baudRate * self.samplesPerSymbol)
        self.binDisplay.set_samp_rate(self.baudRate)
        self.frequencyModulator.set_sensitivity(2* math.pi * (self.baudRate / self.sampleRate))

    def get_testFiles(self):
        return self.testFiles

    def set_testFiles(self, testFiles):
        self.testFiles = testFiles
        self.fileSource.open(self.testFiles + self.fileName, True)

    def get_sampleRate(self):
        return self.sampleRate

    def set_sampleRate(self, sampleRate):
        self.sampleRate = sampleRate
        self.frequencyModulator.set_sensitivity(2* math.pi * (self.baudRate / self.sampleRate))
        self.iqOutput.set_frequency_range(0, self.sampleRate)
        self.iqTimeOutput.set_samp_rate(self.sampleRate)

    def get_radioGain(self):
        return self.radioGain

    def set_radioGain(self, radioGain):
        self.radioGain = radioGain

    def get_manualModulation(self):
        return self.manualModulation

    def set_manualModulation(self, manualModulation):
        self.manualModulation = manualModulation
        self.manualSource.set_offset(self.manualModulation)

    def get_manualMode(self):
        return self.manualMode

    def set_manualMode(self, manualMode):
        self.manualMode = manualMode
        self._manualMode_callback(self.manualMode)
        self.blocks_selector_0.set_input_index(self.manualMode)

    def get_invertBits(self):
        return self.invertBits

    def set_invertBits(self, invertBits):
        self.invertBits = invertBits
        self._invertBits_callback(self.invertBits)
        self.shiftTransform.set_k(-1 * self.invertBits)
        self.stretchTransform.set_k(2 * self.invertBits)

    def get_frequencyError(self):
        return self.frequencyError

    def set_frequencyError(self, frequencyError):
        self.frequencyError = frequencyError

    def get_frequencyDeviation(self):
        return self.frequencyDeviation

    def set_frequencyDeviation(self, frequencyDeviation):
        self.frequencyDeviation = frequencyDeviation

    def get_fileName(self):
        return self.fileName

    def set_fileName(self, fileName):
        self.fileName = fileName
        self._fileName_callback(self.fileName)
        self.fileSource.open(self.testFiles + self.fileName, True)

    def get_carrierFrequency(self):
        return self.carrierFrequency

    def set_carrierFrequency(self, carrierFrequency):
        self.carrierFrequency = carrierFrequency





def main(top_block_cls=FSKTransmitter, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
