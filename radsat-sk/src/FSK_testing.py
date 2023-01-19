#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK_testing
# Author: Crawford
# GNU Radio version: 3.10.4.0

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

from FM_Demodulator_rev1 import FM_Demodulator_rev1  # grc-generated hier_block
from FM_Modulator_rev1 import FM_Modulator_rev1  # grc-generated hier_block
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, GrRangeWidget
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
        self.baudRate = baudRate = 9600
        self.samplesPerSymbol = samplesPerSymbol = 80
        self.frequencyDeviation = frequencyDeviation = baudRate/2
        self.sampleRate = sampleRate = samplesPerSymbol * baudRate
        self.rfGain = rfGain = 10
        self.lowPassCutoff = lowPassCutoff = frequencyDeviation*2+600
        self.delay = delay = 0
        self.centerFrequency = centerFrequency = frequencyDeviation * 8
        self.TxFreq = TxFreq = 145.4E6

        ##################################################
        # Blocks
        ##################################################
        self._lowPassCutoff_range = Range(0, sampleRate /2 -100, 100, frequencyDeviation*2+600, 200)
        self._lowPassCutoff_win = GrRangeWidget(self._lowPassCutoff_range, self.set_lowPassCutoff, "low pass filter cuttof", "counter_slider", float, QtCore.Qt.Horizontal, "value")

        self.top_grid_layout.addWidget(self._lowPassCutoff_win, 3, 0, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._delay_range = Range(0, (8*32), 1, 0, 200)
        self._delay_win = GrRangeWidget(self._delay_range, self.set_delay, "delay", "counter_slider", int, QtCore.Qt.Horizontal, "value")

        self.top_grid_layout.addWidget(self._delay_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rfGain_range = Range(0, 100, 1, 10, 200)
        self._rfGain_win = GrRangeWidget(self._rfGain_range, self.set_rfGain, "rfGain", "counter_slider", int, QtCore.Qt.Horizontal, "value")

        self.top_layout.addWidget(self._rfGain_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            (8*32), #size
            sampleRate, #samp_rate
            "Tx vs Rx", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Demod Tx', 'Input Tx', 'Signal 3', 'Signal 4', 'Signal 5',
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
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            (8*samplesPerSymbol), #size
            sampleRate, #samp_rate
            "Modulated Carrier", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Post-Mod', 'FIle Binary', 'Signal 3', 'Signal 4', 'Signal 5',
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
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            sampleRate, #bw
            "post low pass", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            sampleRate, #bw
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
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1, [1], centerFrequency, sampleRate)
        self.fir_filter_xxx_0_0 = filter.fir_filter_fff(samplesPerSymbol, [1])
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.fileSource = blocks.file_source(gr.sizeof_char*1, 'C:\\Users\\ccraw\\Documents\\USST\\Ground Station\\ground_station\\examples\\SampleBinaryFiles\\pyramid_32B.bin', True, 0, 0)
        self.fileSource.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, delay)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-0.5))
        self.FM_Modulator_rev1_0 = FM_Modulator_rev1(
            baudRate=baudRate,
            frequencyDeviation=frequencyDeviation,
            samplesPerSymbol=samplesPerSymbol,
        )
        self.FM_Demodulator_rev1_0 = FM_Demodulator_rev1(
            baudRate=baudRate,
            frequencyDeviation=frequencyDeviation,
            lowPassCutoff=lowPassCutoff,
            samplesPerSymbol=samplesPerSymbol,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.FM_Demodulator_rev1_0, 1), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.FM_Demodulator_rev1_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.FM_Modulator_rev1_0, 1), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.FM_Modulator_rev1_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.FM_Modulator_rev1_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.FM_Modulator_rev1_0, 1), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_time_sink_x_1, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.fileSource, 0), (self.FM_Modulator_rev1_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.FM_Demodulator_rev1_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FSK_testing")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_baudRate(self):
        return self.baudRate

    def set_baudRate(self, baudRate):
        self.baudRate = baudRate
        self.set_frequencyDeviation(self.baudRate/2)
        self.set_sampleRate(self.samplesPerSymbol * self.baudRate)
        self.FM_Demodulator_rev1_0.set_baudRate(self.baudRate)
        self.FM_Modulator_rev1_0.set_baudRate(self.baudRate)

    def get_samplesPerSymbol(self):
        return self.samplesPerSymbol

    def set_samplesPerSymbol(self, samplesPerSymbol):
        self.samplesPerSymbol = samplesPerSymbol
        self.set_sampleRate(self.samplesPerSymbol * self.baudRate)
        self.FM_Demodulator_rev1_0.set_samplesPerSymbol(self.samplesPerSymbol)
        self.FM_Modulator_rev1_0.set_samplesPerSymbol(self.samplesPerSymbol)

    def get_frequencyDeviation(self):
        return self.frequencyDeviation

    def set_frequencyDeviation(self, frequencyDeviation):
        self.frequencyDeviation = frequencyDeviation
        self.set_centerFrequency(self.frequencyDeviation * 8)
        self.set_lowPassCutoff(self.frequencyDeviation*2+600)
        self.FM_Demodulator_rev1_0.set_frequencyDeviation(self.frequencyDeviation)
        self.FM_Modulator_rev1_0.set_frequencyDeviation(self.frequencyDeviation)

    def get_sampleRate(self):
        return self.sampleRate

    def set_sampleRate(self, sampleRate):
        self.sampleRate = sampleRate
        self.qtgui_sink_x_0.set_frequency_range(0, self.sampleRate)
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.sampleRate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.sampleRate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.sampleRate)

    def get_rfGain(self):
        return self.rfGain

    def set_rfGain(self, rfGain):
        self.rfGain = rfGain

    def get_lowPassCutoff(self):
        return self.lowPassCutoff

    def set_lowPassCutoff(self, lowPassCutoff):
        self.lowPassCutoff = lowPassCutoff
        self.FM_Demodulator_rev1_0.set_lowPassCutoff(self.lowPassCutoff)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(self.delay)

    def get_centerFrequency(self):
        return self.centerFrequency

    def set_centerFrequency(self, centerFrequency):
        self.centerFrequency = centerFrequency
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.centerFrequency)

    def get_TxFreq(self):
        return self.TxFreq

    def set_TxFreq(self, TxFreq):
        self.TxFreq = TxFreq




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
