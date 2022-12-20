# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import *
import shelve
from classes.settings import Settings as st
from pathlib import Path

class MainboardDatabase():
    def __init__(self):
        self.isDbExist = False
        isDbTended = False
        p = Path(__file__).parents[2]
        self.path = os.path.join(p, 'mem\\mbDb')
        try:
            print("bu path: ", self.path)
            with shelve.open(self.path, writeback=True) as mbDb:
                if ('imgSY' not in mbDb):
                    self.isDbExist = False
                    self.makeDb()
                else:
                    self.tendDb()
        except:
            print("boyle bi db yok dolayısıyla yeni oluşturuluyor")
            self.makeDb()
            print("DB OLUŞTURULDU")


    def makeDb(self):
        mbDb = shelve.open(self.path, writeback=True)
        if ('imgSY' not in mbDb):
            with shelve.open(self.path, writeback=True) as mbDb:
                mbDb['code'] = []  #mainboard code 
                #AF
                mbDb['version'] = []  #version code
                #7
                mbDb['xSize'] = []  #width
                #21
                mbDb['ySize'] = []  #length
                #15
                mbDb['screwCo'] = []  #screw coordinates
                #[x,y]
                mbDb['conCo'] = []  #connector coordinates with types
                #[[x,y],usb]
                mbDb['inc'] = []  #includes
                # tcon + leddriver
                mbDb['selB'] = [] #the mb import selection is it manual or from image
                # selB == 1 or 2 is manual 3 is image import derivative
                mbDb['from_img_conns'] = [] #the mb from image with all connectors
                # coordinates of the connectors and their types like [[x1,y1,x2,y2],'usb']
                mbDb['from_img_screws'] = [] #the mb from image with all screws
                # coordinates of the connectors and their radius [[x,y], radius]
                mbDb['fullFileName'] = []
                # mbPic = ImageTk.PhotoImage(file = 'PCBs/Cropped/' + self.fullFileName)
                # mbCn.create_image(0, 0, image=mbPic, anchor='nw')
                mbDb['imgSX'] = []
                # pixel width of the image iöported MB
                mbDb['imgSY'] = []
                # pixel height of the image iöported MB
        mbDb.close()
        self.mbDb = mbDb
        print("DB oluşturuldu")
        
    def tendDb(self):
        print("Henüz bu fonksiyon yazılmadı")

##    @staticmethod
    def addMb(self, mb):
        try:
##            mbDb = shelve.open(self.path, writeback=True)
            with shelve.open(self.path, writeback=True) as mbDb:
                print("before code")
                mbDb['code'].append(mb.code)
                print("after code")
                mbDb['version'].append(mb.version)
                mbDb['xSize'].append(mb.xS)
                mbDb['ySize'].append(mb.yS)
                mbDb['screwCo'].append(mb.screwCo)
                mbDb['conCo'].append(mb.conCo)
                mbDb['inc'].append(mb.includes)
                mbDb['selB'].append(mb.selB)
                mbDb['from_img_conns'].append(mb.from_img_conns)
                mbDb['from_img_screws'].append(mb.from_img_screws)
                mbDb['fullFileName'].append(mb.fullFileName)
                mbDb['imgSX'].append(mb.imgSX)
                mbDb['imgSY'].append(mb.imgSY)
            mbDb.close()
        except:
            print("adMb çalışmadı")

##    @staticmethod
    def showSome(self):
        with shelve.open(self.path) as mbDb:
            print("code: ")
            for i in mbDb['code']:
                print(i)
            print("version: ")
            for i in mbDb['version']:
                print(i)
            print("code okundu: ", mbDb['code'])
        mbDb.close()
  

if __name__ == "__main__":
    app = SampleApp()
    
    app.mainloop()
