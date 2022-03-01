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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import filter
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
        self.sps = sps = 32
        self.baud = baud = 9600
        self.txgain = txgain = 10
        self.sens = sens = 1
        self.samp_rate = samp_rate = baud * sps
        self.modGain = modGain = 2
        self.isps = isps = sps
        self.isamp = isamp = baud
        self.freqError = freqError = 100
        self.freqDeviation = freqDeviation = 4800
        self.freq = freq = 107.1e6

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
        self._modGain_range = Range(0, 5, 0.1, 2, 200)
        self._modGain_win = RangeWidget(self._modGain_range, self.set_modGain, 'Mod Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._modGain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1_0_0_1_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            3 #number of inputs
        )
        self.qtgui_time_sink_x_0_1_0_0_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1_0_0_1_0.set_y_axis(-1.2, 1.2)

        self.qtgui_time_sink_x_0_1_0_0_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1_0_0_1_0.enable_tags(True)
        self.qtgui_time_sink_x_0_1_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1_0_0_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1_0_0_1_0.enable_grid(True)
        self.qtgui_time_sink_x_0_1_0_0_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1_0_0_1_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_1_0_0_1_0.enable_stem_plot(False)


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
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_0_0_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_0_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_0_0_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_0_0_1_0.pyqwidget(), Qt.QWidget)
        self.tabs_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_1_0_0_1_0_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.tabs_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1_0_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
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
            samp_rate, #bw
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


        self.limesdr_sink_0_0.set_sample_rate(samp_rate)


        self.limesdr_sink_0_0.set_center_freq(freq, 0)



        self.limesdr_sink_0_0.set_digital_filter(freqDeviation * 2, 0)


        self.limesdr_sink_0_0.set_gain(txgain, 0)


        self.limesdr_sink_0_0.set_antenna(255, 0)


        self.limesdr_sink_0_0.calibrate(2.5e6, 0)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1, firdes.low_pass(1, isamp * isps,(2 * isamp * sens - isamp * sens)/2+400, 300 ), (2 * isamp * sens + isamp * sens)/2, samp_rate)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, isps)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(-1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(modGain)
        self.blocks_delay_2 = blocks.delay(gr.sizeof_float*1, 0)
        self.blocks_delay_1 = blocks.delay(gr.sizeof_float*1, 0)
        self.blocks_char_to_float_1 = blocks.char_to_float(1, 1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(isamp * isps, analog.GR_COS_WAVE, isamp / sens, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(isamp * isps, analog.GR_COS_WAVE, 2*isamp /sens, 1, 0, 0)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 16))), True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_time_sink_x_0_1_0_0_1_0, 0))
        self.connect((self.blocks_char_to_float_1, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.qtgui_time_sink_x_0_1_0_0_1_0, 1))
        self.connect((self.blocks_delay_2, 0), (self.qtgui_time_sink_x_0_1_0_0_1_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.limesdr_sink_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0_1_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_delay_1, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_delay_2, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FSKTransmitter")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_isps(self.sps)
        self.set_samp_rate(self.baud * self.sps)

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_isamp(self.baud)
        self.set_samp_rate(self.baud * self.sps)

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.limesdr_sink_0_0.set_gain(self.txgain, 0)

    def get_sens(self):
        return self.sens

    def set_sens(self, sens):
        self.sens = sens
        self.analog_sig_source_x_0.set_frequency(2*self.isamp /self.sens)
        self.analog_sig_source_x_0_0.set_frequency(self.isamp / self.sens)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.isamp * self.isps,(2 * self.isamp * self.sens - self.isamp * self.sens)/2+400, 300 ))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((2 * self.isamp * self.sens + self.isamp * self.sens)/2)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0_1_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_1_0_0_1_0.set_samp_rate(self.samp_rate)

    def get_modGain(self):
        return self.modGain

    def set_modGain(self, modGain):
        self.modGain = modGain
        self.blocks_multiply_const_vxx_0.set_k(self.modGain)

    def get_isps(self):
        return self.isps

    def set_isps(self, isps):
        self.isps = isps
        self.analog_sig_source_x_0.set_sampling_freq(self.isamp * self.isps)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.isamp * self.isps)
        self.blocks_repeat_0.set_interpolation(self.isps)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.isamp * self.isps,(2 * self.isamp * self.sens - self.isamp * self.sens)/2+400, 300 ))

    def get_isamp(self):
        return self.isamp

    def set_isamp(self, isamp):
        self.isamp = isamp
        self.analog_sig_source_x_0.set_sampling_freq(self.isamp * self.isps)
        self.analog_sig_source_x_0.set_frequency(2*self.isamp /self.sens)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.isamp * self.isps)
        self.analog_sig_source_x_0_0.set_frequency(self.isamp / self.sens)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.isamp * self.isps,(2 * self.isamp * self.sens - self.isamp * self.sens)/2+400, 300 ))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((2 * self.isamp * self.sens + self.isamp * self.sens)/2)

    def get_freqError(self):
        return self.freqError

    def set_freqError(self, freqError):
        self.freqError = freqError

    def get_freqDeviation(self):
        return self.freqDeviation

    def set_freqDeviation(self, freqDeviation):
        self.freqDeviation = freqDeviation
        self.limesdr_sink_0_0.set_digital_filter(self.freqDeviation * 2, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.limesdr_sink_0_0.set_center_freq(self.freq, 0)





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
