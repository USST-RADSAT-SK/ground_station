#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM Receiver
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
from gnuradio import audio
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import osmosdr
import time

from gnuradio import qtgui


class RFMReceiver(gr.top_block, Qt.QWidget):
    def __init__(self):
        gr.top_block.__init__(self, "FM Receiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM Receiver")
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

        self.settings = Qt.QSettings("GNU Radio", "RFMReceiver")

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
        self.audioSampleRate = audioSampleRate = 48000
        self.rxSampleRate = rxSampleRate = audioSampleRate * 25
        self.rxGain = rxGain = 0
        self.carrierFrequency = carrierFrequency = 95.1e6

        ##################################################
        # Blocks
        ##################################################
        self._rxGain_range = Range(0, 70, 1, 0, 200)
        self._rxGain_win = RangeWidget(
            self._rxGain_range, self.set_rxGain, "RX Gain", "counter_slider", float
        )
        self.top_grid_layout.addWidget(self._rxGain_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._carrierFrequency_range = Range(50e6, 1.6e9, 0.025e6, 95.1e6, 200)
        self._carrierFrequency_win = RangeWidget(
            self._carrierFrequency_range,
            self.set_carrierFrequency,
            "Carrier Frequency (Hz)",
            "counter",
            float,
        )
        self.top_grid_layout.addWidget(self._carrierFrequency_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rtlSDRSource = osmosdr.source(args="numchan=" + str(1) + " " + "")
        self.rtlSDRSource.set_sample_rate(rxSampleRate)
        self.rtlSDRSource.set_center_freq(carrierFrequency, 0)
        self.rtlSDRSource.set_freq_corr(0, 0)
        self.rtlSDRSource.set_dc_offset_mode(0, 0)
        self.rtlSDRSource.set_iq_balance_mode(0, 0)
        self.rtlSDRSource.set_gain_mode(False, 0)
        self.rtlSDRSource.set_gain(rxGain, 0)
        self.rtlSDRSource.set_if_gain(20, 0)
        self.rtlSDRSource.set_bb_gain(20, 0)
        self.rtlSDRSource.set_antenna("", 0)
        self.rtlSDRSource.set_bandwidth(0, 0)
        self.lowPassFilter = filter.fir_filter_ccf(
            1, firdes.low_pass(1, rxSampleRate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76)
        )
        self.guiSink = qtgui.sink_c(
            1024,  # fftsize
            firdes.WIN_BLACKMAN_hARRIS,  # wintype
            carrierFrequency,  # fc
            rxSampleRate,  # bw
            "",  # name
            True,  # plotfreq
            True,  # plotwaterfall
            False,  # plottime
            False,  # plotconst
        )
        self.guiSink.set_update_time(1.0 / 20)
        self._guiSink_win = sip.wrapinstance(self.guiSink.pyqwidget(), Qt.QWidget)

        self.guiSink.enable_rf_freq(True)

        self.top_grid_layout.addWidget(self._guiSink_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fmDemodulator = analog.wfm_rcv(
            quad_rate=rxSampleRate,
            audio_decimation=rxSampleRate // audioSampleRate,
        )
        self.audioTimeSink = qtgui.time_sink_f(
            1024,  # size
            audioSampleRate,  # samp_rate
            "",  # name
            1,  # number of inputs
        )
        self.audioTimeSink.set_update_time(1 / 20)
        self.audioTimeSink.set_y_axis(-1.2, 1.2)

        self.audioTimeSink.set_y_label("Amplitude", "")

        self.audioTimeSink.enable_tags(True)
        self.audioTimeSink.set_trigger_mode(
            qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, ""
        )
        self.audioTimeSink.enable_autoscale(False)
        self.audioTimeSink.enable_grid(True)
        self.audioTimeSink.enable_axis_labels(True)
        self.audioTimeSink.enable_control_panel(True)
        self.audioTimeSink.enable_stem_plot(False)

        self.audioTimeSink.disable_legend()

        labels = [
            "Signal 1",
            "Signal 2",
            "Signal 3",
            "Signal 4",
            "Signal 5",
            "Signal 6",
            "Signal 7",
            "Signal 8",
            "Signal 9",
            "Signal 10",
        ]
        widths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        colors = [
            "blue",
            "red",
            "green",
            "black",
            "cyan",
            "magenta",
            "yellow",
            "dark red",
            "dark green",
            "dark blue",
        ]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        for i in range(1):
            if len(labels[i]) == 0:
                self.audioTimeSink.set_line_label(i, "Data {0}".format(i))
            else:
                self.audioTimeSink.set_line_label(i, labels[i])
            self.audioTimeSink.set_line_width(i, widths[i])
            self.audioTimeSink.set_line_color(i, colors[i])
            self.audioTimeSink.set_line_style(i, styles[i])
            self.audioTimeSink.set_line_marker(i, markers[i])
            self.audioTimeSink.set_line_alpha(i, alphas[i])

        self._audioTimeSink_win = sip.wrapinstance(
            self.audioTimeSink.pyqwidget(), Qt.QWidget
        )
        self.top_grid_layout.addWidget(self._audioTimeSink_win, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.audioSink = audio.sink(audioSampleRate, "", False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.fmDemodulator, 0), (self.audioSink, 0))
        self.connect((self.fmDemodulator, 0), (self.audioTimeSink, 0))
        self.connect((self.lowPassFilter, 0), (self.fmDemodulator, 0))
        self.connect((self.rtlSDRSource, 0), (self.guiSink, 0))
        self.connect((self.rtlSDRSource, 0), (self.lowPassFilter, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "RFMReceiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_audioSampleRate(self):
        return self.audioSampleRate

    def set_audioSampleRate(self, audioSampleRate):
        self.audioSampleRate = audioSampleRate
        self.set_rxSampleRate(self.audioSampleRate * 25)
        self.audioTimeSink.set_samp_rate(self.audioSampleRate)

    def get_rxSampleRate(self):
        return self.rxSampleRate

    def set_rxSampleRate(self, rxSampleRate):
        self.rxSampleRate = rxSampleRate
        self.guiSink.set_frequency_range(self.carrierFrequency, self.rxSampleRate)
        self.lowPassFilter.set_taps(
            firdes.low_pass(1, self.rxSampleRate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76)
        )
        self.rtlSDRSource.set_sample_rate(self.rxSampleRate)

    def get_rxGain(self):
        return self.rxGain

    def set_rxGain(self, rxGain):
        self.rxGain = rxGain
        self.rtlSDRSource.set_gain(self.rxGain, 0)

    def get_carrierFrequency(self):
        return self.carrierFrequency

    def set_carrierFrequency(self, carrierFrequency):
        self.carrierFrequency = carrierFrequency
        self.guiSink.set_frequency_range(self.carrierFrequency, self.rxSampleRate)
        self.rtlSDRSource.set_center_freq(self.carrierFrequency, 0)


def main(top_block_cls=RFMReceiver, options=None):

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
