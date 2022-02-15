#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RFMTransmitterProject
# Author: Austin
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
        gr.top_block.__init__(self, "RFMTransmitterProject")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RFMTransmitterProject")
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
        self.audioSampleRate = audioSampleRate = 44100
        self.rfSampleRate = rfSampleRate = int(audioSampleRate * 25)
        self.rfGain = rfGain = 50
        self.frequency = frequency = 107.1e6
        self.TransmitVolume = TransmitVolume = 1

        ##################################################
        # Blocks
        ##################################################
        self._rfGain_range = Range(0, 60, 1, 50, 200)
        self._rfGain_win = RangeWidget(self._rfGain_range, self.set_rfGain, 'Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rfGain_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._TransmitVolume_range = Range(0, 2, 0.1, 1, 200)
        self._TransmitVolume_win = RangeWidget(self._TransmitVolume_range, self.set_TransmitVolume, 'Volume', "counter_slider", float)
        self.top_grid_layout.addWidget(self._TransmitVolume_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            frequency, #fc
            rfSampleRate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            False, #plottime
            False #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/20)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(True)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_0_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.mainTabs = Qt.QTabWidget()
        self.mainTabs_widget_0 = Qt.QWidget()
        self.mainTabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.mainTabs_widget_0)
        self.mainTabs_grid_layout_0 = Qt.QGridLayout()
        self.mainTabs_layout_0.addLayout(self.mainTabs_grid_layout_0)
        self.mainTabs.addTab(self.mainTabs_widget_0, 'RF')
        self.mainTabs_widget_1 = Qt.QWidget()
        self.mainTabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.mainTabs_widget_1)
        self.mainTabs_grid_layout_1 = Qt.QGridLayout()
        self.mainTabs_layout_1.addLayout(self.mainTabs_grid_layout_1)
        self.mainTabs.addTab(self.mainTabs_widget_1, 'Audio')
        self.top_grid_layout.addWidget(self.mainTabs, 3, 0, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.limesdr_sink_0 = limesdr.sink('', 0, '', '')


        self.limesdr_sink_0.set_sample_rate(rfSampleRate)


        self.limesdr_sink_0.set_center_freq(frequency, 0)

        self.limesdr_sink_0.set_bandwidth(5e6, 0)


        self.limesdr_sink_0.set_digital_filter(rfSampleRate, 0)


        self.limesdr_sink_0.set_gain(rfGain, 0)


        self.limesdr_sink_0.set_antenna(255, 0)


        self.limesdr_sink_0.calibrate(2.5e6, 0)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('BrittleRilleByKevinMacLeod.wav', True)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_ff(TransmitVolume)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=audioSampleRate,
        	quad_rate=rfSampleRate,
        	tau=75e-6,
        	max_dev=75e3,
        	fh=-1.0,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_tx_0, 0), (self.limesdr_sink_0, 0))
        self.connect((self.analog_wfm_tx_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "RFMTransmitter")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_audioSampleRate(self):
        return self.audioSampleRate

    def set_audioSampleRate(self, audioSampleRate):
        self.audioSampleRate = audioSampleRate
        self.set_rfSampleRate(int(self.audioSampleRate * 25))

    def get_rfSampleRate(self):
        return self.rfSampleRate

    def set_rfSampleRate(self, rfSampleRate):
        self.rfSampleRate = rfSampleRate
        self.limesdr_sink_0.set_digital_filter(self.rfSampleRate, 0)
        self.limesdr_sink_0.set_digital_filter(self.rfSampleRate, 1)
        self.qtgui_sink_x_0_0.set_frequency_range(self.frequency, self.rfSampleRate)

    def get_rfGain(self):
        return self.rfGain

    def set_rfGain(self, rfGain):
        self.rfGain = rfGain
        self.limesdr_sink_0.set_gain(self.rfGain, 0)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.limesdr_sink_0.set_center_freq(self.frequency, 0)
        self.qtgui_sink_x_0_0.set_frequency_range(self.frequency, self.rfSampleRate)

    def get_TransmitVolume(self):
        return self.TransmitVolume

    def set_TransmitVolume(self, TransmitVolume):
        self.TransmitVolume = TransmitVolume
        self.blocks_multiply_const_vxx_0_1.set_k(self.TransmitVolume)





def main(top_block_cls=RFMTransmitter, options=None):

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
