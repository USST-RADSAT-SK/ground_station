#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: NFM_rcv
# Author: Barry Duggan
# Description: NB FM receiver
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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import NFM_rcv_epy_block_0 as epy_block_0  # embedded python block



from gnuradio import qtgui

class NFM_rcv(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NFM_rcv", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NFM_rcv")
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

        self.settings = Qt.QSettings("GNU Radio", "NFM_rcv")

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
        self.samp_rate = samp_rate = 576000
        self.volume = volume = 0.05
        self.sq_lvl = sq_lvl = -50
        self.rxGain = rxGain = 0
        self.rxBaseband = rxBaseband = 437.8e6
        self.rf_decim = rf_decim = 3
        self.channel_filter = channel_filter = firdes.complex_band_pass(1.0, samp_rate, -3000, 3000, 200, window.WIN_BLACKMAN, 6.76)

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 1.00, 0.05, 0.05, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, "Volume", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._volume_win)
        self._sq_lvl_range = Range(-100, 0, 5, -50, 200)
        self._sq_lvl_win = RangeWidget(self._sq_lvl_range, self.set_sq_lvl, "Squelch", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sq_lvl_win)
        self._rxGain_range = Range(0, 100, 1, 0, 200)
        self._rxGain_win = RangeWidget(self._rxGain_range, self.set_rxGain, "Rx Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rxGain_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("serial=31E34AD", 'name=MyB210,product=B210')),
            uhd.stream_args(
                cpu_format="fc32",
                args='peak=0.003906',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(rxBaseband, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(rxGain, 0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.fft_filter_xxx_0_0 = filter.fft_filter_ccc(rf_decim, channel_filter, 1)
        self.fft_filter_xxx_0_0.declare_sample_delay(0)
        self.epy_block_0 = epy_block_0.blk(upBaseFreq=rxBaseband, dnBaseFreq=rxBaseband, gsLat=52.144176, gsLon=-106.61291, noradId=25544)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(volume)
        self.blocks_msgpair_to_var_1 = blocks.msg_pair_to_var(self.set_rxBaseband)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 1000)
        self.audio_sink_0 = audio.sink(48000, '', False)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(sq_lvl, 1)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=(int)(samp_rate/rf_decim),
        	tau=75e-6,
        	max_dev=5e3,
          )


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.epy_block_0, 'update_msg'))
        self.msg_connect((self.epy_block_0, 'dnlk_freq_msg'), (self.blocks_msgpair_to_var_1, 'inpair'))
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.audio_sink_0, 0))
        self.connect((self.fft_filter_xxx_0_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.fft_filter_xxx_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NFM_rcv")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_channel_filter(firdes.complex_band_pass(1.0, self.samp_rate, -3000, 3000, 200, window.WIN_BLACKMAN, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0_0.set_k(self.volume)

    def get_sq_lvl(self):
        return self.sq_lvl

    def set_sq_lvl(self, sq_lvl):
        self.sq_lvl = sq_lvl
        self.analog_simple_squelch_cc_0.set_threshold(self.sq_lvl)

    def get_rxGain(self):
        return self.rxGain

    def set_rxGain(self, rxGain):
        self.rxGain = rxGain
        self.uhd_usrp_source_0.set_gain(self.rxGain, 0)

    def get_rxBaseband(self):
        return self.rxBaseband

    def set_rxBaseband(self, rxBaseband):
        self.rxBaseband = rxBaseband
        self.uhd_usrp_source_0.set_center_freq(self.rxBaseband, 0)

    def get_rf_decim(self):
        return self.rf_decim

    def set_rf_decim(self, rf_decim):
        self.rf_decim = rf_decim

    def get_channel_filter(self):
        return self.channel_filter

    def set_channel_filter(self, channel_filter):
        self.channel_filter = channel_filter
        self.fft_filter_xxx_0_0.set_taps(self.channel_filter)




def main(top_block_cls=NFM_rcv, options=None):

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
