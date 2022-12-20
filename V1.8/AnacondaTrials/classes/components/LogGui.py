# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import *
import numpy as np
from classes.settings import Settings as st
from pathlib import Path
import shelve
import threading as th
from threading import Thread
from time import *

class MetaLogger(type):
    @property
    def logTxt(cls):
        return cls.logText

    @logTxt.setter
    def logTxt(cls, txt):
        cls.logText = txt


class LogGui(object, metaclass = MetaLogger):
    
    def __init__(self, master):
        logCn = tk.Canvas(master, width= master.winfo_width(), height = master.winfo_height(), background = 'white')
        self.logCn = logCn
        self.logCn.grid()
        self.logText = "Logs"
        master.update_idletasks() 
        print("master.winfo_width()", master.winfo_width())
        self.logLabel = tk.Label(self.logCn, text=self.logText, wraplength=master.winfo_width(), justify="left")
        self.logLabel.grid(sticky="nsew")
        
    @property
    def logTxt(self):
        return type(self).logTxt

    def updateLbl(self, txt):
        self.logLabel.configure(text = "->" + txt)
        
    def addTxtDown(self, *txt):
        # pass
        tempTxt = self.logLabel.cget("text")
        addTxt = ""
        for i in txt:
            if i[-1] == " ":
                if i[0] == " ":
                    addTxt += i[1:]
                else:
                    addTxt += i
            else:
                if i[0] == " ":
                    addTxt += i[1:] + " "
                else:
                    addTxt += i + " "
                
        self.logLabel.configure(text = tempTxt + "\n ->" + addTxt)

        
    def addTxtUp(self, *txt):
        # pass
        tempTxt = self.logLabel.cget("text")
        addTxt = ""
        for i in txt:
            if i[-1] == " ":
                if i[0] == " ":
                    addTxt += i[1:]
                else:
                    addTxt += i
            else:
                if i[0] == " ":
                    addTxt += i[1:] + " "
                else:
                    addTxt += i + " "
                
        self.logLabel.configure(text = "->" + addTxt + "\n" + tempTxt)
        
    def clrLog(self):
        self.logLabel.configure(text = "...")
        
if __name__ == "__main__":
    app = SampleApp()
    
    app.mainloop()
