# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import *
import shelve
from classes.settings import Settings as st
from pathlib import Path
import logging

class TVConfigDatabase():
    def __init__(self):
        self.isDbExist = False
        isDbTended = False
        p = Path(__file__).parents[2]
        self.path = os.path.join(p, 'mem\\tvcDb')
        try:
            print("bu path: ", self.path)
            with shelve.open(self.path, writeback=True) as mbDb:
                self.makeDb()
        except Exception as e:
            print("makeDb çalışmadı")
            print(e)


    def makeDb(self):
        mbDb = shelve.open(self.path, writeback=True)
        if ('ferriteTags' not in mbDb):
            with shelve.open(self.path, writeback=True) as mbDb:
                mbDb['tvConfigCode'] = []  
                mbDb['mbCode'] = []  
                mbDb['mbRotNum'] = []  
                mbDb['mbDrag'] = []  
                mbDb['mbCords'] = [] 
                mbDb['pnlCode'] = [] 
                mbDb['mbScrewCords'] = []
                mbDb['mbConCords'] = []
                
                mbDb['isPsuAdded'] = []
                mbDb['isUrsaAdded'] = []
                mbDb['isTconAdded'] = []

                mbDb['psuCode'] = []  
                mbDb['psuRotNum'] = []  
                mbDb['psuDrag'] = []  
                mbDb['psuCords'] = [] 
                mbDb['psuScrewCords'] = []
                mbDb['psuConCords'] = []
                
                mbDb['ursaCode'] = []  
                mbDb['ursaRotNum'] = []  
                mbDb['ursaDrag'] = []  
                mbDb['ursaCords'] = [] 
                mbDb['ursaScrewCords'] = []
                mbDb['ursaConCords'] = []
                
                mbDb['cableShapes'] = []
                mbDb['cableShields'] = []
                mbDb['cableTypes'] = []
                mbDb['cableColors'] = []
                mbDb['cableWidths'] = []
                mbDb['cableCords'] = []
                mbDb['cableTransparencies'] = []
                mbDb['cableTags'] = []
                
                mbDb['emiTapeCords'] = []
                mbDb['emiTapeTags'] = []

                mbDb['ferriteCords'] = []
                mbDb['ferriteTags'] = []
                
        else:
            self.tenDb()
        mbDb.close()
        self.mbDb = mbDb
        print("DB oluşturuldu")
        
    def tendDb(self):
        print("tendDB ye girdi")
        with shelve.open(self.path, writeback=True) as mbDb:
            maxElementLen = 0
            minElementLen = 1
            for i in mbDb.keys():
                if len(mbDb[i]) > maxElementLen:
                    maxElementLen = len(mbDb[i])
            for i in mbDb.keys():
                if len(mbDb[i]) < maxElementLen:
                    diff = maxElementLen - len(mbDb[i])
                    for k in range(diff):
                        mbDb[i].append(None)
                    print(i, " dizinine ", diff, " kadar None eklendi")
        mbDb.close()

##    @staticmethod
    def addMb(self, mb):
        try:
##            mbDb = shelve.open(self.path, writeback=True)
            with shelve.open(self.path, writeback=True) as mbDb:
                print("get in addMb")
                verNum = 0
                for i in mbDb['tvConfigCode']:
                    if mb.tvConfigName+"-ver_" in i:
                        tempVerNum = int(i.split("-ver_")[-1])
                        if tempVerNum > verNum:
                            verNum = tempVerNum
                mbDb['tvConfigCode'].append(mb.tvConfigName + "-ver_" + str(verNum + 1))
                print("tvConfigCode: ", mb.tvConfigName + "-ver_" + str(verNum + 1))
                mbDb['mbCode'].append(mb.mbName)
                print("mbName: ", mb.mbName)
                mbDb['mbRotNum'].append(mb.mbRotation)
                print("mbRotation: ", mb.mbRotation)
                mbDb['mbDrag'].append(mb.mbDrag)
                print("mbDrag: ", mb.mbDrag)
                mbDb['mbCords'].append(mb.mbCords)
                print("mbCords: ", mb.mbCords)
                mbDb['pnlCode'].append(mb.panelName)
                print("panelName: ", mb.panelName)
                mbDb['mbScrewCords'].append(mb.mbScrewCords)
                print("mbScrewCords: ", mb.mbScrewCords)
                mbDb['mbConCords'].append(mb.mbConCords)
                print("mbConCords: ", mb.mbConCords)
                
                mbDb['isPsuAdded'].append(mb.isPsuAdded)
                mbDb['isUrsaAdded'].append(mb.isUrsaAdded)
                mbDb['isTconAdded'].append(mb.isTconAdded)
                
                mbDb['psuCode'].append(mb.psuName) 
                mbDb['psuRotNum'].append(mb.psuRotation)
                mbDb['psuDrag'].append(mb.psuDrag)
                mbDb['psuCords'].append(mb.psuCords)
                mbDb['psuScrewCords'].append(mb.psuScrewCords)
                mbDb['psuConCords'].append(mb.psuConCords)
                
                mbDb['ursaCode'].append(mb.ursaName)
                mbDb['ursaRotNum'].append(mb.ursaRotation)
                mbDb['ursaDrag'].append(mb.ursaDrag)
                mbDb['ursaCords'].append(mb.ursaCords)
                mbDb['ursaScrewCords'].append(mb.ursaScrewCords)
                mbDb['ursaConCords'].append(mb.ursaConCords)
                
                cableShapes = []
                cableShields = []
                cableTypes = []
                cableColors = []
                cableWidths = []
                cableCords = []
                cableTransparencies = []
                cableTags = []
                for i in range(len(mb.realCblObjs)):
                    cableShapes.append(mb.realCblObjs[i][0].shape)
                    cableShields.append(mb.realCblObjs[i][0].shield)
                    cableTypes.append(mb.realCblObjs[i][0]._type)
                    cableColors.append(mb.realCblObjs[i][0].color)
                    cableWidths.append(mb.realCblObjs[i][0].width)
                    cableCords.append(mb.realCblObjs[i][2].cblCords)
                    cableTransparencies.append(mb.realCblObjs[i][2].trnsLst)
                    cableTags.append(mb.realCblObjs[i][1][0]+"-"+mb.realCblObjs[i][1][1][0]+"-"+mb.realCblObjs[i][1][1][1])  
                mbDb['cableShapes'].append(cableShapes)
                mbDb['cableShields'].append(cableShields)
                mbDb['cableTypes'].append(cableTypes)
                mbDb['cableColors'].append(cableColors)
                mbDb['cableWidths'].append(cableWidths)
                mbDb['cableCords'].append(cableCords)
                mbDb['cableTransparencies'].append(cableTransparencies)
                mbDb['cableTags'].append(cableTags)
                
                mbDb['emiTapeCords'].append(mb.emiTapeCords)
                mbDb['emiTapeTags'].append(mb.emiTapeTags)
                
                mbDb['ferriteCords'].append(mb.ferriteCords)
                mbDb['ferriteTags'].append(mb.ferriteTags)
                
            mbDb.close()
        except Exception as e:
            print("addMb çalışmadı")
            print(e)

##    @staticmethod
    def showSome(self):
        with shelve.open(self.path) as mbDb:
            for i in mbDb.keys():
                print("column ", i, " length: ", len(mbDb[i]))
            for i in mbDb.keys():
                print("column ", i, " elements: ")
                for k in range(len(mbDb[i])):
                    print(mbDb[i][k])
        mbDb.close()
  

if __name__ == "__main__":
    app = SampleApp()
    
    app.mainloop()
