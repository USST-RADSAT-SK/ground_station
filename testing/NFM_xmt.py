#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: NFM_xmt
# Author: Not Barry Duggan :)
# Description: NBFM transmitter
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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
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



from gnuradio import qtgui

class NFM_xmt(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NFM_xmt", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NFM_xmt")
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

        self.settings = Qt.QSettings("GNU Radio", "NFM_xmt")

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
        self.usrp_rate = usrp_rate = 576000
        self.volume = volume = 5.0
        self.txGain = txGain = 0
        self.txBaseband = txBaseband = 145.99E6
        self.samp_rate = samp_rate = 48000
        self.pl_freq = pl_freq = 0.0
        self.if_rate = if_rate = int(usrp_rate/2)
        self.PTT = PTT = 0

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 10.0, 0.1, 5.0, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, "Audio gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._volume_win)
        self._txGain_range = Range(0, 65, 1, 0, 200)
        self._txGain_win = RangeWidget(self._txGain_range, self.set_txGain, "Tx Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._txGain_win)
        # Create the options list
        self._pl_freq_options = [0.0, 67.0, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5, 94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3, 131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 162.2, 167.9, 173.8, 179.9, 186.2, 192.8, 203.5, 210.7, 218.1, 225.7, 233.6, 241.8, 250.3]
        # Create the labels list
        self._pl_freq_labels = ['0.0', '67.0', '71.9', '74.4', '77.0', '79.7', '82.5', '85.4', '88.5', '91.5', '94.8', '97.4', '100.0', '103.5', '107.2', '110.9', '114.8', '118.8', '123.0', '127.3', '131.8', '136.5', '141.3', '146.2', '151.4', '156.7', '162.2', '167.9', '173.8', '179.9', '186.2', '192.8', '203.5', '210.7', '218.1', '225.7', '233.6', '241.8', '250.3']
        # Create the combo box
        self._pl_freq_tool_bar = Qt.QToolBar(self)
        self._pl_freq_tool_bar.addWidget(Qt.QLabel("PL Tone" + ": "))
        self._pl_freq_combo_box = Qt.QComboBox()
        self._pl_freq_tool_bar.addWidget(self._pl_freq_combo_box)
        for _label in self._pl_freq_labels: self._pl_freq_combo_box.addItem(_label)
        self._pl_freq_callback = lambda i: Qt.QMetaObject.invokeMethod(self._pl_freq_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._pl_freq_options.index(i)))
        self._pl_freq_callback(self.pl_freq)
        self._pl_freq_combo_box.currentIndexChanged.connect(
            lambda i: self.set_pl_freq(self._pl_freq_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._pl_freq_tool_bar)
        _PTT_check_box = Qt.QCheckBox("'PTT'")
        self._PTT_choices = {True: 1, False: 0}
        self._PTT_choices_inv = dict((v,k) for k,v in self._PTT_choices.items())
        self._PTT_callback = lambda i: Qt.QMetaObject.invokeMethod(_PTT_check_box, "setChecked", Qt.Q_ARG("bool", self._PTT_choices_inv[i]))
        self._PTT_callback(self.PTT)
        _PTT_check_box.stateChanged.connect(lambda i: self.set_PTT(self._PTT_choices[bool(i)]))
        self.top_layout.addWidget(_PTT_check_box)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("serial=31E34AD", 'name=MyB210,product=B210')),
            uhd.stream_args(
                cpu_format="fc32",
                args='peak=0.003906',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_samp_rate(if_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(txBaseband, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(txGain, 0)
        self.uhd_usrp_sink_0.set_max_output_buffer(255)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            if_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                if_rate,
                5000,
                2000,
                window.WIN_BLACKMAN,
                6.76))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume*PTT)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                300,
                5000,
                200,
                window.WIN_BLACKMAN,
                6.76))
        self.audio_source_0 = audio.source(48000, '', False)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, pl_freq, 0.15, 0, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=if_rate,
        	tau=75e-6,
        	max_dev=5e3,
        	fh=-1.0,
                )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_tx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.audio_source_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.uhd_usrp_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NFM_xmt")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.set_if_rate(int(self.usrp_rate/2))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume*self.PTT)

    def get_txGain(self):
        return self.txGain

    def set_txGain(self, txGain):
        self.txGain = txGain
        self.uhd_usrp_sink_0.set_gain(self.txGain, 0)

    def get_txBaseband(self):
        return self.txBaseband

    def set_txBaseband(self, txBaseband):
        self.txBaseband = txBaseband
        self.uhd_usrp_sink_0.set_center_freq(self.txBaseband, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, 300, 5000, 200, window.WIN_BLACKMAN, 6.76))

    def get_pl_freq(self):
        return self.pl_freq

    def set_pl_freq(self, pl_freq):
        self.pl_freq = pl_freq
        self._pl_freq_callback(self.pl_freq)
        self.analog_sig_source_x_0.set_frequency(self.pl_freq)

    def get_if_rate(self):
        return self.if_rate

    def set_if_rate(self, if_rate):
        self.if_rate = if_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.if_rate, 5000, 2000, window.WIN_BLACKMAN, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.if_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.if_rate)

    def get_PTT(self):
        return self.PTT

    def set_PTT(self, PTT):
        self.PTT = PTT
        self._PTT_callback(self.PTT)
        self.blocks_multiply_const_vxx_0.set_k(self.volume*self.PTT)




def main(top_block_cls=NFM_xmt, options=None):

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
