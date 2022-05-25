#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK Transmitter
# Author: austin
# GNU Radio version: 3.8.1.0

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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import limesdr
import math
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
        self.samplesPerSymbol = samplesPerSymbol = 32
        self.baudRate = baudRate = 9600
        self.txgain = txgain = 10
        self.txSampleRate = txSampleRate = baudRate * samplesPerSymbol
        self.frequencyDeviation = frequencyDeviation = baudRate//2
        self.freqError = freqError = 200
        self.carrierFrequency = carrierFrequency = 915e6

        ##################################################
        # Blocks
        ##################################################
        self._txgain_range = Range(0, 60, 1, 10, 200)
        self._txgain_win = RangeWidget(self._txgain_range, self.set_txgain, 'Tx gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._txgain_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.top_grid_layout.addWidget(self.tabs, 10, 0, 1, 1)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1_0_0 = qtgui.time_sink_c(
            1024 * 2, #size
            txSampleRate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1_0_0.set_y_axis(-1.2, 1.2)

        self.qtgui_time_sink_x_0_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_1_0_0.enable_stem_plot(True)


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
                    self.qtgui_time_sink_x_0_1_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_1_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_0_0.pyqwidget(), Qt.QWidget)
        self.tabs_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_1_0_0_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_HAMMING, #wintype
            0, #fc
            txSampleRate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.tabs_grid_layout_0.addWidget(self._qtgui_sink_x_0_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.limesdr_sink_0_0 = limesdr.sink('', 0, '', '')


        self.limesdr_sink_0_0.set_sample_rate(txSampleRate)


        self.limesdr_sink_0_0.set_center_freq(carrierFrequency, 0)

        self.limesdr_sink_0_0.set_bandwidth(5e6, 0)


        self.limesdr_sink_0_0.set_digital_filter(frequencyDeviation+freqError, 0)


        self.limesdr_sink_0_0.set_gain(txgain, 0)


        self.limesdr_sink_0_0.set_antenna(255, 0)


        self.limesdr_sink_0_0.calibrate(2.5e6, 0)
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
            samples_per_symbol=samplesPerSymbol,
            bt=0.5,
            verbose=False,
            log=False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/radsat-gs/ground_station/examples/SampleBinaryFiles/50p_duty_32B.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.limesdr_sink_0_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.qtgui_time_sink_x_0_1_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FSKTransmitter")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samplesPerSymbol(self):
        return self.samplesPerSymbol

    def set_samplesPerSymbol(self, samplesPerSymbol):
        self.samplesPerSymbol = samplesPerSymbol
        self.set_txSampleRate(self.baudRate * self.samplesPerSymbol)

    def get_baudRate(self):
        return self.baudRate

    def set_baudRate(self, baudRate):
        self.baudRate = baudRate
        self.set_frequencyDeviation(self.baudRate//2)
        self.set_txSampleRate(self.baudRate * self.samplesPerSymbol)

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.limesdr_sink_0_0.set_gain(self.txgain, 0)

    def get_txSampleRate(self):
        return self.txSampleRate

    def set_txSampleRate(self, txSampleRate):
        self.txSampleRate = txSampleRate
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.txSampleRate)
        self.qtgui_time_sink_x_0_1_0_0.set_samp_rate(self.txSampleRate)

    def get_frequencyDeviation(self):
        return self.frequencyDeviation

    def set_frequencyDeviation(self, frequencyDeviation):
        self.frequencyDeviation = frequencyDeviation
        self.limesdr_sink_0_0.set_digital_filter(self.frequencyDeviation+self.freqError, 0)

    def get_freqError(self):
        return self.freqError

    def set_freqError(self, freqError):
        self.freqError = freqError
        self.limesdr_sink_0_0.set_digital_filter(self.frequencyDeviation+self.freqError, 0)

    def get_carrierFrequency(self):
        return self.carrierFrequency

    def set_carrierFrequency(self, carrierFrequency):
        self.carrierFrequency = carrierFrequency
        self.limesdr_sink_0_0.set_center_freq(self.carrierFrequency, 0)



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
