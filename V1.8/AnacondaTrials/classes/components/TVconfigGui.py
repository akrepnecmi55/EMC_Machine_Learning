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
from classes.components import Cable
from classes.FlatCable import *
from classes.components.LogGui import LogGui as logGui
from PIL import ImageTk, Image
from classes.db.TVConfigDatabase import TVConfigDatabase as tvcDb

class TVconfigGui():

    # def __init__(self, master):
    def __init__(self, master, rx):
        self.rx = rx
        tvCn = tk.Canvas(master, width= master.winfo_width(), height = master.winfo_height(), background = 'white')
        print(master.winfo_width())
        self.cm = 5
        self.scRate = st.panelCm/self.cm
        self.rects = []
        self.ovals = []
        self.texts = []
        self.stepSize = 1
        self.sleepTime = 10
        self.loggerObj = None
        p = Path(__file__).parents[2]
        self.tvcPath = os.path.join(p, 'mem\\tvcDb')
        self.pPath = os.path.join(p, 'mem\\panelDb')
        self.mbPath = os.path.join(p, 'mem\\mbDb')
        self.ursaPath = os.path.join(p, 'mem\\ursaDb')
        self.psuPath = os.path.join(p, 'mem\\psuDb')
        self.tconPath = os.path.join(p, 'mem\\tconDb')
        self.mWdt = master.winfo_width()
        self.mHgt = master.winfo_height()
        self.x_padding=50
        self.y_padding=25
        self.tvConfigName = ""


        self.isMbClkOnce = False
        self.isPsuClkOnce = False
        self.isUrsaClkOnce = False
        self.isTconClkOnce = False

        self.isMbClkTwice = False
        self.isPsuClkTwice = False
        self.isUrsaClkTwice = False
        self.isTconClkTwice = False

        self.isPnlAdded = False
        self.isMbAdded = False
        self.isPsuAdded = False
        self.isUrsaAdded = False
        self.isTconAdded = False
        
        self.mbRotation = 0 #number of turns
        self.mbDrag = [0, 0]
        self.mbScrewCords = None
        self.mbCords = None
        self.mbConCords = None
        
        self.psuRotation = 0 #number of turns
        self.psuDrag = [0, 0]
        self.psuName = None
        self.psuScrewCords = None
        self.psuCords = None
        self.psuConCords = None
        
        self.ursaRotation = 0 #number of turns
        self.ursaDrag = [0, 0]
        self.ursaName = None
        self.ursaScrewCords = None
        self.ursaCords = None
        self.ursaConCords = None

        self.dragMode = False

        self.isZoomed = False

        self.thSldStt = False

        self.cableMode = False
        self.cblAdded = False
        self.detCnOn = False

        self.zoomN = 0
        self.zoomedRects = []
        self.zoomedOvals = []
        self.zoomedTexts = []
        self.tempInitCblCons = []
        self.smtMoved = False
        self.cablingMode = False
        self.cablingStt = False
        self.isCblLocked = False
        self.cableFloatMode = False
        self.flatCables = []
        
        self.tempCblCrds = []
        self.tempCblObjs = []
        ## To be saved in Database
        self.realCblObjs = []

        self.emtMode = False
        self.emiStt = 0
        self.emiTapeRects = []
        self.emiTapeCords = []
        self.emiTapeTags = []
        self.ferMode = False
        self.emiTypeInd = 0 # this is the emi tape type index that is listed in settings file / will be increase by command
        self.ferStt = 0
        self.ferriteRects = []
        self.ferriteCords = []
        self.ferriteTags = []
        self.ferTypeInd = 0 # this is the ferrite type index that is listed in settings file / will be increase by command

        # self.images = []

        self.tvCn = tvCn

        self.tvCn.grid()
        self.tvCn.focus_set() #bunu belirtmek önemli. Bind focusu canvasa vermemiz lazım.

        self.tvCn.bind('<Motion>', self.move)
        self.tvCn.bind('<space>', self.space)
        self.tvCn.bind('<MouseWheel>', self.mWCombined)
        self.tvCn.bind('<Button-1>', self.gnrClk)
        self.tvCn.bind('<Button-3>', self.gnr_r_Clk)
        self.tvCn.bind('<Key>', self.wdtChgr)

    def gnr_r_Clk(self, event):
        self.clrCbl()
        self.clrEmiTape()
        self.clrFerTape()
        self.loggerObj.clrLog()


    def isEmiModeOn(func):
        def inner(self, *args, **kwargs):
            if self.emtMode:
                print("self.emtMode is ON")
                func(self, *args, **kwargs)
            else:
                print("self.emtMode is NOT ON!")
        return inner

    def isFerModeOn(func):
        def inner(self, *args, **kwargs):
            if self.ferMode:
                print("self.ferMode is ON")
                func(self, *args, **kwargs)
            else:
                print("self.ferMode is NOT ON!")
        return inner

    def clearEveryFlag(self):
        self.cablingStt = False
        self.cablingMode = False
        self.isCblLocked = False
        self.cableFloatMode = False
        self.dragMode = False
        self.isMbClkOnce = False
        self.isPsuClkOnce = False
        self.isUrsaClkOnce = False
        self.isTconClkOnce = False
        self.smtMoved = False
        self.isOnEdge = False
        self.detCnOn = False



    @isEmiModeOn
    def clrEmiTape(self):
        print("clrEmiTape called")
        self.emiStt = 0
        self.tvCn.delete(self.tmpEmiTape)
        self.clearEveryFlag()

    @isFerModeOn
    def clrFerTape(self):
        print("clrFerTape called")
        self.ferStt = 0
        self.tvCn.delete(self.tmpFerrite)
        self.clearEveryFlag()



    def cblNotAdded(func):
        def inner(self, *args, **kwargs):
            if self.cblAdded:
                print("cable added")
            else:
                print("cable not added")
                func(self, *args, **kwargs)
        return inner

    def isCablingSttOn(func):
        def inner(self):
            if self.cablingStt:
                print("self.cablingStt is ON")
                func(self)
            else:
                print("self.cablingStt is NOT ON!")
        return inner

    def isCablingSttOnTest(func):
        def inner(self, *args, **kwargs):
            if self.cablingStt:
                print("self.cablingStt is ON")
                func(self, *args, **kwargs)
            else:
                print("self.cablingStt is NOT ON!")
        return inner

    @isCablingSttOn
    def clrCbl(self):
        print("clrCbl called")
        self.cablingStt = False
        self.cablingMode = False
        self.isCblLocked = False
        self.cableFloatMode =  False
        self.tempCblObjs[-1].delAll(self.tvCn)
        self.tempCblObjs.pop()

    @isCablingSttOn
    def setCblTrns(self):
        self.tempCblObjs[-1].toggleTrnsp()
        tt = lambda: 'Kablonun bu kısmı havada ya da kapakta' if self.tempCblObjs[-1].trprns else 'Kablo arka metale basık'
        self.loggerObj.addTxtUp(tt())

    def cblSttNotOn(func):
        def inner(self, event):
            if self.cablingStt:
                print("self.cablingStt is ON and func wont be called")
            else:
                print("self.cablingStt is NOT ON and func will be called")
                func(self, event)
        return inner

    @isCablingSttOn
    def testT(self):
        print("bu method cablingStt ON ise çalışacak!")

    @isEmiModeOn
    def emiClc(self, cor):
        xW = st.emiTapeList[self.emiTypeInd][0]*self.cm #emi tapes x width
        yW = st.emiTapeList[self.emiTypeInd][1]*self.cm #emi tapes y width
        dim = [int(cor[0] - xW / 2), int(cor[1] - yW / 2), int(cor[0] + xW / 2), int(cor[1] + yW / 2)]
        if self.emiStt == 0: #if not clicked once, mouse see nothing and no emi tape is seen. ıt is ready to receive a command
            self.dim = dim
            self.emiTypeInd = 0 # this is the emi tape type index that is listed in settings file / will be increase by command
            self.clearEveryFlag()
            self.emiStt = 1 # now it is seen and ready to be put
            self.tmpEmiTape = self.makeRect(self.tvCn, self.dim, tags = 'tmpEmiTape', fill = 'gray')
            self.dragMode = True
        elif self.emiStt == 1: #if clicked once
            self.dim = self.tvCn.coords(self.tmpEmiTape)
            overlappedItems = self.tvCn.find_overlapping(self.dim[0], self.dim[1], self.dim[2], self.dim[3])
            print(overlappedItems)
            ## Bütün itemlardan tagleri ayırıp EMI tape'i ona göre kodlayıp kaydedeceğiz.
            ## Örneğin, SourceBoard to panel, MainboardLVDS to Panel vb.
            tags = []
            for i in overlappedItems:
                tags.append(self.tvCn.itemcget(i, "tags"))
            tmpStrTag = ""
            ctr  = 0
            for i in tags:
                if 'EmiTape' in i:
                    continue
                if 'current' in i:
                    continue
                if ctr > 0:
                   tmpStrTag += "-"
                tmpStrTag += i
                ctr += 1
            print("tags: ", tags)
            self.tvCn.itemconfig(self.tmpEmiTape, tag = tmpStrTag)
            self.emiTapeRects.append(self.tmpEmiTape)
            self.emiTapeCords.append(self.dim)
            self.emiTapeTags.append(tmpStrTag)
            self.clearEveryFlag()
            self.emiStt = 0
            # self.tvCn.delete(self.tmpEmiTape)

    @isFerModeOn
    def ferClc(self, cor):
        xW = st.ferList[self.ferTypeInd][0]*self.cm #ferrites x width
        yW = st.ferList[self.ferTypeInd][1]*self.cm #ferrites y width
        dim = [int(cor[0] - xW / 2), int(cor[1] - yW / 2), int(cor[0] + xW / 2), int(cor[1] + yW / 2)]
        if self.ferStt == 0: #if not clicked once, mouse see nothing and no ferrite is seen. ıt is ready to receive a command
            self.dim = dim
            self.ferTypeInd = 0 # this is the ferrite type index that is listed in settings file / will be increase by command
            self.clearEveryFlag()
            self.ferStt = 1 # now it is seen and ready to be put
            self.tmpFerrite = self.makeRect(self.tvCn, self.dim, tags = 'tmpFerrite', fill = '#252E33')
            self.dragMode = True
        elif self.ferStt == 1: #if clicked once
            self.dim = self.tvCn.coords(self.tmpFerrite)
            overlappedItems = self.tvCn.find_overlapping(self.dim[0], self.dim[1], self.dim[2], self.dim[3])
            print(overlappedItems)
            ## Bütün itemlardan tagleri ayırıp Ferrite'i ona göre kodlayıp kaydedeceğiz.
            ## Örneğin, SourceBoard to panel, MainboardLVDS to Panel vb.
            tags = []
            for i in overlappedItems:
                tags.append(self.tvCn.itemcget(i, "tags"))
            tmpStrTag = ""
            ctr  = 0
            for i in tags:
                if 'Ferrite' in i:
                    continue
                if 'current' in i:
                    continue
                if ctr > 0:
                   tmpStrTag += "-"
                tmpStrTag += i
                ctr += 1
            print("tags: ", tags)
            self.ferriteRects.append(self.tmpFerrite)
            self.ferriteCords.append(self.dim)
            self.ferriteTags.append(tmpStrTag)
            self.clearEveryFlag()
            self.ferStt = 0
            # self.tvCn.delete(self.tmpEmiTape)

    def gnrClk(self, event):
        ev = [event.x,event.y]
        if self.cablingStt:
            if self.isCblLocked: #the cable is locked first time
                if self.cableFloatMode: #the cable is locked and routing is being done at the moment
                    if not self.cablingMode:
                        self.tempCblObjs[-1].clkFPC()
                    else:
                        if self.lastTag2Cbl.split('-')[-1] == self.tvCn.gettags(self.firstMate)[0].split('-')[-1] and self.lastTag2Cbl != self.tvCn.gettags(self.firstMate)[0]:
                            self.tempCblObjs[-1].clkFPC()
                            tCor = self.tempCblObjs[-1].cblCords[-1]
                            print("tCor: ", tCor)
                            print("ev: ", ev)
                            dist = ((ev[0]-tCor[0])**2 + (ev[1]-tCor[1])**2)
                            print("distSquare: ", dist)
                            print("(self.cm/2)**2: ", (self.cm/2)**2)
                            if ( dist < (self.cm)**2):
                                # self.realCblObjs.append([self.tmpCbl, self.getMatings()])
                                self.realCblObjs.append([self.tmpCbl, self.getMatings(), self.tempCblObjs[-1]])
                                #cable object is added to cables once it is connected. format is : [obj, 'LVDS', [mb, tcon]]
                                self.cablingStt = False
                                self.cablingMode = False
                                self.isCblLocked = False
                                self.cableFloatMode =  False
                                print("realCblObjs: ", self.realCblObjs[-1][0].shape, self.realCblObjs[-1][0].shield,
                                self.realCblObjs[-1][0]._type, self.realCblObjs[-1][0].width, self.realCblObjs[-1][2].cblCords,
                                self.realCblObjs[-1][2].trnsLst, self.realCblObjs[-1][1], self.realCblObjs[-1][2])
                                self.flatCables[-1].setCableTags(self.tvCn, self.realCblObjs[-1][1][0]+"-"+self.realCblObjs[-1][1][1][0]+"-"+self.realCblObjs[-1][1][1][1])

        else:
            if self.cablingMode:
                self.cablingStt = True
                self.firstMate = self.tvCn.find_withtag(self.lastTag2Cbl)
                print("gnrClk deki self.lastTag2Cbl: ", self.lastTag2Cbl)
                print("self.tvCn.gettags(self.firstMate): ",self.tvCn.gettags(self.firstMate) )
                print("self.tvCn.gettags(self.firstMate)[0].split('-')[-1]: ", self.tvCn.gettags(self.firstMate)[0].split('-')[-1])
                delArr(self.tvCn, self.tempCblCrds) #clean the temporary cale coords because it is the first coords to start with
                self.tempCblCrds.append([self.tvCn.coords(self.firstMate)]) #  add the first coord to the temporary coords list which is the first connector
                self.isCblLocked = True #the cable is locked first time
                self.cableFloatMode = True #the cable is locked first time and cable is float before done. Routing mode
                print("self.tvCn.gettags(self.firstMate)[0] ", self.tvCn.gettags(self.firstMate)[0].split('-')[-1])
                print("self.lastTag2Cbl conTag: ", self.lastTag2Cbl.split('-')[-1])
                print("self.lastTag2Cbl fullTag: ", self.lastTag2Cbl)
                self.tmpCbl = Cable.cblSel(self.tvCn.gettags(self.firstMate)[0].split('-')[-1])
                print("coloru: ", self.tmpCbl.color)
                self.flatCables.append(FlatCable(self.rx))
                self.tempCblObjs.append(self.flatCables[-1])
                self.loggerObj.updateLbl("Kablonun panele yapışık olmayan tarafları için space'e bas")
                self.loggerObj.updateLbl("Kablo kalınlığını artırmak için 'Q', azaltmak için 'A' ya basmalısın")
                self.loggerObj.addTxtDown("Shield yapısını değiştirmek için mouse wheel ile oynayın")
                self.loggerObj.addTxtDown("Vazgeçmek içinse sağ tıkla")
            elif self.emtMode:
                self.emiClc(ev)
            elif self.ferMode:
                print("1")
                self.ferClc(ev)
        self.testT()


    def getMatings(self):
        #retuns the conn type and the matings by alphabetic order eg: LVDS, [MB, TCON]
        # print("bura kopuk: ", sorted([self.tvCn.gettags(self.firstMate)[0].split('-')[0], self.lastTag2Cbl.split('-')[0]], key=str.lower))
        # return [self.lastTag2Cbl.split('-')[-1], sorted([self.tvCn.gettags(self.firstMate)[0].split('-')[0], self.lastTag2Cbl.split('-')[0]], key=str.lower)]
        return [self.lastTag2Cbl.split('-')[-1], [self.tvCn.gettags(self.firstMate)[0].split('-')[0], self.lastTag2Cbl.split('-')[0]]]

    def mWCombined(self, event):
        if not self.cablingStt:
            self.mW(event)
        else:
            self.cblShlShft(event)

    @isCablingSttOnTest
    def cblShlShft(self, event):
        # print("olacak")
        if event.delta > 0:
            self.tmpCbl.shldTypeShiftUp()
        elif event.delta < 0:
            self.tmpCbl.shldTypeShiftDwn()
        self.loggerObj.addTxtUp(self.tmpCbl.shield, " : ", self.tmpCbl.shieldTypes[self.tmpCbl.shield])

    @cblSttNotOn
    def mW(self, event):
        if not self.isZoomed:
            if event.delta > 0:
                ev = [event.x,event.y]
                for i in self.zoomedRects:
                    self.tvCn.delete(i)
                for i in self.zoomedOvals:
                    self.tvCn.delete(i)
                for i in self.zoomedTexts:
                    self.tvCn.delete(i)
                self.zoomedRects.clear()
                self.zoomedOvals.clear()
                self.zoomedTexts.clear()
                del self.zoomedRects[:]
                del self.zoomedOvals[:]
                del self.zoomedTexts[:]
                if self.isPnlAdded:
                    for i in self.tempPnlRects:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedRects.append(self.zoomInItems(ev, i, shape = 'rect'))
                    for i in self.tempPnlOvals:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedOvals.append(self.zoomInItems(ev, i, shape = 'oval'))
                    for i in self.tempPnlTexts:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedTexts.append(self.zoomInItems(ev, i, shape = 'text'))
                if self.isMbAdded:
                    for i in self.tempMbRects:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedRects.append(self.zoomInItems(ev, i, shape = 'rect'))
                    for i in self.tempMbOvals:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedOvals.append(self.zoomInItems(ev, i, shape = 'oval'))
                    for i in self.tempMbTexts:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedTexts.append(self.zoomInItems(ev, i, shape = 'text'))
                if self.isUrsaAdded:
                    for i in self.tempUrRects:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedRects.append(self.zoomInItems(ev, i, shape = 'rect'))
                    for i in self.tempUrOvals:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedOvals.append(self.zoomInItems(ev, i, shape = 'oval'))
                    for i in self.tempUrTexts:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedTexts.append(self.zoomInItems(ev, i, shape = 'text'))
                if self.isPsuAdded:
                    for i in self.tempPsuRects:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedRects.append(self.zoomInItems(ev, i, shape = 'rect'))
                    for i in self.tempPsuOvals:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedOvals.append(self.zoomInItems(ev, i, shape = 'oval'))
                    for i in self.tempPsuTexts:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedTexts.append(self.zoomInItems(ev, i, shape = 'text'))
                if self.isTconAdded:
                    for i in self.tempTconRects:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedRects.append(self.zoomInItems(ev, i, shape = 'rect'))
                    for i in self.tempTconOvals:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedOvals.append(self.zoomInItems(ev, i, shape = 'oval'))
                    for i in self.tempTconTexts:
                        self.tvCn.itemconfigure(i, state='hidden')
                        self.zoomedTexts.append(self.zoomInItems(ev, i, shape = 'text'))
                self.isZoomed = True
        else:
            if event.delta < 0:
                ev = [event.x,event.y]
                for i in self.zoomedRects:
                    self.tvCn.delete(i)
                for i in self.zoomedOvals:
                    self.tvCn.delete(i)
                for i in self.zoomedTexts:
                    self.tvCn.delete(i)
                self.zoomedRects.clear()
                self.zoomedOvals.clear()
                self.zoomedTexts.clear()
                del self.zoomedRects[:]
                del self.zoomedOvals[:]
                del self.zoomedTexts[:]
                if self.isPnlAdded:
                    for i in self.tempPnlRects:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempPnlOvals:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempPnlTexts:
                        self.tvCn.itemconfigure(i, state='normal')
                if self.isMbAdded:
                    for i in self.tempMbRects:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempMbOvals:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempMbTexts:
                        self.tvCn.itemconfigure(i, state='normal')
                if self.isUrsaAdded:
                    for i in self.tempUrRects:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempUrOvals:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempUrTexts:
                        self.tvCn.itemconfigure(i, state='normal')
                if self.isPsuAdded:
                    for i in self.tempPsuRects:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempPsuOvals:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempPsuTexts:
                        self.tvCn.itemconfigure(i, state='normal')
                if self.isTconAdded:
                    for i in self.tempTconRects:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempTconOvals:
                        self.tvCn.itemconfigure(i, state='normal')
                    for i in self.tempTconTexts:
                        self.tvCn.itemconfigure(i, state='normal')
                self.isZoomed = False

    def zoomInItems(self, ref, item, **karg):
        arr = self.tvCn.coords(item)
        scaler = [[2,0],[0,2]]
        if karg['shape'] == 'rect':
            temp = [[arr[0],arr[1]],[arr[2],arr[3]]]
            newTemp = np.subtract(temp, ref)
            scaled = np.dot(newTemp, scaler)
            final = np.add(scaled, ref)
            fnl = [final[0][0], final[0][1], final[1][0], final[1][1]]
            return self.makeRect(self.tvCn, fnl, width = self.tvCn.itemcget(item, 'width'), tags = self.tvCn.itemcget(item, 'tags'), fill = self.tvCn.itemcget(item, 'fill'))
        if karg['shape'] == 'oval':
            temp = [[arr[0],arr[1]],[arr[2],arr[3]]]
            newTemp = np.subtract(temp, ref)
            scaled = np.dot(newTemp, scaler)
            final = np.add(scaled, ref)
            fnl = [final[0][0], final[0][1], final[1][0], final[1][1]]
            return self.makeOval(self.tvCn, fnl, width = self.tvCn.itemcget(item, 'width'), tags = self.tvCn.itemcget(item, 'tags'), fill = self.tvCn.itemcget(item, 'fill'))
        if karg['shape'] == 'text':
            temp = [[arr[0],arr[1]]]
            newTemp = np.subtract(temp, ref)
            scaled = np.dot(newTemp, scaler)
            final = np.add(scaled, ref)
            fnl = [final[0][0], final[0][1]]
            return self.makeText(self.tvCn, fnl, width = self.tvCn.itemcget(item, 'width'), text = self.tvCn.itemcget(item, 'text'))

    def space(self, event):
        print("space e girdi")
        if self.dragMode:
            print("drag mode ON")
            ev = [event.x,event.y]
            if self.isMbClkOnce:
                for i in self.tempMbRects:
                    self.rotateRect(ev, i)
                for i in self.tempMbOvals:
                    self.rotateOval(ev, i)
                for i in self.tempMbTexts:
                    self.rotateText(ev, i)
                self.mbRotation += 1
            if self.isUrsaClkOnce:
                for i in self.tempUrRects:
                    self.rotateRect(ev, i)
                for i in self.tempUrOvals:
                    self.rotateOval(ev, i)
                for i in self.tempUrTexts:
                    self.rotateText(ev, i)
                self.ursaRotation += 1
            if self.isPsuClkOnce:
                for i in self.tempPsuRects:
                    self.rotateRect(ev, i)
                for i in self.tempPsuOvals:
                    self.rotateOval(ev, i)
                for i in self.tempPsuTexts:
                    self.rotateText(ev, i)
                self.psuRotation += 1
            if self.isTconClkOnce:
                for i in self.tempTconRects:
                    self.rotateRect(ev, i)
                for i in self.tempTconOvals:
                    self.rotateOval(ev, i)
                for i in self.tempTconTexts:
                    self.rotateText(ev, i)
            if self.emiStt == 1:
                self.rotateRect(ev,self.tmpEmiTape)
            if self.ferStt == 1:
                self.rotateRect(ev,self.tmpFerrite)
        self.setCblTrns()

    def rotateRect(self, ref, rect):
        temp = self.tvCn.coords(rect)
        relTemp = [[temp[0]-ref[0],temp[1]-ref[1]],[temp[2]-ref[0],temp[3]-ref[1]]]
        rotator = [[0,1],[-1,0]]
        rotated = np.dot(relTemp,rotator)
        self.tvCn.coords(rect, [rotated[0][0]+ref[0], rotated[0][1]+ref[1], rotated[1][0]+ref[0], rotated[1][1]+ref[1]] )
        self.dim = [rotated[0][0]+ref[0], rotated[0][1]+ref[1], rotated[1][0]+ref[0], rotated[1][1]+ref[1]]

    def rotateOval(self, ref, oval):
        temp = self.tvCn.coords(oval)
        relTemp = [[temp[0]-ref[0],temp[1]-ref[1]],[temp[2]-ref[0],temp[3]-ref[1]]]
        rotator = [[0,1],[-1,0]]
        rotated = np.dot(relTemp,rotator)
        self.tvCn.coords(oval, [rotated[0][0]+ref[0], rotated[0][1]+ref[1], rotated[1][0]+ref[0], rotated[1][1]+ref[1]] )

    def rotateText(self, ref, text):
        temp = self.tvCn.coords(text)
        relTemp = [ [temp[0]-ref[0],temp[1]-ref[1]] ]
        rotator = [[0,1],
                   [-1,0]]
        rotated = np.dot(relTemp,rotator)
        self.tvCn.coords(text, [ rotated[0][0]+ref[0], rotated[0][1]+ref[1] ] )

    def stepUp(self, obj_list):
        for i in obj_list:
            self.tvCn.tag_raise(i)

    @cblNotAdded
    @cblSttNotOn
    def mbClk(self, event):
        print("mbClk a girdi")
        ev = [event.x,event.y]
        if not self.dragMode:
            self.stepUp(self.tempMbRects)
            self.stepUp(self.tempMbOvals)
            self.stepUp(self.tempMbTexts)
            self.dragMode = True
            self.isMbClkOnce = True
            self.isPsuClkOnce = False
            self.isUrsaClkOnce = False
            self.isTconClkOnce = False
        else:
            self.dragMode = False
            self.isTconClkOnce = False
            self.isMbClkOnce = False
            self.isPsuClkOnce = False
            self.isUrsaClkOnce = False
        self.lastEv = ev
        print("mbcLK dan çıktı")

    @cblNotAdded
    @cblSttNotOn
    def ursaClk(self, event):
        print("ursa clk a girdi")
        ev = [event.x,event.y]
        if not self.dragMode:
            self.stepUp(self.tempUrRects)
            self.stepUp(self.tempUrOvals)
            self.stepUp(self.tempUrTexts)
            self.dragMode = True
            self.isMbClkOnce = False
            self.isPsuClkOnce = False
            self.isUrsaClkOnce = True
            self.isTconClkOnce = False
        else:
            self.dragMode = False
            self.isTconClkOnce = False
            self.isMbClkOnce = False
            self.isPsuClkOnce = False
            self.isUrsaClkOnce = False
        self.lastEv = ev
        print("ursa clk dan çıktı")

    @cblNotAdded
    @cblSttNotOn
    def psuClk(self, event):
        print("psu clk a girdi")
        ev = [event.x,event.y]
        if not self.dragMode:
            self.stepUp(self.tempPsuRects)
            self.stepUp(self.tempPsuOvals)
            self.stepUp(self.tempPsuTexts)
            self.dragMode = True
            self.isMbClkOnce = False
            self.isPsuClkOnce = True
            self.isUrsaClkOnce = False
            self.isTconClkOnce = False
        else:
            self.dragMode = False
            self.isTconClkOnce = False
            self.isMbClkOnce = False
            self.isPsuClkOnce = False
            self.isUrsaClkOnce = False
        self.lastEv = ev
        print("psu clk dan çıktı")

    @cblNotAdded
    @cblSttNotOn
    def tconClk(self, event):
        ev = [event.x,event.y]
        if not self.dragMode:
            self.stepUp(self.tempTconRects)
            self.stepUp(self.tempTconOvals)
            self.stepUp(self.tempTconTexts)
            self.dragMode = True
            self.isMbClkOnce = False
            self.isPsuClkOnce = False
            self.isUrsaClkOnce = False
            self.isTconClkOnce = True
        else:
            self.dragMode = False
            self.isTconClkOnce = False
            self.isMbClkOnce = False
            self.isPsuClkOnce = False
            self.isUrsaClkOnce = False
        self.lastEv = ev

    def move(self, event):
        ev = [event.x,event.y]
        self.tvCn.delete('tempIdentifier')
        if self.dragMode:
            diff = [ev[0]-self.lastEv[0],ev[1]-self.lastEv[1]]
            if self.isMbClkOnce:
                for i in self.tempMbRects:
                    self.tvCn.move(i, diff[0], diff[1])
                for i in self.tempMbOvals:
                    self.tvCn.move(i, diff[0], diff[1])
                for i in self.tempMbTexts:
                    self.tvCn.move(i, diff[0], diff[1])
                self.mbDrag[0] += diff[0]
                self.mbDrag[1] += diff[1]
            if self.isUrsaClkOnce:
                for i in self.tempUrRects:
                    self.tvCn.move(i, diff[0], diff[1])
                for i in self.tempUrOvals:
                    self.tvCn.move(i, diff[0], diff[1])
                for i in self.tempUrTexts:
                    self.tvCn.move(i, diff[0], diff[1])
                self.ursaDrag[0] += diff[0]
                self.ursaDrag[1] += diff[1]
            if self.isPsuClkOnce:
                for i in self.tempPsuRects:
                    self.tvCn.move(i, diff[0], diff[1])
                for i in self.tempPsuOvals:
                    self.tvCn.move(i, diff[0], diff[1])
                for i in self.tempPsuTexts:
                    self.tvCn.move(i, diff[0], diff[1])
                self.psuDrag[0] += diff[0]
                self.psuDrag[1] += diff[1]
            if self.isTconClkOnce:
                for i in self.tempTconRects:
                    self.tvCn.move(i, diff[0], diff[1])
                for i in self.tempTconOvals:
                    self.tvCn.move(i, diff[0], diff[1])
                for i in self.tempTconTexts:
                    self.tvCn.move(i, diff[0], diff[1])
            if self.emiStt:
                self.tvCn.move(self.tmpEmiTape, diff[0], diff[1])
                # self.dim = [self.dim[0]+diff[0], diff[1]+diff[1], self.dim[2]+diff[0], diff[3]+diff[1]]
                print(self.dim)
            if self.ferStt:
                self.tvCn.move(self.tmpFerrite, diff[0], diff[1])
            self.lastEv = ev
            self.smtMoved = True
        else:
            if self.isZoomed:
                if self.edgeCheck(ev):
                    self.isOnEdge = True
                    self.tSlide = th.Thread(target=self.slide, args = [ev])
                    self.tSlide.start()
                else:
                    self.isOnEdge = False
            else:
                if self.detCnOn:
                    if self.smtMoved:
                        self.updCblCons()
                        self.smtMoved = False
                    self.idntfCns(ev)
                if self.cableFloatMode:
                    if self.tempCblObjs[-1].setNum < 1:
                        tcor = self.tvCn.coords(self.firstMate)
                        cor = [(tcor[0] + tcor[2])/2 , (tcor[1] + tcor[3])/2]
                        self.tempCblObjs[-1].drawFPC(self.tvCn, cor, ev, self.tmpCbl.width*self.cm, self.tmpCbl.color)
                    else:
                        ind = self.tempCblObjs[-1].setNum
                        cor = self.tempCblObjs[-1].cblCords[ind]
                        self.tempCblObjs[-1].drawFPC(self.tvCn, cor, ev, self.tmpCbl.width*self.cm, self.tmpCbl.color)

            self.lastEv = ev

    def wdtChgr(self, event):
        if event.keysym == 'q':
            self.chgCblWdt(self.tmpCbl, 'inc')
        elif event.keysym == 'a':
            self.chgCblWdt(self.tmpCbl, 'dec')

    def chgCblWdt(self, cblObj, command):
        if command == 'inc':
            cblObj.width += 0.2
        elif command == 'dec':
            cblObj.width -= 0.2
        self.tempCblObjs[-1].wdtUpdate(self.tvCn, self.tmpCbl.color, cblObj.width*self.cm)
        self.loggerObj.addTxtUp("cable width is: ", str(cblObj.width))

    def edgeCheck(self, ev):
        if ev[0] > self.mWdt*0.95:
            return True
        elif ev[0] < self.mWdt*0.05:
            return True
        elif ev[1] > self.mHgt*0.95:
            return True
        elif ev[1] < self.mHgt*0.05:
            return True
        else:
            return False

    def slide(self, ev):
        while(self.isOnEdge):

            if ev[0] > self.mWdt*0.95:
                stepX = -self.stepSize
            elif ev[0] < self.mWdt*0.05:
                stepX = self.stepSize
            else:
                stepX = 0

            if ev[1] > self.mHgt*0.95:
                stepY = -self.stepSize
            elif ev[1] < self.mHgt*0.05:
                stepY = self.stepSize
            else:
                stepY = 0

            sleep(0.05)
            self.moveItems(stepX, stepY)
        self.thSldStt = False

    def idntfCns(self, ev):
        if self.cblAdded:
            if self.detCnOn:
                tmpRtn = self.isNearCon(ev, self.tempInitCblCons)
                if tmpRtn[0]:
                    self.makeOval(self.tvCn, tmpRtn[1][0], width = 3, tags = 'tempIdentifier', outline = 'red' )
                    self.lastTag2Cbl = tmpRtn[1][1]
                    print("self.lastTag2Cbl: ", self.lastTag2Cbl)
                    self.cablingMode = True
                else:
                    self.cablingMode = False

    def isNearCon(self, ev, cons):
        for i in cons:
            tCon = [(i[0][0]+i[0][2])/2, (i[0][1]+i[0][3])/2]
            # rad = abs(i[0]-i[2])  #Tam çapı
            rad = abs(i[0][0]-i[0][2])  #Tam çapı
            difX = ev[0]-tCon[0]
            difY = ev[1]-tCon[1]
            if (difX ** 2 + difY ** 2) < rad ** 2:
                return [True, i]
        return [False, ev]

    def moveItems(self, stepX, stepY):
        print("moveItems a girdi")
        for i in self.zoomedRects:
            rect = self.tvCn.coords(i)
            self.tvCn.coords(i, [rect[0]+stepX, rect[1]+stepY, rect[2]+stepX, rect[3]+stepY])
        for i in self.zoomedOvals:
            oval = self.tvCn.coords(i)
            self.tvCn.coords(i, [oval[0]+stepX, oval[1]+stepY, oval[2]+stepX, oval[3]+stepY])
        for i in self.zoomedTexts:
            text = self.tvCn.coords(i)
            self.tvCn.coords(i, [text[0]+stepX, text[1]+stepY])
            
    def showTVC(self, code):
        self.tvcName = code
        mbRotation = 0
        mbDrag = [0, 0]
        mbCords = None
        with shelve.open(self.tvcPath, writeback=True) as tvcDb:
            idx = tvcDb['tvConfigCode'].index(code)
            self.addPanel(tvcDb['pnlCode'][idx])
            self.addMB(tvcDb['mbCode'][idx])
            mbRotation = tvcDb['mbRotNum'][idx]
            mbCords = tvcDb['mbCords'][idx]
            mbDrag = tvcDb['mbDrag'][idx]
            
            self.isPsuAdded = tvcDb['isPsuAdded'][idx]
            if self.isPsuAdded:
                self.addPSU(tvcDb['psuCode'][idx])
            psuRotation = tvcDb['psuRotNum'][idx]
            psuCords = tvcDb['psuCords'][idx]
            psuDrag = tvcDb['psuDrag'][idx]
            
            self.isUrsaAdded = tvcDb['isUrsaAdded'][idx]
            if self.isUrsaAdded:
                self.addUrsa(tvcDb['ursaCode'][idx])
            ursaRotation = tvcDb['ursaRotNum'][idx]
            ursaCords = tvcDb['ursaCords'][idx]
            ursaDrag = tvcDb['ursaDrag'][idx]
            
            for i in range(len(tvcDb['cableShapes'][idx])):
                self.flatCables.append(FlatCable(self.rx))
                # self.tempCblObjs.append(self.flatCables[-1])
                lenX = len(tvcDb['cableCords'][idx][i])
                self.flatCables[-1].setNum = lenX
                print("lenX: ", lenX)
                cords = tvcDb['cableCords'][idx][i]
                width = tvcDb['cableWidths'][idx][i]
                color = tvcDb['cableColors'][idx][i]
                tag = tvcDb['cableTags'][idx][i]
                for h in range(lenX - 1):
                    print("cords[h], cords[h+1]: ", cords[h], ", ", cords[h+1])
                    self.flatCables[-1].drawFPC(self.tvCn, cords[h], cords[h+1], width*self.cm, color)
                self.flatCables[-1].setCableTags(self.tvCn, tag)
                
            for i in range(len(tvcDb['emiTapeCords'][idx])):
                cords = tvcDb['emiTapeCords'][idx][i]
                tag = tvcDb['emiTapeTags'][idx][i]  
                self.emiTapeRects.append(self.makeRect(self.tvCn, cords, tags = tag, fill = 'gray'))
                
            for i in range(len(tvcDb['ferriteCords'][idx])):
                cords = tvcDb['ferriteCords'][idx][i]
                tag = tvcDb['ferriteTags'][idx][i]  
                self.ferriteRects.append(self.makeRect(self.tvCn, cords, tags = tag, fill = '#252E33'))
                
        tvcDb.close()
        
        evMB = [self.x_padding+int(self.mb_coordinate[0]*self.screen_rate), self.y_padding+int(self.mb_coordinate[1]*self.screen_rate)]
        for k in range(mbRotation % 4):
            for i in self.tempMbRects:
                self.rotateRect(evMB, i)
            for i in self.tempMbOvals:
                self.rotateOval(evMB, i)
            for i in self.tempMbTexts:
                self.rotateText(evMB, i)
            shift = int(self.mbH*self.screen_rate)
            if k % 2 != 0:
                shift = int(self.mbW*self.screen_rate)
            for i in self.tempMbRects:
                self.tvCn.move(i, shift, 0)
            for i in self.tempMbOvals:
                self.tvCn.move(i, shift, 0)
            for i in self.tempMbTexts:
                self.tvCn.move(i, shift, 0)
        
        shiftX = mbCords[0] - evMB[0]
        shiftY = mbCords[1] - evMB[1]
        
        for i in self.tempMbRects:
            self.tvCn.move(i, shiftX, shiftY)
        for i in self.tempMbOvals:
            self.tvCn.move(i, shiftX, shiftY)
        for i in self.tempMbTexts:
            self.tvCn.move(i, shiftX, shiftY)
        
#PSU için
        if self.isPsuAdded:
            evPSU = [self.psu_x_padding, self.psu_y_padding]
            for k in range(psuRotation % 4):
                for i in self.tempPsuRects:
                    self.rotateRect(evPSU, i)
                for i in self.tempPsuOvals:
                    self.rotateOval(evPSU, i)
                for i in self.tempPsuTexts:
                    self.rotateText(evPSU, i)
                shift = int(self.psuH*self.screen_rate)
                if k % 2 != 0:
                    shift = int(self.psuW*self.screen_rate)
                for i in self.tempPsuRects:
                    self.tvCn.move(i, shift, 0)
                for i in self.tempPsuOvals:
                    self.tvCn.move(i, shift, 0)
                for i in self.tempPsuTexts:
                    self.tvCn.move(i, shift, 0)
            
            shiftX = psuCords[0] - evPSU[0]
            shiftY = psuCords[1] - evPSU[1]
            
            for i in self.tempPsuRects:
                self.tvCn.move(i, shiftX, shiftY)
            for i in self.tempPsuOvals:
                self.tvCn.move(i, shiftX, shiftY)
            for i in self.tempPsuTexts:
                self.tvCn.move(i, shiftX, shiftY)
            
#Ursa
        if self.isUrsaAdded:
            evUrsa = [self.ursa_x_padding, self.ursa_y_padding]
            for k in range(ursaRotation % 4):
                for i in self.tempUrRects:
                    self.rotateRect(evUrsa, i)
                for i in self.tempUrOvals:
                    self.rotateOval(evUrsa, i)
                for i in self.tempUrTexts:
                    self.rotateText(evUrsa, i)
                shift = int(self.ursaH*self.screen_rate)
                if k % 2 != 0:
                    shift = int(self.ursaW*self.screen_rate)
                for i in self.tempUrRects:
                    self.tvCn.move(i, shift, 0)
                for i in self.tempUrOvals:
                    self.tvCn.move(i, shift, 0)
                for i in self.tempUrTexts:
                    self.tvCn.move(i, shift, 0)
            
            shiftX = ursaCords[0] - evUrsa[0]
            shiftY = ursaCords[1] - evUrsa[1]
            
            for i in self.tempUrRects:
                self.tvCn.move(i, shiftX, shiftY)
            for i in self.tempUrOvals:
                self.tvCn.move(i, shiftX, shiftY)
            for i in self.tempUrTexts:
                self.tvCn.move(i, shiftX, shiftY)
                
        
        

    def addPanel(self, code):
        self.getIndex(code) #self.Index became the index of the Code in DB
        self.panelName = code
        self.getInfo(self.Index)
        self.tempPnlRects = []
        self.tempPnlOvals = []
        self.tempPnlTexts = []
        self.tempTconRects = []
        self.tempTconOvals = []
        self.tempTconTexts = []
        self.backplane = self.makeRect(self.tvCn, [50,25,850,475], width = 3, tags = "backplane",fill="#E1E9ED")
        self.tempPnlRects.append(self.backplane)
        if self.tcon_coordinates is not None:
            self.isTconAdded = True
            self.tempTconRects.append(self.makeRect(self.tvCn, [int(self.tcon_coordinates[0][0]*self.screen_rate)+self.x_padding,
                                                                int(self.tcon_coordinates[0][1]*self.screen_rate)+self.y_padding,
                                                                int(self.tcon_coordinates[1][0]*self.screen_rate)+self.x_padding,
                                                                int(self.tcon_coordinates[1][1]*self.screen_rate)+self.y_padding],
                                                                width = 3, tags = "tcon" , fill="#00EE6D"))

            self.tempTconTexts.append(self.makeText(self.tvCn, [int(self.x_padding+(self.tcon_coordinates[0][0]*self.screen_rate+self.tcon_coordinates[1][0]*self.screen_rate)/2),
                                                                int(self.y_padding+(self.tcon_coordinates[0][1]*self.screen_rate+self.tcon_coordinates[1][1]*self.screen_rate)/2)],
                                                                text = "TCON", angle=0))


            ctr=0
            for i in range(len(self.tcon_lvds_connector_coordinates)):
                self.tempTconOvals.append(self.makeOval(self.tvCn, [int(self.tcon_lvds_connector_coordinates[i][0]*self.screen_rate+self.x_padding)-3,
                                                                int(self.tcon_lvds_connector_coordinates[i][1]*self.screen_rate+self.y_padding)-3 ,
                                                                int(self.tcon_lvds_connector_coordinates[i][0]*self.screen_rate+self.x_padding)+3,
                                                                int(self.tcon_lvds_connector_coordinates[i][1]*self.screen_rate+self.y_padding)+3 ],
                                                                 width=2, tags="tcon-con-"+str(ctr)+"-LVDS",fill="orange"))
                self.tempTconTexts.append(self.makeText(self.tvCn, [int(self.x_padding+self.tcon_lvds_connector_coordinates[i][0]*self.screen_rate),
                                                                    int(self.y_padding+self.tcon_lvds_connector_coordinates[i][1]*self.screen_rate)],
                                                                    text = "LVDS"))
                ctr+=1

            for i in range(len(self.screw_coordinates)):
                self.tempPnlRects.append(self.makeRect(self.tvCn, [ int(self.screw_coordinates[i][0]*self.screen_rate+self.x_padding)-3 ,
                                                                    int(self.screw_coordinates[i][1]*self.screen_rate+self.y_padding)-3 ,
                                                                    int(self.screw_coordinates[i][0]*self.screen_rate+self.x_padding)+3 ,
                                                                    int(self.screw_coordinates[i][1]*self.screen_rate+self.y_padding)+3 ],
                                                                 width=2, tags="tcon screw"+str(i+1)))
            if self.tcon_dc_connector_coordinates is not None:
                ctr=0
                for i in range(len(self.tcon_dc_connector_coordinates)):
                    self.tempTconOvals.append(self.makeOval(self.tvCn, [int(self.tcon_dc_connector_coordinates[i][0]*self.screen_rate+self.x_padding)-3,
                                                                    int(self.tcon_dc_connector_coordinates[i][1]*self.screen_rate+self.y_padding)-3 ,
                                                                    int(self.tcon_dc_connector_coordinates[i][0]*self.screen_rate+self.x_padding)+3,
                                                                    int(self.tcon_dc_connector_coordinates[i][1]*self.screen_rate+self.y_padding)+3 ],
                                                                     width=2, tags="tcon-con-"+str(ctr)+"-DC",fill="orange"))
                    self.tempTconTexts.append(self.makeText(self.tvCn, [int(self.x_padding+self.tcon_dc_connector_coordinates[i][0]*self.screen_rate),
                                                                        int(self.y_padding+self.tcon_lvds_connector_coordinates[i][1]*self.screen_rate)],
                                                                        text = "DC"))
                    ctr+=1

        for i in range(len(self.SB_rectangles)):
            self.tempPnlRects.append(self.makeRect(self.tvCn, [int(self.SB_rectangles[i][0]*self.screen_rate)+self.x_padding ,
                                                            int(self.SB_rectangles[i][1]*self.screen_rate)+self.y_padding ,
                                                            int(self.SB_rectangles[i][2]*self.screen_rate)+self.x_padding,
                                                            int(self.SB_rectangles[i][3]*self.screen_rate)+self.y_padding],
                                                            width=3, tags ="xBoard"+str(i+1),fill="#00EE6D"))
            self.tempPnlTexts.append(self.makeText(self.tvCn, [int(self.x_padding+(self.SB_rectangles[i][0]*self.screen_rate+self.SB_rectangles[i][2]*self.screen_rate)/2),
                                                                int(self.y_padding+(self.SB_rectangles[i][1]*self.screen_rate+self.SB_rectangles[i][3]*self.screen_rate)/2)],
                                                                text = "xBoard"+str(i+1), angle=0))
        ctr=0
        for i in range(len(self.sb_connector_coordinates)):
            self.tempPnlOvals.append(self.makeOval(self.tvCn, [int(self.sb_connector_coordinates[i][0]*self.screen_rate+self.x_padding)-3,
                                                            int(self.sb_connector_coordinates[i][1]*self.screen_rate+self.y_padding)-3 ,
                                                            int(self.sb_connector_coordinates[i][0]*self.screen_rate+self.x_padding)+3,
                                                            int(self.sb_connector_coordinates[i][1]*self.screen_rate+self.y_padding)+3 ],
                                                             width=2, tags="pnl-con-"+str(ctr)+"-LVDS",fill="orange"))
            self.tempPnlTexts.append(self.makeText(self.tvCn, [int(self.x_padding+self.sb_connector_coordinates[i][0]*self.screen_rate),
                                                                int(self.y_padding+self.sb_connector_coordinates[i][1]*self.screen_rate)],
                                                                text = "LVDS"))
            ctr+=1

        #self.tempPnlRects.append(self.backplane)
        self.pnlClk = True

        self.isPnlAdded = True
        self.smtMoved = True

        self.loggerObj.updateLbl("panel Eklendi")

    def addMB(self, code):
        self.mbName = code
        with shelve.open(self.mbPath, writeback=True) as mbDb:
            mbIndex = mbDb['code'].index(code)
            if mbDb['selB'][mbIndex] == 3:
                mbRt = float(self.cm/st.mbCm)
                mbW = mbDb['xSize'][mbIndex]
                self.mbW = mbW
                mbH = mbDb['ySize'][mbIndex]
                self.mbH = mbH
                mbScrewCo = mbDb['screwCo'][mbIndex]
                mbConCo = mbDb['conCo'][mbIndex]
                self.tempMbRects = []
                self.tempMbOvals = []
                self.tempMbTexts = []
                print("Mainboard(cm) x and y:",mbW,mbH)
                print("Mainboard(pixel) x and y:",int(mbW*self.screen_rate),int(mbH*self.screen_rate))
                print("Screw coordinates(cm)",mbScrewCo[0][0],mbScrewCo[0][1])
                print("Screw coordinates(cm)",self.screen_rate*mbScrewCo[0][0],self.screen_rate*mbScrewCo[0][1])
                self.mainBoard = self.makeRect(self.tvCn,  [self.x_padding+int(self.mb_coordinate[0]*self.screen_rate),
                                                            self.y_padding+int(self.mb_coordinate[1]*self.screen_rate),
                                                            int(mbW*self.screen_rate)+self.x_padding+int(self.mb_coordinate[0]*self.screen_rate),
                                                            int(mbH*self.screen_rate)+self.y_padding+int(self.mb_coordinate[1]*self.screen_rate)], width = 2, tags = "mainboard", fill="green")
                self.tempMbRects.append(self.mainBoard)
                self.tempMbTexts.append(self.makeText(self.tvCn, [int(self.x_padding+mbW*self.screen_rate/2+self.mb_coordinate[0]*self.screen_rate),
                                                                    int(self.y_padding+mbH*self.screen_rate/2+self.mb_coordinate[1]*self.screen_rate)], text = "MainBoard", angle=0))
                for i in mbScrewCo:
                    self.tempMbRects.append(self.makeRect(self.tvCn, [int(self.x_padding+self.screen_rate*i[0]+self.mb_coordinate[0]*self.screen_rate)-3,
                                                                        int(self.y_padding+self.screen_rate*i[1]+self.mb_coordinate[1]*self.screen_rate)-3,
                                                                        int(self.x_padding+self.screen_rate*i[0]+self.mb_coordinate[0]*self.screen_rate)+3,
                                                                        int(self.y_padding+self.screen_rate*i[1]+self.mb_coordinate[1]*self.screen_rate)+3], width = 2, tags = "mbScrew"))
                ctr = 0
                for i in mbConCo:
                    # self.tempMbOvals.append(self.makeOval(self.tvCn, [i[0][0]-sc*2, i[0][1]-sc*2, i[0][0]+sc*2, i[0][1]+sc*2], width = 2, tags = "mbCons"))
                    self.tempMbOvals.append(self.makeOval(self.tvCn, [int(self.x_padding+self.screen_rate*i[0][0]+self.mb_coordinate[0]*self.screen_rate)-4,
                                                                        int(self.y_padding+self.screen_rate*i[0][1]+self.mb_coordinate[1]*self.screen_rate)-4,
                                                                        int(self.x_padding+self.screen_rate*i[0][0]+self.mb_coordinate[0]*self.screen_rate)+4,
                                                                        int(self.y_padding+self.screen_rate*i[0][1]+self.mb_coordinate[1]*self.screen_rate)+4], width = 2, tags = "mb-con-"+str(ctr)+"-"+i[1],fill="orange"))
                    self.tempMbTexts.append(self.makeText(self.tvCn, [int(self.x_padding+self.screen_rate*i[0][0]+self.mb_coordinate[0]*self.screen_rate),
                                                                        int(self.y_padding+self.screen_rate*i[0][1]+self.mb_coordinate[1]*self.screen_rate)], text = i[1]))
                    ctr += 1
            else:
                #mbRt = float(self.cm/st.mbCm)

                mbCm = float( mbDb['imgSX'][mbIndex] / mbDb['xSize'][mbIndex] )
                mbRt = float(self.cm/mbCm)
                mbW = mbDb['xSize'][mbIndex]*self.cm
                mbH = mbDb['ySize'][mbIndex]*self.cm
                mbScrewCo = []
                for i in mbDb['from_img_screws'][mbIndex]:
                    newX = int(float((i[0][0]-mbCm/2)*mbRt))
                    newY = int(float((i[0][1]-mbCm/2)*mbRt))
                    mbScrewCo.append([int(self.refX+newX+self.cm/2),int(self.refY+newY+self.cm/2)])
                mbConCo = []
                for i in mbDb['from_img_conns'][mbIndex]:
                    newX = int(float(((i[0][0]+i[0][2])/2-mbCm/2)*mbRt))
                    newY = int(float(((i[0][1]+i[0][3])/2-mbCm/2)*mbRt))
                    mbConCo.append([[int(self.refX+newX+self.cm/2),int(self.refY+newY+self.cm/2)],i[1]])
                self.tempMbRects = []
                self.tempMbOvals = []
                self.tempMbTexts = []
                sc = int(self.cm/4)
                self.mainBoard = self.makeRect(self.tvCn,  [self.refX, self.refY, self.refX + mbW, self.refY + mbH], width = 2, tags = "mainboard", fill = "green")
                print("full File name is: ", 'PCBs/Cropped/' + mbDb['fullFileName'][mbIndex])
                # mbPic = (Image.open('PCBs/Cropped/' + mbDb['fullFileName'][mbIndex]))
                # mbPic = ImageTk.PhotoImage(file = 'PCBs/Cropped/' + mbDb['fullFileName'][mbIndex])
                # resized_mbPic = mbPic.resize((int(mbW+self.cm), int(mbH + self.cm)), Image.ANTIALIAS)
                # new_resized_image = ImageTk.PhotoImage(resized_mbPic)
                # self.tvCn.create_image(self.refX, self.refY, image = new_resized_image, anchor='nw')
                self.tempMbRects.append(self.mainBoard)
                self.tempMbTexts.append(self.makeText(self.tvCn, [int(self.refX+mbW/2),int(self.refY+mbH/2)], text = "MainBoard", angle=0))
                for i in mbScrewCo:
                    self.tempMbRects.append(self.makeRect(self.tvCn, [i[0]-sc, i[1]-sc, i[0]+sc, i[1]+sc], width = 2, tags = "mbScrew"))
                ctr = 0
                for i in mbConCo:
                    # self.tempMbOvals.append(self.makeOval(self.tvCn, [i[0][0]-sc*2, i[0][1]-sc*2, i[0][0]+sc*2, i[0][1]+sc*2], width = 2, tags = "mbCons"))
                    self.tempMbOvals.append(self.makeOval(self.tvCn, [i[0][0]-sc*2, i[0][1]-sc*2, i[0][0]+sc*2, i[0][1]+sc*2], width = 2, tags = "mb-con-"+str(ctr)+"-"+i[1]))
                    self.tempMbTexts.append(self.makeText(self.tvCn, [i[0][0],i[0][1]], text = i[1]))
                    ctr += 1
        mbDb.close()
        self.isMbAdded = True
        self.smtMoved = True
        self.tvCn.tag_bind(self.mainBoard, '<Button-1>', self.mbClk)

        self.loggerObj.updateLbl("mainBoard Eklendi")

    def addUrsa(self, code):
        self.ursaName = code
        with shelve.open(self.ursaPath, writeback=True) as mbDb:
            mbIndex = mbDb['code'].index(code)
            mbRt = float(self.cm/st.mbCm)
            mbW = mbDb['xSize'][mbIndex]
            self.ursaW = mbW
            mbH = mbDb['ySize'][mbIndex]
            self.ursaH = mbH
            mbScrewCo = mbDb['screwCo'][mbIndex]
            mbConCo = mbDb['conCo'][mbIndex]
            self.tempUrRects = []
            self.tempUrOvals = []
            self.tempUrTexts = []
            if len(self.ursa_coordinate)==0:
                self.ursa_x_padding=self.x_padding
                self.ursa_y_padding=self.y_padding
            else:
                self.ursa_x_padding=self.x_padding+self.screen_rate*self.ursa_coordinate[0]
                self.ursa_y_padding=self.y_padding+self.screen_rate*self.ursa_coordinate[1]
            self.ursa = self.makeRect(self.tvCn,  [self.ursa_x_padding,
                                                    self.ursa_y_padding,
                                                    int(mbW*self.screen_rate)+self.ursa_x_padding,
                                                    int(mbH*self.screen_rate)+self.ursa_y_padding], width = 2, tags = "ursa", fill="#010fff010")
            self.tempUrRects.append(self.ursa)
            self.tempUrTexts.append(self.makeText(self.tvCn, [int(self.ursa_x_padding+mbW*self.screen_rate/2),int(self.ursa_y_padding+mbH*self.screen_rate/2)], text = "Ursa", angle=0))
            for i in mbScrewCo:
                self.tempUrRects.append(self.makeRect(self.tvCn, [int(self.ursa_x_padding+self.screen_rate*i[0])-3,
                                                                    int(self.ursa_y_padding+self.screen_rate*i[1])-3,
                                                                    int(self.ursa_x_padding+self.screen_rate*i[0])+3,
                                                                    int(self.ursa_y_padding+self.screen_rate*i[1])+3], width = 2, tags = "urScrew"))
            ctr = 0
            for i in mbConCo:
                self.tempUrOvals.append(self.makeOval(self.tvCn, [int(self.ursa_x_padding+self.screen_rate*i[0][0])-4,
                                                                    int(self.ursa_y_padding+self.screen_rate*i[0][1])-4,
                                                                    int(self.ursa_x_padding+self.screen_rate*i[0][0])+4,
                                                                    int(self.ursa_y_padding+self.screen_rate*i[0][1])+4], width = 2, tags = "ur-con-"+str(ctr)+"-"+i[1],fill="orange"))
                self.tempUrTexts.append(self.makeText(self.tvCn, [int(self.ursa_x_padding+self.screen_rate*i[0][0]),int(self.ursa_y_padding+self.screen_rate*i[0][1])], text = i[1]))
                ctr += 1
        mbDb.close()
        self.isUrsaAdded = True
        self.smtMoved = True
        self.tvCn.tag_bind(self.ursa, '<Button-1>', self.ursaClk)

        self.loggerObj.updateLbl("ursa Eklendi")

    def addPSU(self, code):
        self.psuName = code
        with shelve.open(self.psuPath, writeback=True) as mbDb:
            mbIndex = mbDb['code'].index(code)
            mbRt = float(self.cm/st.mbCm)
            mbW = mbDb['xSize'][mbIndex]
            self.psuW = mbW
            mbH = mbDb['ySize'][mbIndex]
            self.psuH = mbH
            mbScrewCo = mbDb['screwCo'][mbIndex]
            mbConCo = mbDb['conCo'][mbIndex]
            self.tempPsuRects = []
            self.tempPsuOvals = []
            self.tempPsuTexts = []
            if len(self.psu_coordinate)==0:
                self.psu_x_padding=self.x_padding
                self.psu_y_padding=self.y_padding
            else:
                self.psu_x_padding=self.x_padding+self.screen_rate*self.psu_coordinate[0]
                self.psu_y_padding=self.y_padding+self.screen_rate*self.psu_coordinate[1]
            self.psu = self.makeRect(self.tvCn,  [self.psu_x_padding, self.psu_y_padding, int(mbW*self.screen_rate)+self.psu_x_padding, int(mbH*self.screen_rate)+self.psu_y_padding], width = 2, tags = "psu", fill="#111fff080")
            self.tempPsuRects.append(self.psu)
            self.tempPsuTexts.append(self.makeText(self.tvCn, [int(self.psu_x_padding+mbW*self.screen_rate/2),int(self.psu_y_padding+mbH*self.screen_rate/2)], text = "PSU", angle=0))
            for i in mbScrewCo:
                self.tempPsuRects.append(self.makeRect(self.tvCn, [int(self.psu_x_padding+self.screen_rate*i[0])-3,
                                                                    int(self.psu_y_padding+self.screen_rate*i[1])-3,
                                                                    int(self.psu_x_padding+self.screen_rate*i[0])+3,
                                                                    int(self.psu_y_padding+self.screen_rate*i[1])+3], width = 2, tags = "psuScrew"))
            ctr = 0
            for i in mbConCo:
                self.tempPsuOvals.append(self.makeOval(self.tvCn, [int(self.psu_x_padding+self.screen_rate*i[0][0])-4,
                                                                    int(self.psu_y_padding+self.screen_rate*i[0][1])-4,
                                                                    int(self.psu_x_padding+self.screen_rate*i[0][0])+4,
                                                                    int(self.psu_y_padding+self.screen_rate*i[0][1])+4], width = 2, tags = "psu-con-"+str(ctr)+"-"+i[1],fill="orange"))
                self.tempPsuTexts.append(self.makeText(self.tvCn, [int(self.psu_x_padding+self.screen_rate*i[0][0]),int(self.psu_y_padding+self.screen_rate*i[0][1])], text = i[1]))
                ctr += 1
        mbDb.close()
        self.isPsuAdded = True
        self.smtMoved = True
        self.tvCn.tag_bind(self.psu, '<Button-1>', self.psuClk)

        self.loggerObj.updateLbl("PSU Eklendi")

    def addTcon(self, code):
        with shelve.open(self.tconPath, writeback=True) as mbDb:
            mbIndex = mbDb['code'].index(code)
            mbRt = float(self.cm/st.mbCm)
            mbW = mbDb['xSize'][mbIndex]*self.cm
            mbH = mbDb['ySize'][mbIndex]*self.cm
            mbScrewCo = []
            for i in mbDb['screwCo'][mbIndex]:
                newX = int(float((i[0]-st.mbCm)*mbRt))
                newY = int(float((i[1]-st.mbCm)*mbRt))
                mbScrewCo.append([self.refX+newX,self.refY+newY])
            mbConCo = []
            for i in mbDb['conCo'][mbIndex]:
                newX = int(float((i[0][0]-st.mbCm)*mbRt))
                newY = int(float((i[0][1]-st.mbCm)*mbRt))
                mbConCo.append([[self.refX+newX,self.refY+newY],i[1]])
            self.tempTconRects = []
            self.tempTconOvals = []
            self.tempTconTexts = []
            sc = int(self.cm/4)
            self.tcon = self.makeRect(self.tvCn, [self.refX, self.refY, self.refX + mbW, self.refY + mbH], width = 2, tags = "tcon", fill="#311fff000")
            self.tempTconRects.append(self.tcon)
            self.tempTconTexts.append(self.makeText(self.tvCn, [int(self.refX+mbW/2),int(self.refY+mbH/2)], text = "T-CON", angle=0))
            for i in mbScrewCo:
                self.tempTconRects.append(self.makeRect(self.tvCn, [i[0]-sc, i[1]-sc, i[0]+sc, i[1]+sc], width = 2, tags = "tconScrew"))
            ctr = 0
            for i in mbConCo:
                self.tempTconOvals.append(self.makeOval(self.tvCn, [i[0][0]-sc*2, i[0][1]-sc*2, i[0][0]+sc*2, i[0][1]+sc*2], width = 2, tags = "tcon-con-"+str(ctr)+"-"+i[1]))
                self.tempTconTexts.append(self.makeText(self.tvCn, [i[0][0],i[0][1]], text = i[1]))
                ctr += 1
        mbDb.close()
        self.isTconAdded = True
        self.smtMoved = True
        self.tvCn.tag_bind(self.tcon, '<Button-1>', self.tconClk)

        self.loggerObj.updateLbl("T-Con Eklendi")

    def addCable(self):
        if self.isMbAdded and not self.isZoomed:
            if not self.cblAdded:
                delArr(self.tvCn, self.tempInitCblCons)
                self.cblAdded = True
                self.detCnOn = True
            self.cableMode = True

            self.loggerObj.updateLbl("Kablolamaya Başlayın. Elektronik KArtların üzerindeki konektör bölgelerine gelince kırmızı konektörler belirginleşecek.")
            self.loggerObj.addTxtDown("Hangi konektör olduğu ise üzerinde yazıyor. Konektörün üzerine gelip bir kez tıkladığınızda kablolama işlemine başlarsınız. Başladıktan sonra")
            self.loggerObj.addTxtDown("kabloya kıvrım vermek istediğiniz bölgelerde tekrar tıklayın ve kabloyu yerleştirmek istediğiniz aynı tipteki ikinci konektöre tıkladığınızda işlem tamalanacaktır.")
            self.loggerObj.addTxtUp("burda ",
            " bi test ", " yaptık", "bakalım ", " oldu mu?")
        else:
            print("cable a giremedi")

    def updCblCons(self):
        sc = int(self.cm/2)
        delArr(self.tvCn, self.tempInitCblCons)
        for i in self.tempPnlOvals:
            if 'pnl-con-' in self.tvCn.gettags(i)[0]:
                cor = self.tvCn.coords(i)
                self.tempInitCblCons.append([cor,self.tvCn.gettags(i)[0]])
        if self.isMbAdded:
            for i in self.tempMbOvals:
                if 'mb-con-' in self.tvCn.gettags(i)[0]:
                    cor = self.tvCn.coords(i)
                    self.tempInitCblCons.append([cor,self.tvCn.gettags(i)[0]])
                # ctr += 1
        if self.isUrsaAdded:
            for i in self.tempUrOvals:
                if 'ur-con-' in self.tvCn.gettags(i)[0]:
                    cor = self.tvCn.coords(i)
                    self.tempInitCblCons.append([cor,self.tvCn.gettags(i)[0]])

        if self.isPsuAdded:
            for i in self.tempPsuOvals:
                if 'psu-con-' in self.tvCn.gettags(i)[0]:
                    cor = self.tvCn.coords(i)
                    self.tempInitCblCons.append([cor,self.tvCn.gettags(i)[0]])

        if self.isTconAdded:
            for i in self.tempTconOvals:
                if 'tcon-con-' in self.tvCn.gettags(i)[0]:
                    cor = self.tvCn.coords(i)
                    self.tempInitCblCons.append([cor,self.tvCn.gettags(i)[0]])

    def reScrew(self, arr):
        newArr = []
        for i in arr:
            newX = int((i[0]-16)/self.scRate)
            newY = int((i[1]-9)/self.scRate)
            newArr.append([self.refX+newX,self.refY+newY])
        return newArr

    def reCon(self, arr):
        newArr = []
        ctr = 0
        for i in arr:
            newX = int((i[0][0]-16)/self.scRate)
            newY = int((i[0][1]-9)/self.scRate)
            # newArr.append([[self.refX+newX,self.refY+newY],"pnl-con-" + str(ctr) + "-" + i[1]])
            newArr.append([[self.refX+newX,self.refY+newY],i[1]])
            ctr += 1
        return newArr

    def reText(self, arr):
        newArr = []
        for i in arr:
            newX = int((i[0][0]-16)/self.scRate)
            newY = int((i[0][1]-9)/self.scRate)
            newArr.append([[self.refX+newX,self.refY+newY],i[1]])
        return newArr

    def getIndex(self, code):
        with shelve.open(self.pPath, writeback=True) as pnlDb:
            self.Index = pnlDb['kabin_code'].index(code)
        pnlDb.close()

    def getInfo(self, index):
        with shelve.open(self.pPath, writeback=True) as pnlDb:
            self.inch = int(pnlDb['inch'][index])
            print("inch=",self.inch)
            self.kabin_code = pnlDb['kabin_code'][index]  #kabin code
            self.panel_code = pnlDb['panel_code'][index]
            self.SB_rectangles = pnlDb['SB_coordinates'][index]
            print("SB_coordinates=",self.SB_rectangles)
            self.sb_connector_coordinates = pnlDb['sb_lvds_connector_coordinates'][index]
            print("sb_lvds_connector_coordinates=",self.sb_connector_coordinates)
            self.mb_coordinate = pnlDb['mb_coordinate'][index]
            print("mb_coordinate=",self.mb_coordinate)
            try:
                self.psu_coordinate = pnlDb['psu_coordinate'][index]
                print("psu_coordinate=",self.psu_coordinate)
            except:
                self.psu_coordinate = []
            try:
                self.ursa_coordinate = pnlDb['ursa_coordinate'][index]
                print("ursa_coordinate=",self.ursa_coordinate)
            except:
                self.ursa_coordinate = []
            try:
                self.tcon_coordinates = pnlDb['TCON_coordinates'][index]
                print("TCON_coordinates=",self.tcon_coordinates)
                self.screw_coordinates = pnlDb['screw_coordinates'][index]
                print("TCON_screw_coordinates=",self.screw_coordinates)
                self.tcon_lvds_connector_coordinates = pnlDb['tcon_lvds_connector_coordinates'][index]
                print("TCON_LVDS_connector_coordinates=",self.tcon_lvds_connector_coordinates)
            except:
                self.tcon_coordinates = []
                self.screw_coordinates = []
                self.tcon_lvds_connector_coordinates = []
            try:
                self.tcon_dc_connector_coordinates = pnlDb['tcon_dc_connector_coordinates'][index]
            except:
                self.tcon_dc_connector_coordinates = []
            print("tcon_dc_connector_coordinates=",self.tcon_dc_connector_coordinates)


            #INCH bilgisinden panelin x ve y uzunluğu cm cinsinden bulunur. Daha sonra x uzunluğu 800 y uzunluğu 450 olacak şekilde oran bulunur--> oran = 800/x_cm = 450/y_cm
            #Bu oran belirlendikten sonra cm cinsinden olan koordinatlarının çevrimi için sırasıyla şu adımlar uygulanır:
                # 1 - x ve y koordinatları oran ile çarpılarak pixel karşılığı bulunur.
                # 2 - Üzerinde çalışılan kanvas 900,500 boyutlarında olduğu için çizim yapılacak frame in biraz içeride olması istenmektedir.......
                # ......... bu sebeple ekrana bir şey çizdirirken bütün x kordinatlarına 50, bütün y koordinatlarına 25 eklenecektir.
                # 3 - Geri dönüşüm yapılırken de yukardaki işlemler tersine uygulanacaktır.
            self.X_cm = self.inch*2.54*0.871
            self.Y_cm = self.inch*2.54*0.49
            self.screen_rate = 800/self.X_cm

    def saveMaterials(self):
        # self.tempMbRects  #screws and mainboard
        # self.tempMbOvals  #mainboard connectors
        # self.realCblObjs  # cables
        # self.tempPsuRects #psu screws and psu
        # self.tempPsuOvals #psu connectors
        # self.emiTapeRects #emitapes with tags
        # bunu cm olarak kaydetmemiz tamamlamamız lazım şimdilik öylesine yapıyorum
        self.tvConfigName = "pnl_"+self.panelName+"-"+"mb_"+self.mbName
        if self.isPsuAdded:
            self.tvConfigName += ("-psu_" + self.psuName)
        if self.isUrsaAdded:
            self.tvConfigName += ("-ursa_" + self.ursaName)
        
        mbScrewCords = []
        mbCords = []
        mbConCords = []
        for i in range(len(self.tempMbRects)):
            print("len(self.tempMbRects): ", len(self.tempMbRects))
            if "Screw" in self.tvCn.itemcget(self.tempMbRects[i], "tags"):
                print("screw found in tags")
                cord = self.tvCn.coords(self.tempMbRects[i])
                print("cord: ", cord)
                mbScrewCords.append([int((cord[0] + cord[2])/2) , int((cord[1] + cord[3])/2)]) # [x1,y1]
            if "mainboard" in self.tvCn.itemcget(self.tempMbRects[i], "tags"):
                print("self.tvCn.coords(self.tempMbRects[i]): ", self.tvCn.coords(self.tempMbRects[i]))
                mbCords.append(self.tvCn.coords(self.tempMbRects[i])) # [[x1,y1,x2,y2]]
        print("len(self.tempMbOvals): ", len(self.tempMbOvals))
        for i in range(len(self.tempMbOvals)):
            if "-con" in self.tvCn.itemcget(self.tempMbOvals[i], "tags"):
                print("con found in tags")
                cord = self.tvCn.coords(self.tempMbOvals[i])
                tagX = self.tvCn.itemcget(self.tempMbOvals[i], "tags")
                mbConCords.append([[int((cord[0] + cord[2])/2) , int((cord[1] + cord[3])/2)], tagX.split('-')[-1]])  #[[x1,y1], 'DC']
        self.mbScrewCords = mbScrewCords
        print("self.mbScrewCords: ", self.mbScrewCords)
        self.mbCords = mbCords[0]
        print("self.mbCords: ", self.mbCords)
        self.mbConCords = mbConCords
        print("self.mbConCords: ", self.mbConCords)
        
        psuScrewCords = []
        psuCords = []
        psuConCords = []
        
        if self.isPsuAdded:
            print("self.isPsuAdded: ", self.isPsuAdded)
            print("len(self.tempPsuRects): ", len(self.tempPsuRects))
            for i in range(len(self.tempPsuRects)):
                if "Screw" in self.tvCn.itemcget(self.tempPsuRects[i], "tags"):
                    print("screw found in tags")
                    cord = self.tvCn.coords(self.tempPsuRects[i])
                    print("cord: ", cord)
                    psuScrewCords.append([int((cord[0] + cord[2])/2) , int((cord[1] + cord[3])/2)]) # [x1,y1]
                if "psu" in self.tvCn.itemcget(self.tempPsuRects[i], "tags"):
                    print("self.tvCn.coords(self.tempPsuRects[i]): ", self.tvCn.coords(self.tempPsuRects[i]))
                    psuCords.append(self.tvCn.coords(self.tempPsuRects[i])) # [[x1,y1,x2,y2]]
            print("len(self.tempPsuOvals): ", len(self.tempPsuOvals))
            for i in range(len(self.tempPsuOvals)):
                if "-con" in self.tvCn.itemcget(self.tempPsuOvals[i], "tags"):
                    print("con found in tags")
                    cord = self.tvCn.coords(self.tempPsuOvals[i])
                    tagX = self.tvCn.itemcget(self.tempPsuOvals[i], "tags")
                    psuConCords.append([[int((cord[0] + cord[2])/2) , int((cord[1] + cord[3])/2)], tagX.split('-')[-1]])  #[[x1,y1], 'DC']
            self.psuScrewCords = psuScrewCords
            self.psuCords = psuCords[0]
            self.psuConCords = psuConCords
 

        
        ursaScrewCords = []
        ursaCords = []
        ursaConCords = []
        if self.isUrsaAdded:
            for i in range(len(self.tempUrRects)):
                if "Screw" in self.tvCn.itemcget(self.tempUrRects[i], "tags"):
                    cord = self.tvCn.coords(self.tempUrRects[i])
                    ursaScrewCords.append([int((cord[0] + cord[2])/2) , int((cord[1] + cord[3])/2)]) # [x1,y1]
                if "ursa" in self.tvCn.itemcget(self.tempUrRects[i], "tags"):
                    ursaCords.append(self.tvCn.coords(self.tempUrRects[i])) # [[x1,y1,x2,y2]]
            for i in range(len(self.tempUrOvals)):
                if "-con" in self.tvCn.itemcget(self.tempUrOvals[i], "tags"):
                    cord = self.tvCn.coords(self.tempUrOvals[i])
                    tagX = self.tvCn.itemcget(self.tempUrOvals[i], "tags")
                    ursaConCords.append([[int((cord[0] + cord[2])/2) , int((cord[1] + cord[3])/2)], tagX.split('-')[-1]])  #[[x1,y1], 'DC']
            self.ursaScrewCords = ursaScrewCords
            self.ursaCords = ursaCords[0]
            self.ursaConCords = ursaConCords
            
        obj = tvcDb()
        obj.addMb(self)
        print(self.__dict__)
        obj.showSome()
        del obj
                
    def printAll(self):
        print("all: ", self.xS, self.yS, self.xBH, self.xBPN, self.refX, self.refY)
        print("conCo:", self.conCo)

    def makeRect(self, Cn, *cor, **args):
        return Cn.create_rectangle([cor, args])

    def makeTempRect(self, Cn, arr, *cor, **args):
        return Cn.create_rectangle([cor, args])

    def makeOval(self, Cn, *cor, **args):
        return Cn.create_oval([cor, args])

    def makeTempOval(self, Cn, arr, *cor, **args):
        return Cn.create_oval([cor, args])

    def makeText(self, Cn, *cor, **args):
        return Cn.create_text([cor, args])

    def makeTempText(self, Cn, arr, *cor, **args):
        return Cn.create_text([cor, args])

def delArr(Cnv, Arr):
    for i in Arr:
        Cnv.delete(i)
    Arr.clear()
    del Arr[:]

if __name__ == "__main__":
    app = SampleApp()

    app.mainloop()
