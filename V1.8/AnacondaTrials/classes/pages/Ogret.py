# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import * 
from classes.settings import Settings as st
from classes.db.MainboardDatabase import MainboardDatabase as mbDb
import cv2
import matplotlib.pyplot as plt 
from matplotlib.patches import Circle
from PIL import ImageTk, Image
import datetime
import math
import tkinter.font as tkfont

global epoch
epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0
def dist_call(ev1, ev2, lim):
    dist_x = ev1[0] - ev2[0]
    dist_y = ev1[1] - ev2[1]
    if dist_x**2 + dist_y**2 > lim**2:
        return False
    else:
        return True



class MainboardGui():
    def __init__(self):
        mbTk = tk.Tk()
        mbTk.title("mainboard configuration")
        mbF = tk.Frame(mbTk)
        self.inputCheck = False
        self.screwCheck = False
        self.conCheck = False
        
        self.normal_font = tkfont.Font(family="Helvetica", size=12)
        self.bold_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        tk.Label(mbTk, text="code").grid(row = 1, column = 1)
        tk.Label(mbTk, text="version").grid(row = 2, column = 1)
        tk.Label(mbTk, text="x Size (cm)").grid(row = 3, column = 1)
        tk.Label(mbTk, text="y Size (cm)").grid(row = 4, column = 1)
        tk.Label(mbTk, text="screw Coordinates").grid(row = 5, column = 1)
        tk.Label(mbTk, text="connector Coordinates").grid(row = 6, column = 1)
        tk.Label(mbTk, text="Includes").grid(row = 7, column = 1)
        
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
        self.clickedOnce = False
        self.clikedTwice = False
        self.cm = st.mbCm
        self.tmpRec = None
        self.image_with_edges = None
        self.imgSX = None
        self.imgSY = None
        #For connector selection, mouse click determines the visual rectangles first and last coordinates
        self.recFrsEv = None
        self.recLstEv = None
        self.frstClkStt = False
        self.clkTime = 0
        self.rlsTime = 0
        global epoch
        self.is_in_con_sel = False
        self.from_img_conns = [] #coordinates of the connectors and their types like [[x1,y1,x2,y2],'usb']
        self.from_img_screws = [] #coordinates of the connectors and their radius [[x,y], radius]
        self.mb_con_rects = []
        self.tmp_con_cor = None
        self.conCor1 = None
        self.conCor2 = None
        self.is_in_screw_finding = False
        self.btnRlsBugReliever = False
        self.fullFileName = None
        
        tk.Button(mbTk, text="chose locations", command = lambda: self.locateScrews()).grid(row = 5, column = 2)
        tk.Button(mbTk, text="chose locations", command = lambda: self.locateCons()).grid(row = 6, column = 2)
        
        self.Checkbutton1 = tk.IntVar(mbTk)   
        self.Checkbutton2 = tk.IntVar(mbTk)   
        self.Checkbutton3 = tk.IntVar(mbTk) 
        self.Checkbutton4 = tk.IntVar(mbTk)
        self.Button1 = tk.Checkbutton(mbTk, text = "PSU",  
                              variable = self.Checkbutton1, 
                              onvalue = 1, 
                              offvalue = 0, 
                              height = 2, 
                              width = 10) 
          
        self.Button2 = tk.Checkbutton(mbTk, text = "LED Driver", 
                              variable = self.Checkbutton2, 
                              onvalue = 1, 
                              offvalue = 0, 
                              height = 2, 
                              width = 10) 
          
        self.Button3 = tk.Checkbutton(mbTk, text = "Ursa", 
                              variable = self.Checkbutton3, 
                              onvalue = 1, 
                              offvalue = 0, 
                              height = 2, 
                              width = 10)
        
        self.Button4 = tk.Checkbutton(mbTk, text = "T-con", 
                              variable = self.Checkbutton4, 
                              onvalue = 1, 
                              offvalue = 0, 
                              height = 2, 
                              width = 10) 
            
        self.Button1.grid(row = 7, column = 2)   
        self.Button2.grid(row = 8, column = 2)     
        self.Button3.grid(row = 9, column = 2)
        self.Button4.grid(row = 10, column = 2)
        self.includes = []


        tk.Button(mbTk, text="test", command = lambda: self.test()).grid(row = 11, column = 1)
        tk.Button(mbTk, text="Import From IMG", command = lambda: self.imp_img()).grid(row = 12, column = 1)
        tk.Button(mbTk, text="Save", command = lambda: self.save()).grid(row = 13, column = 1)
        
        self.mbTk = mbTk

    def _dont_run_at_con_select(func):
        def inner(self, *args, **kwargs):
            if not self.is_in_con_sel:
                print("self.is_in_con_sel is NOT ON")
                func(self, *args, **kwargs)
            else:
                print("self.is_in_con_sel is ON!")
        return inner

    def _dont_run_at_screw_finding(func):
        def inner(self, *args, **kwargs):
            if not self.is_in_screw_finding:
                print("self.is_in_screw_finding is NOT ON")
                func(self, *args, **kwargs)
            else:
                print("self.is_in_screw_finding is ON!")
        return inner

    def _dont_run_at_btnRlsBugReliever(func):
        def inner(self, *args, **kwargs):
            if not self.btnRlsBugReliever:
                print("self.btnRlsBugReliever is NOT ON")
                func(self, *args, **kwargs)
            else:
                print("self.btnRlsBugReliever is ON!")
        return inner
        
    def detect_edge(self, image):
        ''' function Detecting Edges '''
        
        # self.getSizes()
        
        broadWidth = self.xS
        broadHeight = self.yS
        
        image_with_edges = cv2.Canny(image , 50, 150)

        images = [image , image_with_edges]

        location = [121, 122]
        
        rowEdge = [0 for i in range(len(image_with_edges))]
        colEdge = [0 for i in range(len(image_with_edges[0]))]
        for rInd in range(len(image_with_edges)):
            tmp = 0;
            for i in range(len(image_with_edges[rInd])):
                rowEdge[rInd] += image_with_edges[rInd][i]/100
                colEdge[i] += image_with_edges[rInd][i]/100
        
        xCor1 = colEdge.index(max(colEdge[:int(len(colEdge)/3)]))
        # colEdge.pop(xCor1)
        tempArr = colEdge[int(len(colEdge)*2/3):]
        xCor2 = tempArr.index(max(colEdge[int(len(colEdge)*2/3):])) + int(len(colEdge)*2/3)
        for i in range(len(tempArr)-1):
            if tempArr[-(i+1)] >= colEdge[xCor2]/2:
                xCor2 = len(colEdge)-(i+1)
                break
        for i in range(int(len(colEdge)/3)):
            if colEdge[i] >= colEdge[xCor1]/2:
                xCor1 = i
                break
        
        yCor1 = rowEdge.index(max(rowEdge[:int(len(rowEdge)/3)]))
        tempArr = rowEdge[int(len(rowEdge)*2/3):]
        yCor2 = tempArr.index(max(rowEdge[int(len(rowEdge)*2/3):])) + int(len(rowEdge)*2/3)
        for i in range(len(tempArr)-1):
            if tempArr[-(i+1)] >= rowEdge[yCor2]/2:
                yCor2 = len(rowEdge)-(i+1)
                break
        for i in range(int(len(rowEdge)/3)):
            if rowEdge[i] >= rowEdge[yCor1]/2:
                yCor1 = i
                break
        
        xMin = min(xCor1, xCor2)
        xMax = max(xCor1, xCor2)
        yMin = min(yCor1, yCor2)
        yMax = max(yCor1, yCor2)
        
        refCm = (xMax- xMin) / broadWidth
        refCmY = (yMax- yMin) / broadHeight
        
        print("refCm X Y: ", refCm, " ", refCmY)
        
        boardWidth = (xMax - xMin) 
        boardHeight = (yMax- yMin)
        
        cv2.imwrite('PCBs/Edges/' + self.fName + '__edge.jpeg', image_with_edges)
        
        
        im = Image.open('PCBs/' + self.fullFileName)
        im_edge = Image.open('PCBs/Edges/' + self.fName + '__edge.jpeg')
        
        im = im.crop((int(xMin - refCm/2), int(yMin - refCm/2), int(xMax + refCm/2), int(yMax + refCm/2)))
        im_edge = im_edge.crop((int(xMin - refCm/2), int(yMin - refCm/2), int(xMax + refCm/2), int(yMax + refCm/2)))
        
        im.save('PCBs/Cropped/' + self.fullFileName)
        im_edge.save('PCBs/Cropped/' + self.fName + '__edge.jpeg')
        
        img_edg = cv2.imread('PCBs/Cropped/' + self.fullFileName, 0)
        self.image_with_edges = cv2.Canny(img_edg , 50, 150)
        #cv2.imshow('edged Img', self.image_with_edges)
        
        # mbTk = tk.Tk()
        mbTk = tk.Toplevel()
        mbTk.title("Set every item on board")
        ## we used refCm instead of self.cm. we need to rescale when importin from refCm to self.cm
        mbCn = tk.Canvas(mbTk, width= boardWidth + 2*refCm, height = boardHeight + 2*refCm, background = 'white')
        # mbCn = tk.Canvas(mbTk, width= boardWidth, height = boardHeight, background = 'white')
        mbCn.grid()
        
        mbPic = ImageTk.PhotoImage(file = 'PCBs/Cropped/' + self.fullFileName)  # PIL solution
        mbTk.mbPic = mbPic
        self.imgSX = mbPic.width()
        self.imgSY = mbPic.height()
        
        print("img Tk size: ", self.imgSX, ", ",  self.imgSY)
        mbCn.update()
        # mbPic = PhotoImage(file='PCBs/Cropped/' + self.fullFileName)
        mbCn.create_image(0, 0, image=mbPic, anchor='nw')
        
        self.mbCn = mbCn
        
        self.selB = 3 # to understand that this click is coming from this method and this canvas
        
        self.mbCn.bind('<Button-1>', self.mbClk)
        self.mbCn.bind('<Motion>', self.mbM)
        self.mbCn.bind('<Button-3>', self.mbRclk)
        self.mbCn.bind('<ButtonRelease-1>', self.btnRls)
        self.mbCn.bind('<MouseWheel>', self.mWhl)
        
        # plt.show()

    def imp_img(self):
        tk.Tk().withdraw()
        mbF = tk.Frame(self.mbTk)
        mbF.grid(row = 1, column = 3, rowspan = 13)
        self.mbF = mbF
        imgPath = tk.filedialog.askopenfilename()
        fName = imgPath.split('/')[-1]
        self.fullFileName = fName
        self.fName = fName[:-(len(fName.split('.')[-1])+1)]
        self.xS = int(self.fName.split('_')[0])/10
        self.yS = int(self.fName.split('_')[1])/10
        if self.fName[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            self.code = self.fName.split('-')[-2].split('_')[-1]
            self.version = self.fName.split('-')[-1]
        else:
            self.version = '0'
            self.code = self.fName.split('-')[-1].split('_')[-1]
        print("code: ", self.code, " version: ", self.version)
        print("xS, yS: ", self.xS, ", ", self.yS)
        print(self.fName)
        print(imgPath)
        image = cv2.imread(imgPath.split('/')[-2]+'/'+imgPath.split('/')[-1], 0)
        # plt.imshow(image, cmap='gray')
        # plt.imshow(image, cmap='gray')
        # plt.show()
        self.detect_edge(image)

    def save(self):
        if self.selB == 1 or self.selB == 2:
            self.getSizes()
        obj = mbDb()
        obj.addMb(self)
        obj.showSome()
        del obj


    def test(self):
        psuS = int(float(self.Checkbutton1.get()))
        print(psuS)
        ldS = int(float(self.Checkbutton2.get()))
        uS = int(float(self.Checkbutton3.get()))
        tcS = int(float(self.Checkbutton4.get()))
        self.includes = [psuS,ldS,uS,tcS]
        print(self.includes)
        
    def getSizes(self):
        self.xS = int(float(self.xSizeEnt.get()))
        self.yS = int(float(self.ySizeEnt.get()))
        self.code = self.codeEnt.get()
        self.version = self.versionEnt.get()
        print("x,y sizes:", self.xS , self.yS)


    def locateScrews(self):
        self.getSizes()
        self.selB = 1
        mbSc = tk.Tk()
        mbSc.title("Select Screw locations on the board")
        mbScFrCv = tk.Canvas(mbSc, width= self.cm*self.xS+2*self.cm, height = self.cm*self.yS+2*self.cm, background = 'white')
        mbScFrCv.grid()
        self.mbScFrCv = mbScFrCv
        mbScFrCv.create_rectangle(self.cm, self.cm, (self.xS+1)*self.cm, (self.yS+1)*self.cm, width=3)
        mbScFrCv.create_text(self.cm*(self.xS/2+1),self.cm*(self.yS/2+1), text = 'MainBoard', angle=0)
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
        mbCnFrCv.create_text(self.cm*(self.xS/2+1),self.cm*(self.yS/2+1), text = 'MainBoard', angle=0)
        for ev in self.screwCo:
            self.mbCnFrCv.create_rectangle(ev[0]-3,ev[1]-3,ev[0]+3,ev[1]+3, width=2, fill="green")
        self.conInt = 0
        self.conC = 0
##        self.sc = 0 
        self.mbCnFrCv.bind('<Button-1>', self.mbClk)
        self.mbCnFrCv.bind('<Motion>', self.mbM)
        self.mbCnFrCv.bind('<Button-3>', self.mbRclk)
        mbCn.bind('<space>', self.mbSpc)
        
    
    def btnRls(self, event):
        if not self.btnRlsBugReliever:
            ev = [event.x,event.y]
            self.frstClkStt = False
            self.rlsTime = unix_time_millis(datetime.datetime.now())
            self.mbCn.delete("tempRec")
            if self.rlsTime - self.clkTime > 500:
                if (abs(ev[0]-self.recFrsEv[0]) > 5 or abs(ev[1]-self.recFrsEv[1]) > 5):
                    self.recLstEv = ev
                    self.create_line_of_rec(self.recFrsEv, self.recLstEv, 'finalRec', 2)
                    self.find_con(self.recFrsEv, self.recLstEv, 'conRec')
                    print("last clc on canvas: ", self.recLstEv)
                else:
                    self.recLstEv = ev
                    self.find_screw(ev, 'tempCircle')
                    self.is_in_screw_finding = True
                    self.is_in_con_sel = False
        else:
            self.btnRlsBugReliever = False
        

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
        if self.selB == 3 and not self.is_in_con_sel and not self.is_in_screw_finding:
            self.clkTime = unix_time_millis(datetime.datetime.now())
            self.frstClkStt = True
            self.recFrsEv = ev
        elif self.selB == 3 and self.is_in_con_sel and not self.is_in_screw_finding:
            self.mbCn.delete("conRec")
            self.mbCn.delete("tempConText")
            self.mbCn.delete("tempRec")
            self.mbCn.delete("tempCircle")
            self.mbCn.create_text(self.tmp_con_cor[0], self.tmp_con_cor[1], text = st.conList[self.conInt], fill='green', angle=0, font=self.bold_font, tags= 'finalConText' )
            self.mbCn.create_rectangle(self.conCor1[0], self.conCor1[1], self.conCor2[0], self.conCor2[1], width=4, tags="rinalRec")
            self.from_img_conns.append([[self.conCor1[0], self.conCor1[1], self.conCor2[0], self.conCor2[1]], st.conList[self.conInt]]) #coordinates of the connectors and their types like [[x1,y1,x2,y2],'usb']
            self.mb_con_rects.append([self.conCor1[0], self.conCor1[1], self.conCor2[0], self.conCor2[1]])
            tX = int((self.conCor1[0] + self.conCor2[0])/2)
            tY = int((self.conCor1[1] + self.conCor2[1])/2)
            self.conCo.append([[tX,tY], st.conList[self.conInt]])
            
            self.is_in_con_sel = False
            self.btnRlsBugReliever = True
            
        elif self.selB == 3 and self.is_in_screw_finding and not self.is_in_con_sel:
            x = self.from_img_screws[-1][0][0]
            y = self.from_img_screws[-1][0][1]
            rad = self.from_img_screws[-1][1]
            self.mbCn.create_oval(x-rad, y-rad, x+rad, y+rad, width=2, tags='FinalScrew')
            
            self.screwCo.append([x,y])
            
            self.is_in_screw_finding = False
            self.btnRlsBugReliever = True
            
        
  
    @_dont_run_at_con_select
    def create_line_of_rec(self, ev1, ev2, tag, wdt):
        self.mbCn.create_line(ev1[0], ev1[1], ev1[0], ev2[1], width=wdt, dash=(4, 2), tags=tag)
        self.mbCn.create_line(ev1[0], ev1[1], ev2[0], ev1[1], width=wdt, dash=(4, 2), tags=tag)
        self.mbCn.create_line(ev1[0], ev2[1], ev2[0], ev2[1], width=wdt, dash=(4, 2), tags=tag)
        self.mbCn.create_line(ev2[0], ev1[1], ev2[0], ev2[1], width=wdt, dash=(4, 2), tags=tag)

    @_dont_run_at_con_select
    def create_circle(self, x, y, rad, tag, wdt):
        self.mbCn.create_oval(x-rad, y-rad, x+rad, y+rad, width=wdt, dash=(4, 2), tags=tag)
    
    
    @_dont_run_at_con_select
    def find_con(self, ev1, ev2, tag):
        im_edge = self.image_with_edges
        im_edge = cv2.resize(im_edge, (self.imgSX, self.imgSY), interpolation= cv2.INTER_LINEAR)
        print("im_edge size: ", len(im_edge), ", ", len(im_edge[0]))
        
        x_min = min(ev1[0], ev2[0])
        y_min = min(ev1[1], ev2[1])
        x_max = max(ev1[0], ev2[0])
        y_max = max(ev1[1], ev2[1])
        
        xLen = x_max - x_min 
        yLen = y_max - y_min
        
        maxCol1 = 0
        maxCol2 = 0
        colInd1 = -1
        colInd2 = -1
        for x in range(int(xLen/3)):
            colKpr = 0
            for y in range(yLen - 6):
                colKpr += im_edge[y_min + 3 + y][x_min + 3 + x] / 255
            if colKpr > maxCol1:
                maxCol1 = colKpr
                colInd1 = x_min + 3 + x
                
            colKpr = 0
            for y in range(yLen - 6):
                colKpr += im_edge[y_min + 3 + y][x_max - 3 - x] / 255
            if colKpr > maxCol2:
                maxCol2 = colKpr
                colInd2 = x_max - 3 - x

        maxRow1 = 0
        maxRow2 = 0
        rowInd1 = -1
        rowInd2 = -1
        for y in range(int(yLen/3)):
            rowKpr = 0
            for x in range(xLen - 6):
                rowKpr += im_edge[y_min + 3 + y][x_min + 3 + x] / 255
            if rowKpr > maxRow1:
                maxRow1 = rowKpr
                rowInd1 = y_min + 3 + y
                
            rowKpr = 0
            for x in range(xLen - 6):
                rowKpr += im_edge[y_max - 3 - y][x_min + 3 + x] / 255
            if rowKpr > maxRow2:
                maxRow2 = rowKpr
                rowInd2 = y_max - 3 - y
        self.mbCn.delete("tempRec")
        self.mbCn.delete("finalRec")
        conCorner1 = [colInd1, rowInd1]
        conCorner2 = [colInd2, rowInd2]
        print(conCorner1, " , ", conCorner2)
        self.create_line_of_rec(conCorner1, conCorner2, tag, 4)
        #self.from_img_conns.append([],)
        self.conCor1 = conCorner1
        self.conCor2 = conCorner2
        self.tmp_con_cor = [int((colInd1+colInd2)/2),int((rowInd1+rowInd2)/2)]
        self.conInt = 0
        self.mbCn.create_text(self.tmp_con_cor[0], self.tmp_con_cor[1], text = st.conList[self.conInt], fill='green', angle=0, font=self.bold_font, tags= 'tempConText' )
        self.is_in_con_sel = True
        self.is_in_screw_finding = False
        
        
    @_dont_run_at_con_select
    def find_screw(self, ev, tag):
        im_edge = self.image_with_edges
        im_edge = cv2.resize(im_edge, (self.imgSX, self.imgSY), interpolation= cv2.INTER_LINEAR)
        
        y_max = ev[1] + self.cm/2
        y_min = ev[1] - self.cm/2
        x_max = ev[0] + self.cm/2
        x_min = ev[0] - self.cm/2
        
        x_c = ev[0]
        y_c = ev[1]
        
        rad = int(self.cm / 10)+1
        
        # rad = int(self.cm / 10)+1
        # deg = 0
        
        # touches = [None for in range(360)]
        # for i in range(360):
            # radyan = math.pi*2*i/360
            # for j in range(self.cm/2):
                # rel_x = x_c + j*math.cos(radyan)
                # rel_y = y_c + j*math.sin(radyan)
                # if im_edge[rel_x][rel_y] == 255:
                    # touches[i].append([rel_x,rel_y])
        
        # arcs_from_left = []
        # arcs_from_right = []
        # for i in range(36):
            # for j in range(10):
                # stt = i*10
                # for k in range(10):
                    # if len(touches[stt]) > 0:
                        # break
                    # else:
                        # stt += 1
                # if stt > i*10+7:
                    # break
                # for k in range(len(touches[stt])):
                    # tmp_ctr = 0
                    # temp_arc_from_left = [touches[stt][k]]
                    # temp_arc_from_right = [touches[stt][k]]
                    # while(tmp_ctr < i*10 + 9 - stt):
                        
                        # for l in touches[stt+tmp_ctr+1]:
                            # if dist_call(temp_arc_from_left[-1], l, self.cm/10+1):
                                # temp_arc_from_left.append(l)
                                # break
                        
                        # lt = len(touches[stt+tmp_ctr+1])
                        # for l in range(lt):
                            # if dist_call(temp_arc_from_right[-1], touches[stt+tmp_ctr+1][lt-1-l], self.cm/10+1):
                                # temp_arc_from_right.append(l)
                                # break
                                
                        # tmp_ctr += 1
                    # if len(temp_arc_from_left) > 3:
                        # arcs_from_left.append(temp_arc_from_left)
                    # if len(temp_arc_from_right) > 3:
                        # arcs_from_right.append(temp_arc_from_right)
        
        rad_ch = False
        cen_ch = False
        tempCX = 0
        tempCY = 0
        tempRad = 0
        for i in range(int(self.cm/3)):
            for j in range(int(self.cm/3)):
                for k in range(int(self.cm/3)):
                    temp_count_p = 0
                    temp_count_n = 0
                    for h in range(360):
                        rel_x_p = x_c + i + (rad + k)*math.cos(h*math.pi*2/360)
                        rel_y_p = y_c + j + (rad + k)*math.sin(h*math.pi*2/360)
                        rel_x_n = x_c - i + (rad + k)*math.cos(h*math.pi*2/360)
                        rel_y_n = y_c - j + (rad + k)*math.sin(h*math.pi*2/360)
                        rel_x_p = int(rel_x_p)
                        rel_y_p = int(rel_y_p)
                        rel_x_n = int(rel_x_n)
                        rel_y_n = int(rel_y_n)
                        if im_edge[rel_y_p][rel_x_p] == 255:
                            temp_count_p += 1
                        if im_edge[rel_y_n][rel_x_n] == 255:
                            temp_count_n += 1
                            
                    print("temp_count_p,temp_count_n: ",temp_count_p,temp_count_n)
                    if temp_count_p >= temp_count_n:
                        if temp_count_p > 150 and tempRad < rad + k:
                            tempCX = x_c + i
                            tempCY = y_c + j
                            tempRad = rad + k
                            print("tempCX,tempCY,tempRad: ",tempCX,tempCY,tempRad)
                    else:
                        if temp_count_n > 150 and tempRad < rad + k:
                            tempCX = x_c - i
                            tempCY = y_c - j
                            tempRad = rad + k
                            print("tempCX,tempCY,tempRad: ",tempCX,tempCY,tempRad)
        
        self.create_circle(tempCX, tempCY, tempRad, 'tempCircle', 4)
        self.from_img_screws.append([[tempCX,tempCY],tempRad])
                    
    def mWhl(self, event):
        ev = [event.x,event.y]
        self.mbCn.delete("tempConText")
        if self.selB == 3 and self.is_in_con_sel:
            if event.delta > 0:
                self.conInt += 1
            elif event.delta < 0:
                self.conInt -= 1
            self.conInt = self.conInt % len(st.conList)
            self.mbCn.create_text(self.tmp_con_cor[0], self.tmp_con_cor[1], text = st.conList[self.conInt], fill='green', angle=0, font=self.bold_font, tags= 'tempConText' )

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
        if self.selB == 3:
            # if self.clickedOnce == True and self.clikedTwice == False:
            if self.frstClkStt:
                self.mbCn.delete("tempRec")
                # self.mbCn.create_rectangle(self.recFrsEv[0],self.recFrsEv[1],ev[0], ev[1], width=1, fill="green", tags='tempRec')
                self.create_line_of_rec(self.recFrsEv, ev, 'tempRec', 2)
                
    def mbRclk(self, event):
        ev = [event.x,event.y]
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
        if self.selB == 3:
            self.mbCn.delete("conRec")
            self.mbCn.delete("tempConText")
            self.mbCn.delete("tempCircle")
            self.is_in_con_sel = False
            self.is_in_screw_finding = False
            if len(self.from_img_screws):
                self.from_img_screws.pop()
                
    def mbSpc(self, event):
        ev = [event.x,event.y]
        print("space e girdi!")
        if self.selB == 2:
            self.conInt = (self.conInt + 1)%len(st.conList)
            print("conn no is: ", self.conInt)
            self.mbCnFrCv.delete("temp")
            self.mbCnFrCv.create_oval(ev[0]-10,ev[1]-10,ev[0]+10,ev[1]+10, width=2, fill="red", tags= "temp")
            self.mbCnFrCv.create_text(ev[0],ev[1], text = st.conList[self.conInt], angle=0, tags= "temp")
        if self.selB == 3 and self.is_in_con_sel:
            pass
            
            
        

if __name__ == "__main__":
    app = SampleApp()
    
    app.mainloop()
