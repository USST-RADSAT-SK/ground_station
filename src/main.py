import os

noradID = 25544

os.system('python3 rotatorControl.py')   
os.system('python3 TRxGUI.py')
os.system('python3 RRadsatRadioService.py')

"""
TODO:
    - Test TLE updating
    - Test this master script
    - Add arguments to each call (set noradID in this script and
      pass as input to other 3?)

"""

