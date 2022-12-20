# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import * 
import math 
from PIL import Image, ImageTk
from classes.settings import Settings as st

class FlatCable():
    # def __init__(self):
    def __init__(self, rx):
        self.cblObj = None
        self.cblObjSet = []
        self.cblCords = []
        self.setNum = 0
        self.clkOnce = False
        self.wdtUpd = False
        self.imagesTk = []
        self.imagesCv = []
        self.images = []
        self.trnsLst = []
        self.trprns = False
        self.root = rx
        self.img = None
        # self.image = None
        
    def crtIm(self, width, length, rot, color, canvas, x1, y1):
        colorX = self.root.winfo_rgb(color) + (55,)
        colorY = self.root.winfo_rgb('#AAAAAA') + (55,)
        colorZ = (int(color[1:3],16),int(color[3:5],16),int(color[5:7],16),55)
        # colorZ = (200,10,120,135)
        print("color: ", color, " colorX: ", colorX)
        print("color: ", color, " colorY: ", colorY)
        print("color: ", color, " colorZ: ", colorZ)
        print("rot: ", rot)
        try: 
            # self.images.append(Image.new('RGBA', (int(width), int(length)), colorX))
            # self.images.append((Image.new('RGBA', (int(width), int(length)), colorZ)).rotate(rot))
            self.images.append(Image.new('RGBA', (int(width), int(length)), colorZ))
            # self.images[-1].rotate(rot)
        except:
            print("bunu yapamadı zaten")

        # self.image = ImageTk.PhotoImage(self.images[-1])
        # self.imagesTk.append(ImageTk.PhotoImage(self.images[-1]))
        self.imagesTk.append(ImageTk.PhotoImage(self.images[-1].rotate(rot, expand=True)))
        # self.imagesTk.append(self.image)
        self.imagesCv.append(canvas.create_image(x1, y1, image=self.imagesTk[-1], anchor='nw'))
        # canvas.update()
        
    def drawFPC(self, canvas, ev_Start, ev_Stop, width, color):
        yDiff = (ev_Stop[1]-ev_Start[1])
        xDiff = (ev_Stop[0]-ev_Start[0])
        self.clrFPC(canvas)
        self.clkOnce = False
        if not self.cblCords:
            self.cblCords.append(ev_Start)
        if xDiff != 0.0:
            tanj = yDiff/xDiff
        else:
            tanj = yDiff/0.0001
            
        if not self.wdtUpd:
            if self.trprns:
                self.trnsLst.append(True)  #If transparent it is true
            else:
                self.trnsLst.append(False)  #If not False, track transparency of the coordinates here
            
        ff = lambda: "" if self.trprns else color 
            
        if abs(tanj) < 0.57:
            y = ev_Start[1]
            p1 = [ev_Start[0],y-width/2,ev_Start[0],y+width/2,ev_Stop[0],y+width/2,ev_Stop[0],y-width/2]
            self.cblObjSet.append(canvas.create_polygon(*p1, outline='gray', fill=ff(), width=2))

            if not self.wdtUpd:
                self.cblCords.append([ev_Stop[0], y])
            if self.trprns:
                self.crtIm(abs(ev_Start[0]-ev_Stop[0]), int(width), 0, color, canvas, int(min(ev_Start[0], ev_Stop[0])) ,int(y-width/2))
            else:
                self.imagesCv.append(None)
                self.imagesTk.append(None)
        elif abs(tanj) > 1.73:
            x = ev_Start[0]
            p1 = [x-width/2,ev_Start[1],x+width/2,ev_Start[1],x+width/2,ev_Stop[1],x-width/2,ev_Stop[1]]
            self.cblObjSet.append(canvas.create_polygon(*p1, outline='gray', fill=ff(), width=2))

            if not self.wdtUpd:
                self.cblCords.append([x, ev_Stop[1]])
            if self.trprns:
                self.crtIm(int(width), abs(ev_Start[1]-ev_Stop[1]), 0, color, canvas, int(x-width/2),int( min(ev_Start[1], ev_Stop[1])))
            else:
                self.imagesCv.append(None)
                self.imagesTk.append(None)
        else:
            t = max(abs(ev_Stop[0]-ev_Start[0]),abs(ev_Stop[1]-ev_Start[1]))
            w = width/2.828 #2 sqrt 2
            x = ev_Start[0]
            y = ev_Start[1]
            m_x = 0
            m_y = 0
            stp = [ev_Stop[0], ev_Stop[1]]
            rot = 45
            if tanj < 0:
                if xDiff < 0:
                    p1 = [x-w,y-w,x+w,y+w,x-t+w,y+t+w,x-t-w,y+t-w]
                    stp = [x-t,y+t]
                else:
                    p1 = [x-w,y-w,x+w,y+w,x+t+w,y-t+w,x+t-w,y-t-w]
                    stp = [x+t,y-t]
            else:
                if xDiff < 0:
                    p1 = [x-w,y+w,x+w,y-w,x-t+w,y-t-w,x-t-w,y-t+w]
                    stp = [x-t,y-t]
                else:
                    p1 = [x-w,y+w,x+w,y-w,x+t+w,y+t-w,x+t-w,y+t+w]
                    stp = [x+t,y+t]
            if xDiff < 0:
                if yDiff < 0:
                    rot = -45
                    m_x = -w
                    m_y = -w
                else:
                    rot = 45
                    m_x = -w
                    m_y = -w-t
            else:
                if yDiff < 0:
                    rot = -135
                    m_x = -w-t
                    m_y = -w
                else:
                    rot = 135
                    m_x = -w-t
                    m_y = -w-t
            print("p1: ", p1)
            self.cblObjSet.append(canvas.create_polygon(*p1, outline='gray', fill=ff(), width=2, tags = ""))
            
            if not self.wdtUpd:
                self.cblCords.append(stp)
            if self.trprns:
                # print("math.sqrt(2)*t: ", math.sqrt(2)*t)
                self.crtIm(int(math.sqrt(2)*t), int(width), rot, color, canvas, int(stp[0]), int(stp[1]))
                canvas.move(self.imagesCv[-1], m_x, m_y)
            else:
                self.imagesCv.append(None)
                self.imagesTk.append(None)
            
            
    def clrFPC(self, canvas):
        if len(self.cblObjSet) > self.setNum:
            i = self.setNum
            while i < len(self.cblObjSet):
                canvas.delete(self.cblObjSet[i])
                # if self.trprns:
                # if self.trnsLst[i]:
                    # canvas.delete(self.imagesCv[i])
                canvas.delete(self.imagesCv[i])
                i += 1
            del self.cblObjSet[self.setNum : len(self.cblObjSet)]
            del self.cblCords[self.setNum + 1 : len(self.cblCords)]
            # if self.trprns:
                # del self.imagesCv[self.setNum : len(self.imagesCv)]
            del self.imagesCv[self.setNum : len(self.imagesCv)]
            del self.imagesTk[self.setNum : len(self.imagesTk)]
            del self.trnsLst[self.setNum : len(self.trnsLst)]
            
                
            
    def clkFPC(self):
        if not self.clkOnce:
            self.setNum += 1
            self.clkOnce = True
            
    def wdtUpdate(self, canvas, color, wdt):
        stp = len(self.cblObjSet)
        tempTrns = self.trprns
        self.wdtUpd = True
        for i in range(stp):
            canvas.delete(self.cblObjSet[i])
            if self.trnsLst[i]:
                canvas.delete(self.imagesCv[i])
        self.cblObjSet.clear()
        for i in range(stp):
            self.trprns = self.trnsLst[i]
            self.drawFPC(canvas, self.cblCords[i], self.cblCords[i+1], wdt, color)
        self.wdtUpd = False
        self.trprns = tempTrns
        
    def delAll(self, canvas):
        stp = len(self.cblObjSet)
        for i in range(stp):
            canvas.delete(self.cblObjSet[i])
        self.cblObjSet.clear()
        
    def toggleTrnsp(self):
        self.trprns = not self.trprns
            
    def setCableTags(self, canvas, __tag):
        for i in self.cblObjSet:
            canvas.itemconfig(i, tag = __tag)
        
        
if __name__ == "__main__":
    app = SampleApp()
    
    app.mainloop()
