#!/usr/bin/env bash
add-apt-repository ppa:ettusresearch/uhd
apt-get update
apt-get install -y git gnuradio gr-osmosdr gr-satellites libuhd-dev libuhd4.1.0 uhd-host
uhd_images_downloader


