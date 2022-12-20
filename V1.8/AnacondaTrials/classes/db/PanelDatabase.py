# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import *
import shelve
from classes.settings import Settings as st
from pathlib import Path

class PanelDatabase():
    def __init__(self):
        self.isDbExist = False
        isDbTended = False
        p = Path(__file__).parents[2]
        self.path = os.path.join(p, 'mem\\panelDb')
        try:
            print("bu path: ", self.path)
            with shelve.open(self.path, writeback=True) as mbDb:
                if ('mb_coordinate' not in mbDb):
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
        if ('mb_coordinate' not in mbDb):
            with shelve.open(self.path, writeback=True) as mbDb:
                mbDb['inch'] = []  #inch

                mbDb['kabin_code'] = []  #kabin code

                mbDb['panel_code'] = []  #panel kodu

                mbDb['screw_coordinates'] = []  #TCON screw center coordinates  [[x1,y1],[x2,y2].....]

                mbDb['tcon_lvds_connector_coordinates'] = []  #TCON LVDS connectors center coordinates [[x1,y1],[x2,y2]......]

                mbDb['tcon_dc_connector_coordinates'] = []  #TCON DC connectors center coordinates [[x1,y1],[x2,y2]......]

                mbDb['sb_lvds_connector_coordinates'] = []  #Sourceboard LVDS connectors center coordinates [[x1,y1],[x2,y2]......]

                mbDb['SB_coordinates'] = []  #Sourceboard coordinates left top and right bot [[[x1topleft,y1topleft],[x1botright,y1botright]],[[x2topleft,y2topleft],[x2botright,y2botright]].....

                mbDb['TCON_coordinates'] = []  #TCON coordinates left top and right bot [[x1,y1],[x2,y2]]

                mbDb['mb_coordinate'] = [] #Mainboard reference coordinate left top corner

                mbDb['psu_coordinate'] = [] #PSU reference coordinate left top corner

                mbDb['ursa_coordinate'] = [] #URSA reference coordinate left top corner

                #konnektörü de eklicezz!!!!!!!!!!!!!!!!!
        mbDb.close()
        self.mbDb = mbDb
        print("DB oluşturuldu")

    def tendDb(self):
        print("Henüz bu fonksiyon yazılmadı")

##    @staticmethod
    def addPanel(self, mb):
        print("test-> cde / inch: ", mb.panel_code, mb.inch)
#        try:

##            mbDb = shelve.open(self.path, writeback=True)
        with shelve.open(self.path, writeback=True) as mbDb:
            mbDb['kabin_code'].append(mb.kabin_code)
            mbDb['inch'].append(mb.inch)
            mbDb['panel_code'].append(mb.panel_code)
            mbDb['sb_lvds_connector_coordinates'].append(mb.sb_connector_coordinates)
            mbDb['SB_coordinates'].append(mb.SB_coordinates)
            if mb.TCON_include:
                mbDb['TCON_coordinates'].append(mb.tcon_coordinates)
                mbDb['screw_coordinates'].append(mb.screw_coordinates)
                mbDb['tcon_lvds_connector_coordinates'].append(mb.connector_coordinates)
            if mb.TCON_DC_include:
                mbDb['tcon_dc_connector_coordinates'].append(mb.TCON_DC_coordinate)
            mbDb['mb_coordinate'].append(mb.mb_coordinate)
            if mb.psuFlag:
                mbDb['psu_coordinate'].append(mb.psu_coordinate)
            if mb.ursaFlag:
                mbDb['ursa_coordinate'].append(mb.ursa_coordinate)

        mbDb.close()
#        except:
#            print("addPanel çalışmadı")

##    @staticmethod
    def showSome(self):#YENİDEN DÜZENLENECEK!!!!!!!!!!!!!
        with shelve.open(self.path) as mbDb:
            print("code: ")
            for i in mbDb['code']:
                print(i)
            print("version: ")
            for i in mbDb['inch']:
                print(i)
            print("code okundu: ", mbDb['code'])
        mbDb.close()


if __name__ == "__main__":
    app = SampleApp()

    app.mainloop()
