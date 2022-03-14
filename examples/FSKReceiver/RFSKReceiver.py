#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK Receiver
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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import CLIPrintSink
import math
import osmosdr
import time
import satellites.components.demodulators

from gnuradio import qtgui

class RFSKReceiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FSK Receiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FSK Receiver")
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

        self.settings = Qt.QSettings("GNU Radio", "RFSKReceiver")

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
        self.baudRate = baudRate = 9600
        self.bandwidth = bandwidth = 5000
        self.samplePerSecond = samplePerSecond = 30
        self.frequencyDeviation = frequencyDeviation = abs(bandwidth//2 - baudRate)
        self.sampleRate = sampleRate = baudRate * samplePerSecond
        self.rxGain = rxGain = 0
        self.frequencyOffset = frequencyOffset = 0
        self.filterWidth = filterWidth = frequencyDeviation
        self.exampleDelay = exampleDelay = 0
        self.carrierFrequency = carrierFrequency = 433e6

        ##################################################
        # Blocks
        ##################################################
        self._rxGain_range = Range(0, 70, 1, 0, 200)
        self._rxGain_win = RangeWidget(self._rxGain_range, self.set_rxGain, 'Rx gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rxGain_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._frequencyOffset_range = Range(-7000, 7000, 50, 0, 200)
        self._frequencyOffset_win = RangeWidget(self._frequencyOffset_range, self.set_frequencyOffset, 'filter size', "counter_slider", float)
        self.top_grid_layout.addWidget(self._frequencyOffset_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._filterWidth_range = Range(1000, 25000, 100, frequencyDeviation, 200)
        self._filterWidth_win = RangeWidget(self._filterWidth_range, self.set_filterWidth, 'Filter Width', "counter_slider", float)
        self.top_grid_layout.addWidget(self._filterWidth_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._exampleDelay_range = Range(-16*8, 16*8, 1, 0, 200)
        self._exampleDelay_win = RangeWidget(self._exampleDelay_range, self.set_exampleDelay, 'Data Comparison Position', "counter_slider", float)
        self.top_grid_layout.addWidget(self._exampleDelay_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.xlatingFIRfilter = filter.freq_xlating_fir_filter_ccc(4, [1], frequencyOffset, sampleRate * 4)
        self.uCharToFloat = blocks.uchar_to_float()
        self.preTranslateGUISink = qtgui.sink_c(
            1024*4, #fftsize
            firdes.WIN_BLACKMAN, #wintype
            carrierFrequency, #fc
            sampleRate * 4, #bw
            "Pre Translate", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.preTranslateGUISink.set_update_time(1.0/10)
        self._preTranslateGUISink_win = sip.wrapinstance(self.preTranslateGUISink.pyqwidget(), Qt.QWidget)

        self.preTranslateGUISink.enable_rf_freq(True)

        self.top_grid_layout.addWidget(self._preTranslateGUISink_win, 13, 0, 1, 1)
        for r in range(13, 14):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.preDemodLowPassFilter = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                sampleRate,
                filterWidth,
                300,
                firdes.WIN_HAMMING,
                6.76))
        self.postDemodGUISink = qtgui.sink_f(
            1024, #fftsize
            firdes.WIN_BLACKMAN, #wintype
            0, #fc
            baudRate, #bw
            "Post Demod", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.postDemodGUISink.set_update_time(1.0/10)
        self._postDemodGUISink_win = sip.wrapinstance(self.postDemodGUISink.pyqwidget(), Qt.QWidget)

        self.postDemodGUISink.enable_rf_freq(True)

        self.top_grid_layout.addWidget(self._postDemodGUISink_win, 12, 0, 1, 1)
        for r in range(12, 13):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.osmoSDRSource = osmosdr.source(
            args="numchan=" + str(1) + " " + "rtl=0"
        )
        self.osmoSDRSource.set_sample_rate(sampleRate * 4)
        self.osmoSDRSource.set_center_freq(carrierFrequency, 0)
        self.osmoSDRSource.set_freq_corr(0, 0)
        self.osmoSDRSource.set_dc_offset_mode(0, 0)
        self.osmoSDRSource.set_iq_balance_mode(0, 0)
        self.osmoSDRSource.set_gain_mode(False, 0)
        self.osmoSDRSource.set_gain(rxGain, 0)
        self.osmoSDRSource.set_if_gain(20, 0)
        self.osmoSDRSource.set_bb_gain(20, 0)
        self.osmoSDRSource.set_antenna('', 0)
        self.osmoSDRSource.set_bandwidth(0, 0)
        self.multiplyConst = blocks.multiply_const_cc(0.0001)
        self.lowPassCompairSink = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            sampleRate, #bw
            "", #name
            2
        )
        self.lowPassCompairSink.set_update_time(0.10)
        self.lowPassCompairSink.set_y_axis(-140, 10)
        self.lowPassCompairSink.set_y_label('Relative Gain', 'dB')
        self.lowPassCompairSink.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.lowPassCompairSink.enable_autoscale(False)
        self.lowPassCompairSink.enable_grid(False)
        self.lowPassCompairSink.set_fft_average(1.0)
        self.lowPassCompairSink.enable_axis_labels(True)
        self.lowPassCompairSink.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.lowPassCompairSink.set_line_label(i, "Data {0}".format(i))
            else:
                self.lowPassCompairSink.set_line_label(i, labels[i])
            self.lowPassCompairSink.set_line_width(i, widths[i])
            self.lowPassCompairSink.set_line_color(i, colors[i])
            self.lowPassCompairSink.set_line_alpha(i, alphas[i])

        self._lowPassCompairSink_win = sip.wrapinstance(self.lowPassCompairSink.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._lowPassCompairSink_win, 11, 0, 1, 1)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.invertExample = blocks.multiply_const_ff(-1)
        self.exampleUnpack = blocks.unpack_k_bits_bb(8)
        self.exampleFileSource = blocks.file_source(gr.sizeof_char*1, '/home/austin/Documents/usst/ground_station/examples/SampleBinaryFiles/pyramid_32B.bin', True, 0, 0)
        self.exampleFileSource.set_begin_tag(pmt.PMT_NIL)
        self.delayExample = blocks.delay(gr.sizeof_float*1, exampleDelay)
        self.compairUCharToFloat = blocks.uchar_to_float()
        self.bitCompariosn = qtgui.time_sink_f(
            32*8*2, #size
            1, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.bitCompariosn.set_update_time(1/30)
        self.bitCompariosn.set_y_axis(-1.1, 1.1)

        self.bitCompariosn.set_y_label('Amplitude', "")

        self.bitCompariosn.enable_tags(False)
        self.bitCompariosn.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.bitCompariosn.enable_autoscale(False)
        self.bitCompariosn.enable_grid(True)
        self.bitCompariosn.enable_axis_labels(True)
        self.bitCompariosn.enable_control_panel(False)
        self.bitCompariosn.enable_stem_plot(True)


        labels = ['TX Binary', 'RX Binary Demod', '', '', '',
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


        for i in range(2):
            if len(labels[i]) == 0:
                self.bitCompariosn.set_line_label(i, "Data {0}".format(i))
            else:
                self.bitCompariosn.set_line_label(i, labels[i])
            self.bitCompariosn.set_line_width(i, widths[i])
            self.bitCompariosn.set_line_color(i, colors[i])
            self.bitCompariosn.set_line_style(i, styles[i])
            self.bitCompariosn.set_line_marker(i, markers[i])
            self.bitCompariosn.set_line_alpha(i, alphas[i])

        self._bitCompariosn_win = sip.wrapinstance(self.bitCompariosn.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._bitCompariosn_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.binarySlicer = digital.binary_slicer_fb()
        self.agc = analog.agc_cc(1e-4, 0.8, 1.0)
        self.agc.set_max_gain(65536)
        self.FSKDemod = satellites.components.demodulators.fsk_demodulator(baudrate = baudRate, samp_rate = sampleRate, iq = True, subaudio = False, options="")
        self.CLIPrintSink = CLIPrintSink.blk(flag=0b01111110, maxLen=255, minLen=136)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.FSKDemod, 0), (self.binarySlicer, 0))
        self.connect((self.FSKDemod, 0), (self.postDemodGUISink, 0))
        self.connect((self.agc, 0), (self.FSKDemod, 0))
        self.connect((self.agc, 0), (self.lowPassCompairSink, 0))
        self.connect((self.binarySlicer, 0), (self.CLIPrintSink, 0))
        self.connect((self.binarySlicer, 0), (self.uCharToFloat, 0))
        self.connect((self.compairUCharToFloat, 0), (self.invertExample, 0))
        self.connect((self.delayExample, 0), (self.bitCompariosn, 0))
        self.connect((self.exampleFileSource, 0), (self.exampleUnpack, 0))
        self.connect((self.exampleUnpack, 0), (self.compairUCharToFloat, 0))
        self.connect((self.invertExample, 0), (self.delayExample, 0))
        self.connect((self.multiplyConst, 0), (self.lowPassCompairSink, 1))
        self.connect((self.multiplyConst, 0), (self.preDemodLowPassFilter, 0))
        self.connect((self.osmoSDRSource, 0), (self.preTranslateGUISink, 0))
        self.connect((self.osmoSDRSource, 0), (self.xlatingFIRfilter, 0))
        self.connect((self.preDemodLowPassFilter, 0), (self.agc, 0))
        self.connect((self.uCharToFloat, 0), (self.bitCompariosn, 1))
        self.connect((self.xlatingFIRfilter, 0), (self.multiplyConst, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "RFSKReceiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_baudRate(self):
        return self.baudRate

    def set_baudRate(self, baudRate):
        self.baudRate = baudRate
        self.set_frequencyDeviation(abs(self.bandwidth//2 - self.baudRate))
        self.set_sampleRate(self.baudRate * self.samplePerSecond)
        self.postDemodGUISink.set_frequency_range(0, self.baudRate)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_frequencyDeviation(abs(self.bandwidth//2 - self.baudRate))

    def get_samplePerSecond(self):
        return self.samplePerSecond

    def set_samplePerSecond(self, samplePerSecond):
        self.samplePerSecond = samplePerSecond
        self.set_sampleRate(self.baudRate * self.samplePerSecond)

    def get_frequencyDeviation(self):
        return self.frequencyDeviation

    def set_frequencyDeviation(self, frequencyDeviation):
        self.frequencyDeviation = frequencyDeviation
        self.set_filterWidth(self.frequencyDeviation)

    def get_sampleRate(self):
        return self.sampleRate

    def set_sampleRate(self, sampleRate):
        self.sampleRate = sampleRate
        self.lowPassCompairSink.set_frequency_range(0, self.sampleRate)
        self.osmoSDRSource.set_sample_rate(self.sampleRate * 4)
        self.preDemodLowPassFilter.set_taps(firdes.low_pass(1, self.sampleRate, self.filterWidth, 300, firdes.WIN_HAMMING, 6.76))
        self.preTranslateGUISink.set_frequency_range(self.carrierFrequency, self.sampleRate * 4)

    def get_rxGain(self):
        return self.rxGain

    def set_rxGain(self, rxGain):
        self.rxGain = rxGain
        self.osmoSDRSource.set_gain(self.rxGain, 0)

    def get_frequencyOffset(self):
        return self.frequencyOffset

    def set_frequencyOffset(self, frequencyOffset):
        self.frequencyOffset = frequencyOffset
        self.xlatingFIRfilter.set_center_freq(self.frequencyOffset)

    def get_filterWidth(self):
        return self.filterWidth

    def set_filterWidth(self, filterWidth):
        self.filterWidth = filterWidth
        self.preDemodLowPassFilter.set_taps(firdes.low_pass(1, self.sampleRate, self.filterWidth, 300, firdes.WIN_HAMMING, 6.76))

    def get_exampleDelay(self):
        return self.exampleDelay

    def set_exampleDelay(self, exampleDelay):
        self.exampleDelay = exampleDelay
        self.delayExample.set_dly(self.exampleDelay)

    def get_carrierFrequency(self):
        return self.carrierFrequency

    def set_carrierFrequency(self, carrierFrequency):
        self.carrierFrequency = carrierFrequency
        self.osmoSDRSource.set_center_freq(self.carrierFrequency, 0)
        self.preTranslateGUISink.set_frequency_range(self.carrierFrequency, self.sampleRate * 4)





def main(top_block_cls=RFSKReceiver, options=None):

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
