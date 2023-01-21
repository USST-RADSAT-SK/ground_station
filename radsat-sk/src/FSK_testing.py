#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK_testing
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

from FM_Modulator_rev1 import FM_Modulator_rev1  # grc-generated hier_block
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from TRXVU_AX_25_Framer import TRXVU_AX_25_Framer  # grc-generated hier_block
from gnuradio import blocks
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



from gnuradio import qtgui

class FSK_testing(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FSK_testing", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FSK_testing")
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

        self.settings = Qt.QSettings("GNU Radio", "FSK_testing")

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
        self.rxSamplesPerSymbol = rxSamplesPerSymbol = 30
        self.rxBaudRate = rxBaudRate = 9600
        self.txSamplesPerSymbol = txSamplesPerSymbol = 60
        self.txBaudRate = txBaudRate = 9600
        self.rxSampleRate = rxSampleRate = rxSamplesPerSymbol * rxBaudRate
        self.rxLowPassCutoff = rxLowPassCutoff = rxBaudRate+2000
        self.txSampleRate = txSampleRate = txSamplesPerSymbol * txBaudRate
        self.txLowPassCutoff = txLowPassCutoff = rxBaudRate
        self.txGain = txGain = 0
        self.txFrequencyOffset = txFrequencyOffset = 15000
        self.txFrequencyDeviation = txFrequencyDeviation = 3500
        self.txCorrection = txCorrection = 0
        self.txBaseband = txBaseband = 145.83E6
        self.rxLowPassFilterTap = rxLowPassFilterTap = firdes.low_pass(1.0, rxSampleRate, rxLowPassCutoff,500, window.WIN_HAMMING, 6.76)
        self.rxGain = rxGain = 0
        self.rxFrequencyOffset = rxFrequencyOffset = 15000
        self.rxFrequencyDeviation = rxFrequencyDeviation = rxBaudRate // 4
        self.rxCorrection = rxCorrection = -1000
        self.rxBaseband = rxBaseband = 435.4e6

        ##################################################
        # Blocks
        ##################################################
        self._txGain_range = Range(0, 100, 1, 0, 200)
        self._txGain_win = RangeWidget(self._txGain_range, self.set_txGain, "Tx Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._txGain_win)
        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:15530', 100, True)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("serial=31E34AD", 'name=MyB210,product=B210')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(txSampleRate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(txBaseband, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(txGain, 0)
        self._rxGain_range = Range(0, 100, 1, 0, 200)
        self._rxGain_win = RangeWidget(self._rxGain_range, self.set_rxGain, "Rx Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rxGain_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            txSampleRate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


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


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            rxSampleRate, #bw
            "Pre Demod", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', 'time', False, False, '', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_edit_box_msg_0_win)
        self.blocks_not_xx_0 = blocks.not_bb()
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.TRXVU_AX_25_Framer_0 = TRXVU_AX_25_Framer(
            destinationCallsign='RADSAT',
            destinationSsid=1,
            sourceCallsign='RADSAT',
            sourceSsid=2,
        )
        self.FM_Modulator_rev1_0 = FM_Modulator_rev1(
            baudRate=txBaudRate,
            frequencyDeviation=txFrequencyDeviation,
            samplesPerSymbol=txSamplesPerSymbol,
        )


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.TRXVU_AX_25_Framer_0, 'Info in'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.TRXVU_AX_25_Framer_0, 'Info in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.FM_Modulator_rev1_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.FM_Modulator_rev1_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.FM_Modulator_rev1_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.TRXVU_AX_25_Framer_0, 0), (self.blocks_not_xx_0, 0))
        self.connect((self.blocks_not_xx_0, 0), (self.FM_Modulator_rev1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FSK_testing")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_rxSamplesPerSymbol(self):
        return self.rxSamplesPerSymbol

    def set_rxSamplesPerSymbol(self, rxSamplesPerSymbol):
        self.rxSamplesPerSymbol = rxSamplesPerSymbol
        self.set_rxSampleRate(self.rxSamplesPerSymbol * self.rxBaudRate)

    def get_rxBaudRate(self):
        return self.rxBaudRate

    def set_rxBaudRate(self, rxBaudRate):
        self.rxBaudRate = rxBaudRate
        self.set_rxFrequencyDeviation(self.rxBaudRate // 4)
        self.set_rxLowPassCutoff(self.rxBaudRate+2000)
        self.set_rxSampleRate(self.rxSamplesPerSymbol * self.rxBaudRate)
        self.set_txLowPassCutoff(self.rxBaudRate)

    def get_txSamplesPerSymbol(self):
        return self.txSamplesPerSymbol

    def set_txSamplesPerSymbol(self, txSamplesPerSymbol):
        self.txSamplesPerSymbol = txSamplesPerSymbol
        self.set_txSampleRate(self.txSamplesPerSymbol * self.txBaudRate)
        self.FM_Modulator_rev1_0.set_samplesPerSymbol(self.txSamplesPerSymbol)

    def get_txBaudRate(self):
        return self.txBaudRate

    def set_txBaudRate(self, txBaudRate):
        self.txBaudRate = txBaudRate
        self.set_txSampleRate(self.txSamplesPerSymbol * self.txBaudRate)
        self.FM_Modulator_rev1_0.set_baudRate(self.txBaudRate)

    def get_rxSampleRate(self):
        return self.rxSampleRate

    def set_rxSampleRate(self, rxSampleRate):
        self.rxSampleRate = rxSampleRate
        self.set_rxLowPassFilterTap(firdes.low_pass(1.0, self.rxSampleRate, self.rxLowPassCutoff, 500, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.rxSampleRate)

    def get_rxLowPassCutoff(self):
        return self.rxLowPassCutoff

    def set_rxLowPassCutoff(self, rxLowPassCutoff):
        self.rxLowPassCutoff = rxLowPassCutoff
        self.set_rxLowPassFilterTap(firdes.low_pass(1.0, self.rxSampleRate, self.rxLowPassCutoff, 500, window.WIN_HAMMING, 6.76))

    def get_txSampleRate(self):
        return self.txSampleRate

    def set_txSampleRate(self, txSampleRate):
        self.txSampleRate = txSampleRate
        self.qtgui_time_sink_x_0.set_samp_rate(self.txSampleRate)
        self.uhd_usrp_sink_0.set_samp_rate(self.txSampleRate)

    def get_txLowPassCutoff(self):
        return self.txLowPassCutoff

    def set_txLowPassCutoff(self, txLowPassCutoff):
        self.txLowPassCutoff = txLowPassCutoff

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
        self.FM_Modulator_rev1_0.set_frequencyDeviation(self.txFrequencyDeviation)

    def get_txCorrection(self):
        return self.txCorrection

    def set_txCorrection(self, txCorrection):
        self.txCorrection = txCorrection

    def get_txBaseband(self):
        return self.txBaseband

    def set_txBaseband(self, txBaseband):
        self.txBaseband = txBaseband
        self.uhd_usrp_sink_0.set_center_freq(self.txBaseband, 0)

    def get_rxLowPassFilterTap(self):
        return self.rxLowPassFilterTap

    def set_rxLowPassFilterTap(self, rxLowPassFilterTap):
        self.rxLowPassFilterTap = rxLowPassFilterTap

    def get_rxGain(self):
        return self.rxGain

    def set_rxGain(self, rxGain):
        self.rxGain = rxGain

    def get_rxFrequencyOffset(self):
        return self.rxFrequencyOffset

    def set_rxFrequencyOffset(self, rxFrequencyOffset):
        self.rxFrequencyOffset = rxFrequencyOffset

    def get_rxFrequencyDeviation(self):
        return self.rxFrequencyDeviation

    def set_rxFrequencyDeviation(self, rxFrequencyDeviation):
        self.rxFrequencyDeviation = rxFrequencyDeviation

    def get_rxCorrection(self):
        return self.rxCorrection

    def set_rxCorrection(self, rxCorrection):
        self.rxCorrection = rxCorrection

    def get_rxBaseband(self):
        return self.rxBaseband

    def set_rxBaseband(self, rxBaseband):
        self.rxBaseband = rxBaseband




def main(top_block_cls=FSK_testing, options=None):

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
