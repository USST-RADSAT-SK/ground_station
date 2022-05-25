#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GMSK
# GNU Radio version: 3.8.5.0

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
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget

from gnuradio import qtgui

class gmsk(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "GMSK")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GMSK")
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

        self.settings = Qt.QSettings("GNU Radio", "gmsk")

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
        self.baud = baud = 9600
        self.samp_rate = samp_rate = baud * samplesPerSymbol
        self.variable_1 = variable_1 = 0
        self.t1 = t1 = firdes.gaussian(1, samp_rate, baud/2, samplesPerSymbol)
        self.symbolRate = symbolRate = baud
        self.delay = delay = 0
        self.BT = BT = 0.30

        ##################################################
        # Blocks
        ##################################################
        self._delay_range = Range(-32*8, 32*8, 1, 0, 200)
        self._delay_win = RangeWidget(self._delay_range, self.set_delay, 'delay', "counter_slider", float)
        self.top_layout.addWidget(self._delay_win)
        self.qtgui_time_sink_x_1_0_0 = qtgui.time_sink_f(
            32*8*samplesPerSymbol, #size
            samplesPerSymbol, #samp_rate
            "", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0.set_y_axis(-0.1, 1.1)

        self.qtgui_time_sink_x_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0_0.enable_stem_plot(True)


        labels = ['0.5', '1.0', '2.0', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [0.33, 0.33, 0.33, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_0_win)
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_f(
            32*8*2*samplesPerSymbol, #size
            samplesPerSymbol, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0.set_y_axis(-0.1, 1.1)

        self.qtgui_time_sink_x_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0.enable_stem_plot(True)


        labels = ['After Demod', 'Difference', 'Before Mod', 'Signal 4', 'Signal 5',
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
                self.qtgui_time_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            32*8*2, #size
            samp_rate, #samp_rate
            "", #name
            3 #number of inputs
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
        self.qtgui_time_sink_x_1.enable_stem_plot(True)


        labels = ['After Demod', 'Difference', 'Before Mod', 'Signal 4', 'Signal 5',
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


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_sink_x_0_0 = qtgui.sink_f(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samplesPerSymbol, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            9600, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/samplesPerSymbol)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(1, [0.010465437546372414,0.012803290039300919,0.015447097830474377,0.018379483371973038,0.02156655490398407,0.024956824257969856,0.028481246903538704,0.03205455467104912,0.03557800129055977,0.03894345462322235,0.04203862324357033,0.04475314915180206,0.04698506370186806,0.048647113144397736,0.049672432243824005,0.05001898854970932,0.049672432243824005,0.048647113144397736,0.04698506370186806,0.04475314915180206,0.04203862324357033,0.03894345462322235,0.03557800129055977,0.03205455467104912,0.028481246903538704,0.024956824257969856,0.02156655490398407,0.018379483371973038,0.015447097830474377,0.012803290039300919,0.010465437546372414,0.008436343632638454])
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
            samples_per_symbol=samplesPerSymbol,
            bt=300e-3,
            verbose=False,
            log=False)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=samplesPerSymbol,
            gain_mu=0.175,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,log=False)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, samplesPerSymbol)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(-1)
        self.blocks_head_1 = blocks.head(gr.sizeof_char*1, 64)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/radsat-gs/ground_station/examples/SampleBinaryFiles/alternating_bits.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, delay)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff(0.05)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(0.05)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_head_1, 0))
        self.connect((self.blocks_head_1, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_head_1, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_1, 2))
        self.connect((self.blocks_repeat_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.qtgui_time_sink_x_1_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.qtgui_time_sink_x_1_0_0, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.qtgui_time_sink_x_1, 1))
        self.connect((self.blocks_throttle_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_1_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gmsk")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samplesPerSymbol(self):
        return self.samplesPerSymbol

    def set_samplesPerSymbol(self, samplesPerSymbol):
        self.samplesPerSymbol = samplesPerSymbol
        self.set_samp_rate(self.baud * self.samplesPerSymbol)
        self.set_t1(firdes.gaussian(1, self.samp_rate, self.baud/2, self.samplesPerSymbol))
        self.blocks_repeat_0.set_interpolation(self.samplesPerSymbol)
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samplesPerSymbol)
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samplesPerSymbol)
        self.qtgui_time_sink_x_1_0_0.set_samp_rate(self.samplesPerSymbol)

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_samp_rate(self.baud * self.samplesPerSymbol)
        self.set_symbolRate(self.baud)
        self.set_t1(firdes.gaussian(1, self.samp_rate, self.baud/2, self.samplesPerSymbol))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_t1(firdes.gaussian(1, self.samp_rate, self.baud/2, self.samplesPerSymbol))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_variable_1(self):
        return self.variable_1

    def set_variable_1(self, variable_1):
        self.variable_1 = variable_1

    def get_t1(self):
        return self.t1

    def set_t1(self, t1):
        self.t1 = t1

    def get_symbolRate(self):
        return self.symbolRate

    def set_symbolRate(self, symbolRate):
        self.symbolRate = symbolRate

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(self.delay)

    def get_BT(self):
        return self.BT

    def set_BT(self, BT):
        self.BT = BT





def main(top_block_cls=gmsk, options=None):

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
