#!/bin/bash
python3 rotatorControl.py $1 &
python3 RRadsatRadioService.py $1 &
python3 TRxGUI.py &