#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM Transmitter
# Author: Austin
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == "__main__":
    import ctypes
    import sys

    if sys.platform.startswith("linux"):
        try:
            x11 = ctypes.cdll.LoadLibrary("libX11.so")
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import limesdr

from gnuradio import qtgui


class RFMTransmitter(gr.top_block, Qt.QWidget):
    def __init__(self):
        gr.top_block.__init__(self, "FM Transmitter")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM Transmitter")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme("gnuradio-grc"))
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

        self.settings = Qt.QSettings("GNU Radio", "RFMTransmitter")

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
        self.bandwidth = bandwidth = 160e3
        self.preModSampleRate = preModSampleRate = bandwidth + 50e3
        self.audioSampleRate = audioSampleRate = 44100
        self.txSampleRate = txSampleRate = int(preModSampleRate * 5)
        self.txGain = txGain = 0
        self.preModSampleRatio = preModSampleRatio = audioSampleRate / preModSampleRate
        self.carrierFrequency = carrierFrequency = 107.1e6

        ##################################################
        # Blocks
        ##################################################
        self._txGain_range = Range(0, 60, 0.1, 0, 200)
        self._txGain_win = RangeWidget(
            self._txGain_range, self.set_txGain, "Gain", "counter_slider", float
        )
        self.top_grid_layout.addWidget(self._txGain_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.txGUISink = qtgui.sink_c(
            1024,  # fftsize
            firdes.WIN_HAMMING,  # wintype
            0,  # fc
            txSampleRate,  # bw
            "",  # name
            True,  # plotfreq
            True,  # plotwaterfall
            False,  # plottime
            True,  # plotconst
        )
        self.txGUISink.set_update_time(1.0 / 20)
        self._txGUISink_win = sip.wrapinstance(self.txGUISink.pyqwidget(), Qt.QWidget)

        self.txGUISink.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._txGUISink_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.preModInterpolator = filter.mmse_interpolator_ff(0, preModSampleRatio)
        self.limeSDRSink = limesdr.sink("", 0, "", "")

        self.limeSDRSink.set_sample_rate(txSampleRate)

        self.limeSDRSink.set_center_freq(carrierFrequency, 0)

        self.limeSDRSink.set_bandwidth(5e6, 0)

        self.limeSDRSink.set_digital_filter(bandwidth, 0)

        self.limeSDRSink.set_gain(txGain, 0)

        self.limeSDRSink.set_antenna(255, 0)

        self.limeSDRSink.calibrate(2.5e6, 0)
        self.audioSource = blocks.wavfile_source("BrittleRilleByKevinMacLeod.wav", True)
        self.WBFMModulator = analog.wfm_tx(
            audio_rate=int(preModSampleRate),
            quad_rate=int(txSampleRate),
            tau=75e-6,
            max_dev=bandwidth // 2 - 5000,
            fh=-1.0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.WBFMModulator, 0), (self.limeSDRSink, 0))
        self.connect((self.WBFMModulator, 0), (self.txGUISink, 0))
        self.connect((self.audioSource, 0), (self.preModInterpolator, 0))
        self.connect((self.preModInterpolator, 0), (self.WBFMModulator, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "RFMTransmitter")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_preModSampleRate(self.bandwidth + 50e3)
        self.limeSDRSink.set_digital_filter(self.bandwidth, 0)

    def get_preModSampleRate(self):
        return self.preModSampleRate

    def set_preModSampleRate(self, preModSampleRate):
        self.preModSampleRate = preModSampleRate
        self.set_preModSampleRatio(self.audioSampleRate / self.preModSampleRate)
        self.set_txSampleRate(int(self.preModSampleRate * 5))

    def get_audioSampleRate(self):
        return self.audioSampleRate

    def set_audioSampleRate(self, audioSampleRate):
        self.audioSampleRate = audioSampleRate
        self.set_preModSampleRatio(self.audioSampleRate / self.preModSampleRate)

    def get_txSampleRate(self):
        return self.txSampleRate

    def set_txSampleRate(self, txSampleRate):
        self.txSampleRate = txSampleRate
        self.txGUISink.set_frequency_range(0, self.txSampleRate)

    def get_txGain(self):
        return self.txGain

    def set_txGain(self, txGain):
        self.txGain = txGain
        self.limeSDRSink.set_gain(self.txGain, 0)

    def get_preModSampleRatio(self):
        return self.preModSampleRatio

    def set_preModSampleRatio(self, preModSampleRatio):
        self.preModSampleRatio = preModSampleRatio
        self.preModInterpolator.set_interp_ratio(self.preModSampleRatio)

    def get_carrierFrequency(self):
        return self.carrierFrequency

    def set_carrierFrequency(self, carrierFrequency):
        self.carrierFrequency = carrierFrequency
        self.limeSDRSink.set_center_freq(self.carrierFrequency, 0)


def main(top_block_cls=RFMTransmitter, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string("qtgui", "style", "raster")
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


if __name__ == "__main__":
    main()
