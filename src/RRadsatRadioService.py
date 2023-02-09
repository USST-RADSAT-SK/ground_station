#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Radsat Radio Service
# Author: Crawford
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from fskMod import fskMod  # grc-generated hier_block
from gmskDemod import gmskDemod  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from math import pi, ceil
from trxvuAx25Deframer import trxvuAx25Deframer  # grc-generated hier_block
from trxvuAx25Framer import trxvuAx25Framer  # grc-generated hier_block



from gnuradio import qtgui

class RRadsatRadioService(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Radsat Radio Service", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Radsat Radio Service")
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

        self.settings = Qt.QSettings("GNU Radio", "RRadsatRadioService")

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
        self.rxSamplesPerSymbol = rxSamplesPerSymbol = 60
        self.rxBaudRate = rxBaudRate = 9600
        self.txSamplesPerSymbol = txSamplesPerSymbol = 120
        self.txBaudRate = txBaudRate = rxBaudRate
        self.rxSampleRate = rxSampleRate = rxSamplesPerSymbol * rxBaudRate
        self.rxLowPassCutoff = rxLowPassCutoff = rxBaudRate+2000
        self.txSampleRate = txSampleRate = txSamplesPerSymbol * txBaudRate
        self.txGain = txGain = 0
        self.txFrequencyOffset = txFrequencyOffset = 0
        self.txFrequencyDeviation = txFrequencyDeviation = 3500
        self.txCorrection = txCorrection = 0
        self.txBaseband = txBaseband = 145.83E6
        self.sendFlags = sendFlags = True
        self.rxOverSample = rxOverSample = ceil(200000 / rxSampleRate)
        self.rxLowPassFilterTap = rxLowPassFilterTap = firdes.low_pass(1.0, rxSampleRate, rxLowPassCutoff,500, window.WIN_HAMMING, 6.76)
        self.rxGain = rxGain = 0
        self.rxFrequencyOffset = rxFrequencyOffset = 15000
        self.rxFrequencyDeviation = rxFrequencyDeviation = rxBaudRate // 4
        self.rxCorrection = rxCorrection = -1000
        self.rxBaseband = rxBaseband = 435.4e6
        self.radsatCallsign = radsatCallsign = "RADSAT"

        ##################################################
        # Blocks
        ##################################################
        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'Tx Tab')
        self.tabs_widget_1 = Qt.QWidget()
        self.tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_1)
        self.tabs_grid_layout_1 = Qt.QGridLayout()
        self.tabs_layout_1.addLayout(self.tabs_grid_layout_1)
        self.tabs.addTab(self.tabs_widget_1, 'Rx Tab')
        self.top_layout.addWidget(self.tabs)
        self._txGain_range = Range(0, 60, 1, 0, 200)
        self._txGain_win = RangeWidget(self._txGain_range, self.set_txGain, "Tx Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._txGain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        _sendFlags_check_box = Qt.QCheckBox("Send Inter-frame Flags")
        self._sendFlags_choices = {True: True, False: False}
        self._sendFlags_choices_inv = dict((v,k) for k,v in self._sendFlags_choices.items())
        self._sendFlags_callback = lambda i: Qt.QMetaObject.invokeMethod(_sendFlags_check_box, "setChecked", Qt.Q_ARG("bool", self._sendFlags_choices_inv[i]))
        self._sendFlags_callback(self.sendFlags)
        _sendFlags_check_box.stateChanged.connect(lambda i: self.set_sendFlags(self._sendFlags_choices[bool(i)]))
        self.top_layout.addWidget(_sendFlags_check_box)
        self._rxGain_range = Range(0, 100, 1, 0, 200)
        self._rxGain_win = RangeWidget(self._rxGain_range, self.set_rxGain, "Rx Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_1.addWidget(self._rxGain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_1.setColumnStretch(c, 1)
        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:15530', 100, True)
        self.zeromq_push_msg_sink_0 = zeromq.push_msg_sink('tcp://127.0.0.1:15531', 100, True)
        self.xlatingFIRfilter = filter.freq_xlating_fir_filter_ccc(rxOverSample, rxLowPassFilterTap, - rxFrequencyOffset*0, rxSampleRate)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("serial=31E34AD", 'name=MyB210,product=B210')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(rxSampleRate*rxOverSample)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(rxBaseband + rxFrequencyOffset*0 + rxCorrection, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(rxGain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("serial=31E34AD", 'name=MyB210,product=B210')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "tx_pkt_len",
        )
        self.uhd_usrp_sink_0.set_samp_rate(txSampleRate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(txBaseband, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(txGain, 0)
        self.uhd_usrp_sink_0.set_max_output_buffer(255)
        self.trxvuAx25Framer_0 = trxvuAx25Framer(
            EnableInterFrameFill=sendFlags,
            SamplesPerSymbol=txSamplesPerSymbol,
            destinationCallsign=radsatCallsign,
            destinationSsid=1,
            sourceCallsign=radsatCallsign,
            sourceSsid=10,
        )
        self.trxvuAx25Framer_0.set_max_output_buffer(8192)
        self.trxvuAx25Deframer_0 = trxvuAx25Deframer()
        self.qtgui_time_sink_x_0_1_0 = qtgui.time_sink_f(
            8*32, #size
            txSampleRate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1_0.set_update_time(0.016)
        self.qtgui_time_sink_x_0_1_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1_0.enable_tags(True)
        self.qtgui_time_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "pkt_length")
        self.qtgui_time_sink_x_0_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1_0.enable_grid(False)
        self.qtgui_time_sink_x_0_1_0.enable_axis_labels(False)
        self.qtgui_time_sink_x_0_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_0_1_0.disable_legend()

        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_0.qwidget(), Qt.QWidget)
        self.tabs_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_1_0_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_sink_x_1 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            rxBaseband, #fc
            rxSampleRate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.tabs_grid_layout_1.addWidget(self._qtgui_sink_x_1_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            txBaseband, #fc
            txSampleRate, #bw
            "Pre Demod", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.tabs_grid_layout_0.addWidget(self._qtgui_sink_x_0_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            rxBaseband, #fc
            rxSampleRate, #bw
            "", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.016)
        self.qtgui_freq_sink_x_0.set_y_axis(-250, 1)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['Post Filtering', 'Pre Filtering', '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["dark green", "dark blue", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.tabs_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_1.setColumnStretch(c, 1)
        self.gmskDemod_0 = gmskDemod(
            sampleRate=rxSampleRate,
            samplesPerSymbol=rxSamplesPerSymbol,
        )
        self.fskMod_0 = fskMod(
            baudRate=9600,
            frequencyDeviation=3500,
            samplesPerSymbol=txSamplesPerSymbol,
        )
        self.fskMod_0.set_max_output_buffer(100)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-2, 1e-1, 0.5, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)
        self.analog_agc2_xx_0.set_max_output_buffer(1024)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qtgui_freq_sink_x_0, 'freq'), (self.qtgui_freq_sink_x_0, 'freq'))
        self.msg_connect((self.qtgui_freq_sink_x_0, 'freq'), (self.uhd_usrp_source_0, 'command'))
        self.msg_connect((self.qtgui_freq_sink_x_0, 'freq'), (self.xlatingFIRfilter, 'freq'))
        self.msg_connect((self.trxvuAx25Deframer_0, 'msg_out'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.trxvuAx25Framer_0, 'Info in'))
        self.connect((self.analog_agc2_xx_0, 0), (self.gmskDemod_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0_1_0, 0))
        self.connect((self.fskMod_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.fskMod_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.gmskDemod_0, 2), (self.trxvuAx25Deframer_0, 0))
        self.connect((self.trxvuAx25Framer_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.trxvuAx25Framer_0, 0), (self.fskMod_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.xlatingFIRfilter, 0))
        self.connect((self.xlatingFIRfilter, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.xlatingFIRfilter, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.xlatingFIRfilter, 0), (self.qtgui_sink_x_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "RRadsatRadioService")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_rxSamplesPerSymbol(self):
        return self.rxSamplesPerSymbol

    def set_rxSamplesPerSymbol(self, rxSamplesPerSymbol):
        self.rxSamplesPerSymbol = rxSamplesPerSymbol
        self.set_rxSampleRate(self.rxSamplesPerSymbol * self.rxBaudRate)
        self.gmskDemod_0.set_samplesPerSymbol(self.rxSamplesPerSymbol)

    def get_rxBaudRate(self):
        return self.rxBaudRate

    def set_rxBaudRate(self, rxBaudRate):
        self.rxBaudRate = rxBaudRate
        self.set_rxFrequencyDeviation(self.rxBaudRate // 4)
        self.set_rxLowPassCutoff(self.rxBaudRate+2000)
        self.set_rxSampleRate(self.rxSamplesPerSymbol * self.rxBaudRate)
        self.set_txBaudRate(self.rxBaudRate)

    def get_txSamplesPerSymbol(self):
        return self.txSamplesPerSymbol

    def set_txSamplesPerSymbol(self, txSamplesPerSymbol):
        self.txSamplesPerSymbol = txSamplesPerSymbol
        self.set_txSampleRate(self.txSamplesPerSymbol * self.txBaudRate)
        self.fskMod_0.set_samplesPerSymbol(self.txSamplesPerSymbol)
        self.trxvuAx25Framer_0.set_SamplesPerSymbol(self.txSamplesPerSymbol)

    def get_txBaudRate(self):
        return self.txBaudRate

    def set_txBaudRate(self, txBaudRate):
        self.txBaudRate = txBaudRate
        self.set_txSampleRate(self.txSamplesPerSymbol * self.txBaudRate)

    def get_rxSampleRate(self):
        return self.rxSampleRate

    def set_rxSampleRate(self, rxSampleRate):
        self.rxSampleRate = rxSampleRate
        self.set_rxLowPassFilterTap(firdes.low_pass(1.0, self.rxSampleRate, self.rxLowPassCutoff, 500, window.WIN_HAMMING, 6.76))
        self.set_rxOverSample(ceil(200000 / self.rxSampleRate))
        self.gmskDemod_0.set_sampleRate(self.rxSampleRate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rxBaseband, self.rxSampleRate)
        self.qtgui_sink_x_1.set_frequency_range(self.rxBaseband, self.rxSampleRate)
        self.uhd_usrp_source_0.set_samp_rate(self.rxSampleRate*self.rxOverSample)

    def get_rxLowPassCutoff(self):
        return self.rxLowPassCutoff

    def set_rxLowPassCutoff(self, rxLowPassCutoff):
        self.rxLowPassCutoff = rxLowPassCutoff
        self.set_rxLowPassFilterTap(firdes.low_pass(1.0, self.rxSampleRate, self.rxLowPassCutoff, 500, window.WIN_HAMMING, 6.76))

    def get_txSampleRate(self):
        return self.txSampleRate

    def set_txSampleRate(self, txSampleRate):
        self.txSampleRate = txSampleRate
        self.qtgui_sink_x_0.set_frequency_range(self.txBaseband, self.txSampleRate)
        self.qtgui_time_sink_x_0_1_0.set_samp_rate(self.txSampleRate)
        self.uhd_usrp_sink_0.set_samp_rate(self.txSampleRate)

    def get_txGain(self):
        return self.txGain

    def set_txGain(self, txGain):
        self.txGain = txGain
        self.uhd_usrp_sink_0.set_gain(self.txGain, 0)

    def get_txFrequencyOffset(self):
        return self.txFrequencyOffset

    def set_txFrequencyOffset(self, txFrequencyOffset):
        self.txFrequencyOffset = txFrequencyOffset

    def get_txFrequencyDeviation(self):
        return self.txFrequencyDeviation

    def set_txFrequencyDeviation(self, txFrequencyDeviation):
        self.txFrequencyDeviation = txFrequencyDeviation

    def get_txCorrection(self):
        return self.txCorrection

    def set_txCorrection(self, txCorrection):
        self.txCorrection = txCorrection

    def get_txBaseband(self):
        return self.txBaseband

    def set_txBaseband(self, txBaseband):
        self.txBaseband = txBaseband
        self.qtgui_sink_x_0.set_frequency_range(self.txBaseband, self.txSampleRate)
        self.uhd_usrp_sink_0.set_center_freq(self.txBaseband, 0)

    def get_sendFlags(self):
        return self.sendFlags

    def set_sendFlags(self, sendFlags):
        self.sendFlags = sendFlags
        self._sendFlags_callback(self.sendFlags)
        self.trxvuAx25Framer_0.set_EnableInterFrameFill(self.sendFlags)

    def get_rxOverSample(self):
        return self.rxOverSample

    def set_rxOverSample(self, rxOverSample):
        self.rxOverSample = rxOverSample
        self.uhd_usrp_source_0.set_samp_rate(self.rxSampleRate*self.rxOverSample)

    def get_rxLowPassFilterTap(self):
        return self.rxLowPassFilterTap

    def set_rxLowPassFilterTap(self, rxLowPassFilterTap):
        self.rxLowPassFilterTap = rxLowPassFilterTap
        self.xlatingFIRfilter.set_taps(self.rxLowPassFilterTap)

    def get_rxGain(self):
        return self.rxGain

    def set_rxGain(self, rxGain):
        self.rxGain = rxGain
        self.uhd_usrp_source_0.set_gain(self.rxGain, 0)

    def get_rxFrequencyOffset(self):
        return self.rxFrequencyOffset

    def set_rxFrequencyOffset(self, rxFrequencyOffset):
        self.rxFrequencyOffset = rxFrequencyOffset
        self.uhd_usrp_source_0.set_center_freq(self.rxBaseband + self.rxFrequencyOffset*0 + self.rxCorrection, 0)
        self.xlatingFIRfilter.set_center_freq(- self.rxFrequencyOffset*0)

    def get_rxFrequencyDeviation(self):
        return self.rxFrequencyDeviation

    def set_rxFrequencyDeviation(self, rxFrequencyDeviation):
        self.rxFrequencyDeviation = rxFrequencyDeviation

    def get_rxCorrection(self):
        return self.rxCorrection

    def set_rxCorrection(self, rxCorrection):
        self.rxCorrection = rxCorrection
        self.uhd_usrp_source_0.set_center_freq(self.rxBaseband + self.rxFrequencyOffset*0 + self.rxCorrection, 0)

    def get_rxBaseband(self):
        return self.rxBaseband

    def set_rxBaseband(self, rxBaseband):
        self.rxBaseband = rxBaseband
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rxBaseband, self.rxSampleRate)
        self.qtgui_sink_x_1.set_frequency_range(self.rxBaseband, self.rxSampleRate)
        self.uhd_usrp_source_0.set_center_freq(self.rxBaseband + self.rxFrequencyOffset*0 + self.rxCorrection, 0)

    def get_radsatCallsign(self):
        return self.radsatCallsign

    def set_radsatCallsign(self, radsatCallsign):
        self.radsatCallsign = radsatCallsign
        self.trxvuAx25Framer_0.set_destinationCallsign(self.radsatCallsign)
        self.trxvuAx25Framer_0.set_sourceCallsign(self.radsatCallsign)




def main(top_block_cls=RRadsatRadioService, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
