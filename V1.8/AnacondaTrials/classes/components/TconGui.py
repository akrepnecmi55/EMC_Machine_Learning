# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import * 
from classes.settings import Settings as st
from classes.db.TconDatabase import TconDatabase as tconDb

class TconGui():
    def __init__(self):
        mbTk = tk.Tk()
        mbTk.title("mainboard configuration")
        mbF = tk.Frame(mbTk)
        self.inputCheck = False
        self.screwCheck = False
        self.conCheck = False

        tk.Label(mbTk, text="code").grid(row = 1, column = 1)
        tk.Label(mbTk, text="version").grid(row = 2, column = 1)
        tk.Label(mbTk, text="x Size (cm)").grid(row = 3, column = 1)
        tk.Label(mbTk, text="y Size (cm)").grid(row = 4, column = 1)
        tk.Label(mbTk, text="screw Coordinates").grid(row = 5, column = 1)
        tk.Label(mbTk, text="connector Coordinates").grid(row = 6, column = 1)
        
        self.codeEnt = tk.Entry(mbTk)
        self.versionEnt = tk.Entry(mbTk)
        self.xSizeEnt = tk.Entry(mbTk)
        self.ySizeEnt = tk.Entry(mbTk)

        self.codeEnt.grid(row = 1, column = 2)
        self.versionEnt.grid(row = 2, column = 2)
        self.xSizeEnt.grid(row = 3, column = 2)
        self.ySizeEnt.grid(row = 4, column = 2)
##        self.screwCo = tk.Entry(mbTk)
##        self.code = tk.Entry(mbTk)
        self.screwCo = []
        self.conCo = []
##        self.conList = ['LVDS','VBY1','WIFI','DC','AC','FPC']
        self.mbConList = []
        self.selB = 0
        self.cm = st.tConCm
        
        tk.Button(mbTk, text="chose locations", command = lambda: self.locateScrews()).grid(row = 5, column = 2)
        tk.Button(mbTk, text="chose locations", command = lambda: self.locateCons()).grid(row = 6, column = 2)

        tk.Button(mbTk, text="Save", command = lambda: self.save()).grid(row = 8, column = 1)
        
        
        self.mbTk = mbTk

        
    def getSizes(self):
        self.xS = int(float(self.xSizeEnt.get()))
        self.yS = int(float(self.ySizeEnt.get()))
        self.code = self.codeEnt.get()
        self.version = self.versionEnt.get()
        print("x,y sizes:", self.xS , self.yS)
        
    def save(self):
        self.getSizes()
        obj = tconDb()
        obj.addTcon(self)
        obj.showSome()
        del obj

    def locateScrews(self):
        self.getSizes()
        self.selB = 1
        mbSc = tk.Tk()
        mbSc.title("Select Screw locations on the board")
        mbScFrCv = tk.Canvas(mbSc, width= self.cm*self.xS+2*self.cm, height = self.cm*self.yS+2*self.cm, background = 'white')
        mbScFrCv.grid()
        self.mbScFrCv = mbScFrCv
        mbScFrCv.create_rectangle(self.cm, self.cm, (self.xS+1)*self.cm, (self.yS+1)*self.cm, width=3)
        mbScFrCv.create_text(self.cm*(self.xS/2+1),self.cm*(self.yS/2+1), text = 'T-Con', angle=0)
        self.cc = 0
        self.sc = 0 
        self.mbScFrCv.bind('<Button-1>', self.mbClk)
        self.mbScFrCv.bind('<Motion>', self.mbM)
        self.mbScFrCv.bind('<Button-3>', self.mbRclk)

    def locateCons(self):
        self.getSizes()
        self.selB = 2
        mbCn = tk.Tk()
        mbCn.title("Select Conn locations on the board press Space and Rclick for locating")
        mbCnFrCv = tk.Canvas(mbCn, width= self.cm*self.xS+2*self.cm, height = self.cm*self.yS+2*self.cm, background = 'white')
        mbCnFrCv.grid()
        self.mbCnFrCv = mbCnFrCv
        mbCnFrCv.create_rectangle(self.cm, self.cm, (self.xS+1)*self.cm, (self.yS+1)*self.cm, width=3)
        mbCnFrCv.create_text(self.cm*(self.xS/2+1),self.cm*(self.yS/2+1), text = 'T-Con', angle=0)
        for ev in self.screwCo:
            self.mbCnFrCv.create_rectangle(ev[0]-3,ev[1]-3,ev[0]+3,ev[1]+3, width=2, fill="green")
        self.conInt = 0
        self.conC = 0
##        self.sc = 0 
        self.mbCnFrCv.bind('<Button-1>', self.mbClk)
        self.mbCnFrCv.bind('<Motion>', self.mbM)
        self.mbCnFrCv.bind('<Button-3>', self.mbRclk)
        mbCn.bind('<space>', self.mbSpc)
        
    def mbClk(self, event):
        ev = [event.x,event.y]
        if self.selB == 1:
            self.mbScFrCv.delete("temp")
            if self.cc == 0:
                self.mbScFrCv.create_rectangle(ev[0]-3,ev[1]-3,ev[0]+3,ev[1]+3, width=2, fill="blue", tags="temp")
            elif self.cc == 1:
                self.sc += 1
                self.mbScFrCv.create_rectangle(ev[0]-3,ev[1]-3,ev[0]+3,ev[1]+3, width=2, fill="green", tags='screw' + str(self.sc))
                print(str(self.sc))
                self.screwCo.append(ev)
            self.cc = (self.cc + 1)%2
            print(self.screwCo)
        if self.selB == 2:
            self.mbCnFrCv.delete("temp")
            self.mbCnFrCv.create_oval(ev[0]-10,ev[1]-10,ev[0]+10,ev[1]+10, width=2, fill="red", tags= str(self.conC) + 'con' )
            self.mbCnFrCv.create_text(ev[0],ev[1], text = st.conList[self.conInt], angle=0, tags= str(self.conC) + 'con' )
##            self.conCo.append([ev, self.conInt])
            self.conCo.append([ev, st.conList[self.conInt]])
            self.conC += 1
            print(self.conCo)
            print(self.conC)
            
    def mbM(self, event):
        ev = [event.x,event.y]
        if self.selB == 1:
            if self.cc == 1:
                self.mbScFrCv.delete("temp")
                self.mbScFrCv.create_rectangle(ev[0]-3,ev[1]-3,ev[0]+3,ev[1]+3,width=2, fill="blue", tags="temp")
        if self.selB == 2:
            self.mbCnFrCv.delete("temp")
            self.mbCnFrCv.create_oval(ev[0]-10,ev[1]-10,ev[0]+10,ev[1]+10, width=2, fill="red", tags= "temp")
            self.mbCnFrCv.create_text(ev[0],ev[1], text = st.conList[self.conInt], angle=0, tags= "temp")
    def mbRclk(self, event):
        if self.selB == 1:
            self.mbScFrCv.delete("temp")
            if self.cc == 0 and self.sc > 0:
                self.mbScFrCv.delete('screw' + str(self.sc))
                self.screwCo.pop()
                self.sc -= 1
            print(self.screwCo)
        if self.selB == 2:
            self.mbCnFrCv.delete("temp")
            if self.conC > 0:
                try:
                    self.conC -= 1
                    print("conC is", self.conC)
                    self.mbCnFrCv.delete(str(self.conC) + 'con')
                    self.conCo.pop()
                except:
                    print("olamadı")
                
    def mbSpc(self, event):
        ev = [event.x,event.y]
        print("space e girdi!")
        if self.selB == 2:
            self.conInt = (self.conInt + 1)%len(st.conList)
            print("conn no is: ", self.conInt)
            self.mbCnFrCv.delete("temp")
            self.mbCnFrCv.create_oval(ev[0]-10,ev[1]-10,ev[0]+10,ev[1]+10, width=2, fill="red", tags= "temp")
            self.mbCnFrCv.create_text(ev[0],ev[1], text = st.conList[self.conInt], angle=0, tags= "temp")
        

if __name__ == "__main__":
    app = SampleApp()
    
    app.mainloop()
