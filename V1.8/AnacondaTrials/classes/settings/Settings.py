# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
from classes.components.Cable import *

def init():
    global conList
    global mbCm
    global ursaCm
    global tConCm
    global psuCm
    global panelCm
    global emiTapeList
    global ferList


    # do not put '-' in an where in or nearby to connector names. It will mess up the tag classification methods.
    # conList = ['LVDS','VBY1','MLVDS','WIFI','DC','AC','FPC','BT_ANT','WF_ANT','SPK']
    conList = ['LVDS','VBY1','MLVDS','WIFI','DC','AC','FPC','BT_ANT','WF_ANT','SPK', 'USB', 'HDMI', 'TER', 'SAT','TER&SAT']
    # 5cm * 1cm = [5,1]
    emiTapeList = [ [5,1], [5,5], [7,1] ]
    ferList = [ [2,3], [1,3] ]


    mbCm = 30
    ursaCm = 30
    tConCm = 30
    psuCm = 30
    panelCm = 10


if __name__ == "__main__":
    app = SampleApp()

    app.mainloop()
