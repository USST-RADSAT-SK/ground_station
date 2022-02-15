#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RFMReceiver
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
from gnuradio import audio
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

class RFMReceiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RFMReceiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RFMReceiver")
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
        self.volume = volume = 1
        self.rfSampleRate = rfSampleRate = audioSampleRate * 25
        self.rfGain = rfGain = 50
        self.frequency = frequency = 95.1e6

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 2, 0.1, 1, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, 'Volume', "counter_slider", float)
        self.top_grid_layout.addWidget(self._volume_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rfGain_range = Range(0, 70, 1, 50, 200)
        self._rfGain_win = RangeWidget(self._rfGain_range, self.set_rfGain, 'Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rfGain_win, 2, 0, 1, 2)
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
        self._frequency_range = Range(50e6, 1.6e9, 0.025e6, 95.1e6, 200)
        self._frequency_win = RangeWidget(self._frequency_range, self.set_frequency, 'Frequency', "counter", float)
        self.top_grid_layout.addWidget(self._frequency_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            audioSampleRate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(1/20)
        self.qtgui_time_sink_x_0.set_y_axis(-1.2, 1.2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_0.disable_legend()

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
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.mainTabs_layout_1.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_1 = qtgui.sink_c(
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
        self.qtgui_sink_x_1.set_update_time(1.0/20)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(True)

        self.mainTabs_layout_0.addWidget(self._qtgui_sink_x_1_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                rfSampleRate,
                100e3,
                10e3,
                firdes.WIN_HAMMING,
                6.76))
        self.limesdr_source_0 = limesdr.source('1D538ACAE2BD00', 0, '')


        self.limesdr_source_0.set_sample_rate(rfSampleRate)


        self.limesdr_source_0.set_center_freq(frequency, 0)

        self.limesdr_source_0.set_bandwidth(1.5e6, 0)


        self.limesdr_source_0.set_digital_filter(1e6, 0)


        self.limesdr_source_0.set_gain(rfGain, 0)


        self.limesdr_source_0.set_antenna(255, 0)


        self.limesdr_source_0.calibrate(2.5e6, 0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume)
        self.audio_sink_0 = audio.sink(audioSampleRate, '', False)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=rfSampleRate,
        	audio_decimation=rfSampleRate // audioSampleRate,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.limesdr_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.limesdr_source_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "RFMReceiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_audioSampleRate(self):
        return self.audioSampleRate

    def set_audioSampleRate(self, audioSampleRate):
        self.audioSampleRate = audioSampleRate
        self.set_rfSampleRate(self.audioSampleRate * 25)
        self.qtgui_time_sink_x_0.set_samp_rate(self.audioSampleRate)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume)

    def get_rfSampleRate(self):
        return self.rfSampleRate

    def set_rfSampleRate(self, rfSampleRate):
        self.rfSampleRate = rfSampleRate
        self.limesdr_source_0.set_digital_filter(self.rfSampleRate, 1)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.rfSampleRate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_1.set_frequency_range(self.frequency, self.rfSampleRate)

    def get_rfGain(self):
        return self.rfGain

    def set_rfGain(self, rfGain):
        self.rfGain = rfGain
        self.limesdr_source_0.set_gain(self.rfGain, 0)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.limesdr_source_0.set_center_freq(self.frequency, 0)
        self.qtgui_sink_x_1.set_frequency_range(self.frequency, self.rfSampleRate)





def main(top_block_cls=RFMReceiver, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

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
