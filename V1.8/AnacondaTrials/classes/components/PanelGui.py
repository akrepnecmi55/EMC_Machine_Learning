# Multi-frame tkinter application v2.3
import os
import sys
sys.path.insert(0, "..")
import tkinter as tk
from tkinter import *
from classes.settings import Settings as st
from classes.db.PanelDatabase import PanelDatabase as panelDb
import numpy as np
import cv2
import math
from PIL import ImageTk, Image
import matplotlib.pyplot as plt


class PanelGui():
    def __init__(self):
        self.dB=panelDb()
        self.mbTk = tk.Tk()
        self.kabin_code="BOŞ"
        self.inch=1
        self.panel_code="BOŞ"
        self.mbTk.title("Cell configuration")
        self.mbTk.geometry('600x250')
        self.mbF = tk.Frame(self.mbTk)
        self.wizardflags = 0
        self.SB_processed = 0
        self.TCON_include = False
        self.TCON_DC_include = False
        self.psuFlag = False
        self.ursaFlag = False

        self.Wizard_Button=tk.Button(self.mbTk, text="Label Peripherals on Panel Wizard",width=50, height=10,bg="red", command = lambda: self.imp_img())
        self.Wizard_Button.pack()

    def detect_panel(self,Path):#PANEL ÇERÇEVE OTOMATİK ALGILAMA FONKSİYONU, 4 KÖŞEDE SINIRLAR İÇERİSİNDE İSE TAHMİNİ BİR ÇERÇEVEYİ ÇIKTI OLARAK VERİYOR
        img = cv2.imread(Path)
        img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (15,15), 0)
        vert_threshold = 12/100
        horiz_threshold = 10/100
        top_line_order = 0
        bot_line_order = 0
        left_line_order = 0
        right_line_order = 0

        imgCanny=cv2.Canny(imgBlur, 174, 38)
        kernel = np.ones((5,5))
        imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
        imgErod = cv2.erode(imgDil,kernel,iterations=1)

        height, width = imgErod.shape[:2] # image shape (509,1008) (y,x)
        dst = np.zeros(shape=[height, width, 3], dtype=np.uint8)   #Boş frame
        dst_2 = img.copy()
        dst_3 = np.zeros(shape=[height, width, 3], dtype=np.uint8)   #Boş frame


        horiz_lines = cv2.HoughLines(imgErod,1,np.pi/180,int(width*horiz_threshold))
        if horiz_lines is not None:
            horiz_lines_with_coordinates=[]
            for line in horiz_lines:
                for rho,theta in line:
                    if (1.45<theta and theta<1.67) and rho!=0:
                        #print(rho,theta)
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a*rho
                        y0 = b*rho
                        if int(x0)!=0:
                            y1_new = int(rho / b)
                            y2_new = int(((width-x0)*(y0-y1_new)/x0)+y0)
                            if y1_new+y2_new>0:
                                horiz_lines_with_coordinates.append(((y1_new+y2_new)/2,y1_new,y2_new))
                        else:
                            y1_new = int(rho / b)
                            y2_new = y1_new
                            if y1_new+y2_new>0:
                                horiz_lines_with_coordinates.append(((y1_new+y2_new)/2,y1_new,y2_new))
        else:
            print("No Line founded")

        vert_lines = cv2.HoughLines(imgErod,1,np.pi/180,int(height*vert_threshold))

        if vert_lines is not None:
            vert_lines_with_coordinates=[]
            for line in vert_lines:
                for rho,theta in line:
                    if ((theta<0.5) or (theta>2.6)) and rho!=0:
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a*rho
                        y0 = b*rho
                        if int(y0)!=0:
                            x1_new = int(rho / a)
                            x2_new = int(((height-y0)*(x0-x1_new)/y0)+x0)
                            if(x1_new+x2_new>0):
                                vert_lines_with_coordinates.append(((x1_new+x2_new)/2,x1_new,x2_new))
                        else:
                            x1_new = int(rho / a)
                            x2_new = x1_new
                            if(x1_new+x2_new>0):
                                vert_lines_with_coordinates.append(((x1_new+x2_new)/2,x1_new,x2_new))
        else:
            print("No Line found")
        horiz_lines_with_coordinates.sort()
        vert_lines_with_coordinates.sort()
        if (horiz_lines_with_coordinates is not None) and (vert_lines_with_coordinates is not None):
            cv2.line(dst_2,(0,horiz_lines_with_coordinates[top_line_order][1]),(width,horiz_lines_with_coordinates[top_line_order][2]),(0,255,0),2)
            cv2.line(dst_2,(0,horiz_lines_with_coordinates[-1*(bot_line_order+1)][1]),(width,horiz_lines_with_coordinates[-1*(bot_line_order+1)][2]),(0,255,0),2)
            cv2.line(dst_2,(vert_lines_with_coordinates[left_line_order][1],0),(vert_lines_with_coordinates[left_line_order][2],height),(0,255,0),2)
            cv2.line(dst_2,(vert_lines_with_coordinates[-1*(right_line_order+1)][1],0),(vert_lines_with_coordinates[-1*(right_line_order+1)][2],height),(0,255,0),2)
            cv2.line(dst_3,(0,horiz_lines_with_coordinates[top_line_order][1]),(width,horiz_lines_with_coordinates[top_line_order][2]),(0,255,0),5)
            cv2.line(dst_3,(0,horiz_lines_with_coordinates[-1*(bot_line_order+1)][1]),(width,horiz_lines_with_coordinates[-1*(bot_line_order+1)][2]),(0,255,0),5)
            cv2.line(dst_3,(vert_lines_with_coordinates[left_line_order][1],0),(vert_lines_with_coordinates[left_line_order][2],height),(0,255,0),5)
            cv2.line(dst_3,(vert_lines_with_coordinates[-1*(right_line_order+1)][1],0),(vert_lines_with_coordinates[-1*(right_line_order+1)][2],height),(0,255,0),5)
        else:
            print("No Line Found")

        dst_3 = cv2.cvtColor(dst_3,cv2.COLOR_BGR2GRAY)
        self.corners = corners = cv2.goodFeaturesToTrack(dst_3, 4, 0.5, width/10) #func(img, numberofcorners, quality of corner[0-1], minimum euclidean distance between two corners)
        self.width=width
        self.height=height
        try:
            corners = np.int0(corners)
        except:
            pass
        if corners is not None:
            for corner in corners:
                x, y =corner.ravel() # [[x,y]] -> [x,y]
                cv2.circle(dst_2, (x,y), 5, (255,0,0), -1)
                if x<width/2:
                    if y<height/2:
                        self.corner_topleft=[x,y]
                    else:
                        self.corner_botleft=[x,y]
                else:
                    if y<height/2:
                        self.corner_topright=[x,y]
                    else:
                        self.corner_botright=[x,y]
        #if len(corners)==4:
            #print(corner_topleft,corner_topright,corner_botleft,corner_botright)
            #pts1= np.float32([corner_topleft,corner_topright,corner_botleft,corner_botright])
            #pts2 = np.float32([[0,0],[800,0],[0,450],[800,450]])
            #M = cv2.getPerspectiveTransform(pts1,pts2)
            #img_transformed = cv2.warpPerspective(img,M,(800,450))
        #else:
        #    img_transformed=img.copy()


        #cv2.imshow('Choosen Lines on Image', dst_2)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


    def imp_img(self):#IMPORT FROM IMG Tıklayınca çağırılan fonksiyon
        self.Wizard_Button.destroy()
        imgPath = tk.filedialog.askopenfilename()
        print(imgPath)
        print(imgPath.split(".KONF")[0].split("/")[-1])
        self.fName=imgPath.split(".KONF")[0].split("/")[-1]
        self.inch=int(imgPath.split(".KONF")[0].split("/")[-1].split("''")[0])#43''FY2KABIN056T43-E19PANELNESASIKAB.KONF
        self.kabin_code=imgPath.split(".KONF")[0].split("/")[-1].split("''")[1].split("KABIN")[0]
        self.panel_code=imgPath.split(".KONF")[0].split("/")[-1].split("''")[1].split("KABIN")[1].split("PANEL")[0]#Bunu sorrrrrrrrr!!!!!!!!!!!!!!!!!!!!!!
        self.imgPath=imgPath.split('/')[-3]+'/'+imgPath.split('/')[-2]+'/'+imgPath.split('/')[-1]
        self.detect_panel(self.imgPath)
        self.WizardTk = tk.Toplevel()
        self.WizardTk.geometry(str(self.width+50)+'x'+str(self.height+50))
        self.mbTk.destroy()
        self.WizardTk.title("Set Corners")
        mbCn = tk.Canvas(self.WizardTk, width= self.width, height = self.height, background = 'white')
        mbCn.grid(row=1,column=1)
        self.nextbutton=tk.Button(self.WizardTk, text="Next", command = lambda: self.nextframe())
        self.nextbutton.grid(row=2,column=1)
        my_img = Image.open(imgPath)
        my_img = my_img.resize((self.width,self.height), Image.ANTIALIAS)
        self.my_img = ImageTk.PhotoImage(my_img)
        mbCn.update()
        self.image_on_canvas=mbCn.create_image(0, 0, image=self.my_img, anchor='nw')
        self.mbCn = mbCn
        if len(self.corners)!=4:
            self.corner_topleft=[0,0]
            self.corner_topright=[self.width,0]
            self.corner_botleft=[0,self.height]
            self.corner_botright=[self.width,self.height]

        corner_topleft=self.corner_topleft
        corner_topright=self.corner_topright
        corner_botleft=self.corner_botleft
        corner_botright=self.corner_botright
        self.frame=mbCn.create_line(corner_topleft[0],corner_topleft[1],
                                    corner_topright[0],corner_topright[1],
                                    corner_botright[0],corner_botright[1],
                                    corner_botleft[0],corner_botleft[1],
                                    corner_topleft[0],corner_topleft[1],
                                    fill="red",width=2)
        self.corner1=mbCn.create_oval(corner_topleft[0]-10,corner_topleft[1]-10,
                            corner_topleft[0]+10,corner_topleft[1]+10,
                            width=2,outline="red")
        self.corner2=mbCn.create_oval(corner_topright[0]-10,corner_topright[1]-10,
                            corner_topright[0]+10,corner_topright[1]+10,
                            width=2,outline="red")
        self.corner3=mbCn.create_oval(corner_botright[0]-10,corner_botright[1]-10,
                            corner_botright[0]+10,corner_botright[1]+10,
                            width=2,outline="red")
        self.corner4=mbCn.create_oval(corner_botleft[0]-10,corner_botleft[1]-10,
                            corner_botleft[0]+10,corner_botleft[1]+10,
                            width=2,outline="red")
        self.mbCn = mbCn
        self.mbCn.bind('<Button-1>', self.mbClk)


    def mbClk(self, event):#Mouse sol tıklama ile 4 köşenin yerlerinin seçilebildiği fonksiyon
        ev = [event.x,event.y]
        mbCn=self.mbCn
        if ev[0]<self.width/2:#left
            if ev[1]<self.height/2:#top
                corner_topleft=self.corner_topleft=ev
                mbCn.delete(self.frame)
                mbCn.delete(self.corner1)
                self.corner1=mbCn.create_oval(corner_topleft[0]-10,corner_topleft[1]-10,
                                corner_topleft[0]+10,corner_topleft[1]+10,
                                width=2,outline="red")
            else:#bot
                corner_botleft=self.corner_botleft=ev
                mbCn.delete(self.frame)
                mbCn.delete(self.corner4)
                self.corner4=mbCn.create_oval(corner_botleft[0]-10,corner_botleft[1]-10,
                                corner_botleft[0]+10,corner_botleft[1]+10,
                                width=2,outline="red")
        else:#right
            if ev[1]<self.height/2:#top
                corner_topright=self.corner_topright=ev
                mbCn.delete(self.frame)
                mbCn.delete(self.corner2)
                self.corner2=mbCn.create_oval(corner_topright[0]-10,corner_topright[1]-10,
                                corner_topright[0]+10,corner_topright[1]+10,
                                width=2,outline="red")
            else:#bot
                corner_botright=self.corner_botright=ev
                mbCn.delete(self.frame)
                mbCn.delete(self.corner3)
                self.corner3=mbCn.create_oval(corner_botright[0]-10,corner_botright[1]-10,
                                corner_botright[0]+10,corner_botright[1]+10,
                                width=2,outline="red")
        self.frame=mbCn.create_line(self.corner_topleft[0],self.corner_topleft[1],
                        self.corner_topright[0],self.corner_topright[1],
                        self.corner_botright[0],self.corner_botright[1],
                        self.corner_botleft[0],self.corner_botleft[1],
                        self.corner_topleft[0],self.corner_topleft[1],
                        fill="red",width=2)
        self.mbCn = mbCn

    def get_SB_option(self):
        #self.SB_count=int(self.value_inside.get())
        print("Sourceboard count=",self.value_inside.get())
        self.SB_count = self.value_inside.get()
        self.submit_button.destroy()
        self.question_menu.configure(state='disabled')
        self.wizardflags = 1
        self.nextframe()#Sourceboard sayısının onaylanması ile çalışan fonksiyon

    def SB_label_leftclick(self,event): #Sourceboard'ın sol üst köşe koordinatı belirlenir, mouse tıklaması anında çağrılır
        if self.SB_processed < self.SB_count:
            self.topleft_c = [event.x,event.y]
            self.sb_topleftcorners.append(self.topleft_c)

    def SB_label_leftclick_motion(self,event):#Sourceboard'ın dikdörtgen olarak boyutunu görmek için var, sadece görsellik için
        if self.SB_processed < self.SB_count:
            try:
                self.mbCn.delete(self.temp_rect)
            except:
                pass
            self.temp_rect=self.mbCn.create_rectangle(self.topleft_c[0],self.topleft_c[1],event.x,event.y,width=2,outline="blue")

    def SB_label_leftclick_release(self,event):#Sourceboard'ın sağ alt köşe koordinatı belirlenir. Mouse tıklaması serbest bırakılması ile çağırılır
        if self.SB_processed < self.SB_count:
            self.mbCn.delete(self.temp_rect)
            self.SB_rectangle=self.mbCn.create_rectangle(self.topleft_c[0],self.topleft_c[1],event.x,event.y,width=2,outline="blue")
            self.SB_rectangles.append(self.SB_rectangle)
            self.SB_coordinates.append([self.topleft_c[0]*self.reallenght_cm_ratio,self.topleft_c[1]*self.reallenght_cm_ratio,event.x*self.reallenght_cm_ratio,event.y*self.reallenght_cm_ratio])
            self.botright_c = [event.x,event.y]
            self.sb_botrightcorners.append(self.botright_c)
            self.SB_processed +=1
            print(self.sb_topleftcorners)
            print(self.sb_botrightcorners)
            print(self.SB_rectangles)
            print(self.SB_coordinates)
        if self.SB_processed == self.SB_count:
            self.mbCn.unbind('<Button-1>')
            self.mbCn.unbind('<B1-Motion>')
            self.mbCn.unbind('<ButtonRelease-1>')
            self.wizardflags = 2
            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.nextframe())
            self.submit_button.grid(row=2,column=2)

    def TCON_place(self): #TCON Label
        self.TCON_yes_button.grid_remove()
        self.TCON_no_button.grid_remove()
        self.TCON_Q_Label.grid_remove()
        self.TCON_Q_Label2.grid(row=1,column=2)
        self.TCON_include = True
        self.mbCn.bind('<Button-1>', self.TCON_label_leftclick)
        self.mbCn.bind('<B1-Motion>', self.TCON_label_leftclick_motion)
        self.mbCn.bind('<ButtonRelease-1>', self.TCON_label_leftclick_release)

    def TCON_label_leftclick(self,event):
        try:
            self.mbCn.delete(self.TCON_rectangle)
        except:
            pass
        self.tcon_topleftcorners=[event.x,event.y]#TCON'ın sol üst köşe koordinatı belirlenir, mouse tıklaması anında çağrılır

    def TCON_label_leftclick_motion(self,event):#TCON'ın dikdörtgen olarak boyutunu görmek için var, sadece görsellik için
        try:
            self.mbCn.delete(self.temp_rect)
        except:
            pass
        self.temp_rect=self.mbCn.create_rectangle(self.tcon_topleftcorners[0],self.tcon_topleftcorners[1],event.x,event.y,width=2,outline="blue")

    def TCON_label_leftclick_release(self,event):#Tcon'ın sağ alt köşe koordinatı belirlenir. Mouse tıklaması serbest bırakılması ile çağırılır
        self.mbCn.delete(self.temp_rect)
        self.TCON_rectangle=self.mbCn.create_rectangle(self.tcon_topleftcorners[0],self.tcon_topleftcorners[1],event.x,event.y,width=2,outline="blue")
        self.tcon_botrightcorners=[event.x*self.reallenght_cm_ratio,event.y*self.reallenght_cm_ratio]
        self.tcon_topleftcorners=[self.tcon_topleftcorners[0]*self.reallenght_cm_ratio,self.tcon_topleftcorners[1]*self.reallenght_cm_ratio]
        self.tcon_coordinates=[self.tcon_topleftcorners,self.tcon_botrightcorners]
        print(self.tcon_topleftcorners)
        print(self.tcon_botrightcorners)
        print(self.TCON_rectangle)
        self.TCON_end()

    def TCON_end(self):#TCON koordinatları kaydedilir
        self.TCON_yes_button.grid_remove()
        self.TCON_no_button.grid_remove()
        self.TCON_Q_Label.grid_remove()
        self.TCON_Q_Label2.grid_remove()
        if self.TCON_include :
            self.wizardflags = 3
        else:
            self.wizardflags = 8
        self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.nextframe())
        self.submit_button.grid(row=2,column=2)

    def get_connector_option(self):#LVDS konektör sayısı belirlenir
        self.connector_count = self.value_inside.get()
        self.submit_button.destroy()
        self.question_menu.configure(state='disabled')
        self.con_processed=0
        self.wizardflags = 4
        self.nextframe()

    def con_leftclick(self,event):#Konektörü yerleştir
        if self.con_processed < self.connector_count:
            self.connector_coordinates.append([event.x*self.reallenght_cm_ratio,event.y*self.reallenght_cm_ratio])
            self.con_processed+=1
            self.connector_done_label.destroy()
            self.connector_done_label=tk.Label(self.WizardTk, text=str(self.con_processed)+" adet TCON LVDS konektörü yerleştirildi")
            self.connector_done_label.grid(row=2,column=2)
            self.con_circle=self.mbCn.create_oval(event.x-3,event.y-3,event.x+3,event.y+3,outline="red")
            self.con_circles.append(self.con_circle)
            print(self.connector_coordinates)
        if self.con_processed == self.connector_count:
            self.submit_button.configure(state=tk.NORMAL)


    def con_rightclick(self,event):#Yanlış yerleştirilen konektörü sil
        if self.con_processed == 0:
            pass
        elif self.con_processed == self.connector_count:
            self.submit_button.configure(state=tk.DISABLED)
            self.con_circle=self.con_circles[-1]
            self.mbCn.delete(self.con_circle)
            self.con_circles.pop()
            self.connector_coordinates.pop()
            self.con_processed-=1
            self.connector_done_label.destroy()
            self.connector_done_label=tk.Label(self.WizardTk, text=str(self.con_processed)+" adet TCON LVDS konektörü yerleştirildi")
            self.connector_done_label.grid(row=2,column=2)
            print(self.connector_coordinates)
        else:
            self.con_circle=self.con_circles[-1]
            self.mbCn.delete(self.con_circle)
            self.con_circles.pop()
            self.connector_coordinates.pop()
            self.con_processed-=1
            self.connector_done_label.destroy()
            self.connector_done_label=tk.Label(self.WizardTk, text=str(self.con_processed)+" adet TCON LVDS konektörü yerleştirildi")
            self.connector_done_label.grid(row=2,column=2)
            print(self.connector_coordinates)

    def TCON_screw(self):
        self.mbCn.unbind('<Button-1>')
        self.mbCn.unbind('<Button-3>')
        self.connector_label_guide.destroy()
        self.connector_label_guide2.destroy()
        self.connector_done_label.destroy()
        self.submit_button.destroy()
        self.question_menu.destroy()
        self.LVDS_label.destroy()
        self.wizardflags+=1
        self.nextframe()

    def get_TCON_screw_option(self):
        self.screw_count = self.value_inside.get()
        self.submit_button.destroy()
        self.question_menu.configure(state='disabled')
        self.screw_processed=0
        self.wizardflags = 6
        self.nextframe()

    def screw_leftclick(self,event):
        if self.screw_processed < self.screw_count:
            self.screw_coordinates.append([event.x*self.reallenght_cm_ratio,event.y*self.reallenght_cm_ratio])
            self.screw_processed+=1
            self.screw_done_label.destroy()
            self.screw_done_label=tk.Label(self.WizardTk, text=str(self.screw_processed)+" adet vida yerleştirildi")
            self.screw_done_label.grid(row=3,column=2)
            self.screw_circle=self.mbCn.create_oval(event.x-3,event.y-3,event.x+3,event.y+3,outline="red")
            self.screw_circles.append(self.screw_circle)
            print(self.screw_coordinates)
        if self.screw_processed == self.screw_count:
            self.submit_button.configure(state=tk.NORMAL)

    def screw_rightclick(self,event):
        if self.screw_processed == 0:
            pass
        elif self.screw_processed == self.screw_count:
            self.submit_button.configure(state=tk.DISABLED)
            self.screw_circle=self.screw_circles[-1]
            self.mbCn.delete(self.screw_circle)
            self.screw_circles.pop()
            self.screw_coordinates.pop()
            self.screw_processed-=1
            self.screw_done_label.destroy()
            self.screw_done_label=tk.Label(self.WizardTk, text=str(self.screw_processed)+" adet vida yerleştirildi")
            self.screw_done_label.grid(row=3,column=2)
            print(self.screw_coordinates)
        else:
            self.screw_circle=self.screw_circles[-1]
            self.mbCn.delete(self.screw_circle)
            self.screw_circles.pop()
            self.screw_coordinates.pop()
            self.screw_processed-=1
            self.screw_done_label.destroy()
            self.screw_done_label=tk.Label(self.WizardTk, text=str(self.screw_processed)+" adet vida yerleştirildi")
            self.screw_done_label.grid(row=3,column=2)
            print(self.screw_coordinates)

    def TCON_screw_end(self):
        self.wizardflags = 7
        self.TCON_screw_label.destroy()
        self.screw_done_label.destroy()
        self.screw_label_guide.destroy()
        self.question_menu.destroy()
        self.submit_button.destroy()
        self.mbCn.unbind('<Button-1>')
        self.mbCn.unbind('<B1-Motion>')
        self.mbCn.unbind('<ButtonRelease-1>')
        self.nextframe()

    def TCON_DC_place(self):
        self.TCON_Q_Label.destroy()
        self.TCON_yes_button.destroy()
        self.TCON_no_button.destroy()
        self.TCON_Q_Label2.grid(row=1,column=2)
        self.TCON_DC_include = True
        self.mbCn.bind('<Button-1>', self.TCON_DC_label_leftclick)

    def TCON_DC_end(self):
        self.TCON_Q_Label.destroy()
        self.TCON_yes_button.destroy()
        self.TCON_no_button.destroy()
        self.wizardflags = 8
        self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.nextframe())
        self.submit_button.grid(row=2,column=2)

    def TCON_DC_label_leftclick(self,event):
        self.TCON_DC_coordinate=[event.x*self.reallenght_cm_ratio,event.y*self.reallenght_cm_ratio]
        self.TCON_DC_circle=self.mbCn.create_oval(event.x-3,event.y-3,event.x+3,event.y+3,outline="red")
        self.wizardflags = 8
        self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.nextframe())
        self.submit_button.grid(row=2,column=2)

    def get_SB_connector_option(self):
        self.connector_count = self.value_inside.get()
        self.submit_button.destroy()
        self.question_menu.configure(state='disabled')
        self.con_processed=0
        self.wizardflags = 9
        self.nextframe()

    def sb_con_leftclick(self,event):
        if self.con_processed < self.connector_count:
            self.sb_connector_coordinates.append([event.x*self.reallenght_cm_ratio,event.y*self.reallenght_cm_ratio])
            self.con_processed+=1
            self.connector_done_label.destroy()
            self.connector_done_label=tk.Label(self.WizardTk, text=str(self.con_processed)+" adet TCON LVDS konektörü yerleştirildi")
            self.connector_done_label.grid(row=2,column=2)
            self.sb_con_circle=self.mbCn.create_oval(event.x-3,event.y-3,event.x+3,event.y+3,outline="red")
            self.sb_con_circles.append(self.sb_con_circle)
            print(self.sb_connector_coordinates)
        if self.con_processed == self.connector_count:
            self.submit_button.configure(state=tk.NORMAL)

    def sb_con_rightclick(self,event):
        if self.con_processed == 0:
            pass
        elif self.con_processed == self.connector_count:
            self.submit_button.configure(state=tk.DISABLED)
            self.sb_con_circle=self.sb_con_circles[-1]
            self.mbCn.delete(self.sb_con_circle)
            self.sb_con_circles.pop()
            self.sb_connector_coordinates.pop()
            self.con_processed-=1
            self.connector_done_label.destroy()
            self.connector_done_label=tk.Label(self.WizardTk, text=str(self.con_processed)+" adet TCON LVDS konektörü yerleştirildi")
            self.connector_done_label.grid(row=2,column=2)
            print(self.sb_connector_coordinates)
        else:
            self.sb_con_circle=self.sb_con_circles[-1]
            self.mbCn.delete(self.sb_con_circle)
            self.sb_con_circles.pop()
            self.sb_connector_coordinates.pop()
            self.con_processed-=1
            self.connector_done_label.destroy()
            self.connector_done_label=tk.Label(self.WizardTk, text=str(self.con_processed)+" adet TCON LVDS konektörü yerleştirildi")
            self.connector_done_label.grid(row=2,column=2)
            print(self.sb_connector_coordinates)

    def SB_LVDS_end(self):
        self.mbCn.unbind('<Button-1>')
        self.mbCn.unbind('<Button-3>')
        self.SB_LVDS_label.destroy()
        self.question_menu.destroy()
        self.connector_label_guide.destroy()
        self.connector_label_guide2.destroy()
        self.connector_done_label.destroy()
        self.submit_button.destroy()
        self.wizardflags = 10
        self.nextframe()

    def get_board_check(self):
        if self.psuCheck.get() == 1:
            self.psuFlag = True
        if self.ursaCheck.get() == 1:
            self.ursaFlag = True
        self.psuCheckButton.destroy()
        self.ursaCheckButton.destroy()
        self.submit_button.destroy()
        self.boardLabel=tk.Label(self.WizardTk, text="Mainboard'un sol üst noktasını işaretleyiniz(sol tık işaretler, sağ tık siler)")
        self.boardLabel.grid(row=2,column=2)
        self.mbCn.bind('<Button-1>', self.get_mb_coor)
        self.wizardflags=11
        self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.psu_state(),state="disabled")
        self.submit_button.grid(row=3,column=2)

    def get_mb_coor(self,event):
        self.mb_corner_circle=self.mbCn.create_oval(event.x-3,event.y-3,event.x+3,event.y+3,outline="red")
        self.mb_coordinate=[event.x*self.reallenght_cm_ratio,event.y*self.reallenght_cm_ratio]
        self.submit_button.configure(state=tk.NORMAL)
        self.mbCn.unbind('<Button-1>')
        self.mbCn.bind('<Button-3>', self.delete_mb_coor)

    def delete_mb_coor(self):
        self.mbCn.delete(self.mb_corner_circle)
        self.submit_button.configure(state='disabled')
        self.mbCn.unbind('<Button-3>')
        self.mbCn.bind('<Button-1>', self.get_mb_coor)

    def psu_state(self):
        if not self.psuFlag :
            self.ursa_state()
        else:
            self.submit_button.destroy()
            self.boardLabel.destroy()
            self.boardLabel=tk.Label(self.WizardTk, text="PSU'nun sol üst noktasını işaretleyiniz(sol tık işaretler, sağ tık siler)")
            self.boardLabel.grid(row=2,column=2)
            self.mbCn.unbind('<Button-1>')
            self.mbCn.bind('<Button-1>', self.get_psu_coor)
            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.ursa_state(),state="disabled")
            self.submit_button.grid(row=3,column=2)

    def get_psu_coor(self,event):
        self.psu_corner_circle=self.mbCn.create_oval(event.x-3,event.y-3,event.x+3,event.y+3,outline="red")
        self.psu_coordinate=[event.x*self.reallenght_cm_ratio,event.y*self.reallenght_cm_ratio]
        self.submit_button.configure(state=tk.NORMAL)
        self.mbCn.unbind('<Button-1>')
        self.mbCn.bind('<Button-3>', self.delete_psu_coor)

    def delete_psu_coor(self):
        self.mbCn.delete(self.psu_corner_circle)
        self.submit_button.configure(state='disabled')
        self.mbCn.unbind('<Button-3>')
        self.mbCn.bind('<Button-1>', self.get_psu_coor)

    def ursa_state(self):
        if not self.ursaFlag :
            self.nextframe()
        else:
            self.submit_button.destroy()
            self.boardLabel.destroy()
            self.boardLabel=tk.Label(self.WizardTk, text="URSA'nın sol üst noktasını işaretleyiniz(sol tık işaretler, sağ tık siler)")
            self.boardLabel.grid(row=2,column=2)
            self.mbCn.unbind('<Button-1>')
            self.mbCn.bind('<Button-1>', self.get_ursa_coor)
            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.nextframe(),state="disabled")
            self.submit_button.grid(row=3,column=2)

    def get_ursa_coor(self,event):
        self.ursa_corner_circle=self.mbCn.create_oval(event.x-3,event.y-3,event.x+3,event.y+3,outline="red")
        self.ursa_coordinate=[event.x*self.reallenght_cm_ratio,event.y*self.reallenght_cm_ratio]
        self.submit_button.configure(state=tk.NORMAL)
        self.mbCn.unbind('<Button-1>')
        self.mbCn.bind('<Button-3>', self.delete_ursa_coor)

    def delete_ursa_coor(self):
        self.mbCn.delete(self.ursa_corner_circle)
        self.submit_button.configure(state='disabled')
        self.mbCn.unbind('<Button-3>')
        self.mbCn.bind('<Button-1>', self.get_ursa_coor)



    def kaydet(self):
        print("Sourceboard koordinat",self.SB_coordinates)
        print("Sourceboard LVDS koordinat",self.sb_connector_coordinates)
        if self.TCON_include:
            print("TCON var koordinat:",self.tcon_coordinates)
            print("TCON LVDS koordinat:",self.connector_coordinates)
            print("TCON vida koordinat",self.screw_coordinates)
        if self.TCON_DC_include:
            print("TCON dc kon var",self.TCON_DC_coordinate)
        print("Mainboard koordinat",self.mb_coordinate)
        if self.psuFlag:
            print("PSU koordinat",self.psu_coordinate)
        if self.ursaFlag:
            print("URSA koordinat",self.ursa_coordinate)
        self.dB.addPanel(self)

    def nextframe(self):
        self.nextbutton.destroy()
        self.reallenght_cm_ratio=(self.inch * 2.54 * 0.87)/800
        if self.wizardflags == 0:
            img = cv2.imread(self.imgPath)
            img = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
            pts1= np.float32([self.corner_topleft,self.corner_topright,self.corner_botleft,self.corner_botright])
            pts2 = np.float32([[0,0],[1600,0],[0,900],[1600,900]])
            M = cv2.getPerspectiveTransform(pts1,pts2)
            self.img_transformed = cv2.warpPerspective(img,M,(1600,900))
            cv2.imwrite('Panels/PerspectiveTransformed/' + self.fName + '.jpeg', self.img_transformed)
            print("Saved at  "+'Panels/PerspectiveTransformed/' + self.fName + '.jpeg')
            my_img = Image.open('Panels/PerspectiveTransformed/' + self.fName + '.jpeg')
            my_img = my_img.resize((800,450), Image.ANTIALIAS)
            self.my_img = ImageTk.PhotoImage(my_img)
            self.mbCn.delete(self.image_on_canvas)
            self.mbCn.delete(self.frame)
            self.mbCn.delete(self.corner1)
            self.mbCn.delete(self.corner2)
            self.mbCn.delete(self.corner3)
            self.mbCn.delete(self.corner4)
            self.mbCn.unbind('<Button-1>')
            #self.nextbutton.destroy()
            self.mbCn.config(width=800,height=450)
            self.image_on_canvas=self.mbCn.create_image(400, 225, image=self.my_img,anchor="center")

            self.SB_Label=tk.Label(self.WizardTk, text="Source Board Sayısı")
            self.SB_Label.grid(row=1,column=2)
            self.options_list = [1, 2, 4, 8, 16]
            self.value_inside = tk.IntVar(self.WizardTk)
            self.value_inside.set(self.options_list[1])
            self.question_menu = tk.OptionMenu(self.WizardTk, self.value_inside, *self.options_list)
            self.question_menu.grid(row=1,column=4)
            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.get_SB_option())
            self.submit_button.grid(row=2,column=2)
            #self.mbCn.bind('<Button-1>', self.mbClk_SB)
        if self.wizardflags == 1:
            self.sb_topleftcorners=[]
            self.sb_botrightcorners=[]
            self.SB_rectangles=[]
            self.SB_coordinates=[]
            self.mbCn.bind('<Button-1>', self.SB_label_leftclick)
            self.mbCn.bind('<B1-Motion>', self.SB_label_leftclick_motion)
            self.mbCn.bind('<ButtonRelease-1>', self.SB_label_leftclick_release)
        if self.wizardflags == 2:
            print("Meraba")
            self.submit_button.destroy()
            self.SB_Label.destroy()
            self.question_menu.destroy()
            self.tcon_coordinates=[]
            self.TCON_Q_Label=tk.Label(self.WizardTk, text="TCON var mı?")
            self.TCON_Q_Label.grid(row=1,column=2)
            self.TCON_Q_Label2=tk.Label(self.WizardTk, text="TCON u yerleştiriniz")
            self.TCON_yes_button = tk.Button(self.WizardTk, text='Var', command = lambda:self.TCON_place())
            self.TCON_yes_button.grid(row=1,column=3)
            self.TCON_no_button = tk.Button(self.WizardTk, text='Yok', command = lambda:self.TCON_end())
            self.TCON_no_button.grid(row=1,column=4)
        if self.wizardflags == 3:
            self.mbCn.unbind('<Button-1>')
            self.mbCn.unbind('<B1-Motion>')
            self.mbCn.unbind('<ButtonRelease-1>')
            self.submit_button.destroy()
            self.LVDS_label=tk.Label(self.WizardTk, text="Kaç adet TCON LVDS konektörü var işaretleyiniz( MainBoard ve Sourceboard konektörünü işaretlemeyiniz)")
            self.LVDS_label.grid(row=1,column=2)

            self.options_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
            self.value_inside = tk.IntVar(self.WizardTk)
            self.value_inside.set(self.options_list[2])
            self.question_menu = tk.OptionMenu(self.WizardTk, self.value_inside, *self.options_list)
            self.question_menu.grid(row=1,column=3)
            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.get_connector_option())
            self.submit_button.grid(row=2,column=2)
        if self.wizardflags == 4:
            self.connector_coordinates=[]
            self.con_circles=[]

            self.connector_label_guide=tk.Label(self.WizardTk, text="Yerleştirmek için sol tık ile konektörün orta noktasına tıklayınız, sağ tık son yerleştirilen konektörü siler")
            self.connector_label_guide.grid(row=3,column=2)
            self.connector_label_guide2=tk.Label(self.WizardTk, text="Mainboard konnektörünü İŞARETLEMEYİNİZ")
            self.connector_label_guide2.grid(row=4,column=2)
            self.connector_done_label=tk.Label(self.WizardTk, text=str(self.con_processed)+" adet konektör yerleştirildi")
            self.connector_done_label.grid(row=2,column=2)
            self.mbCn.bind('<Button-1>', self.con_leftclick)
            self.mbCn.bind('<Button-3>', self.con_rightclick)

            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.TCON_screw(), state="disabled")
            self.submit_button.grid(row=5,column=2)

        if self.wizardflags == 5:
            self.TCON_screw_label=tk.Label(self.WizardTk, text="TCON üzerinde kaç adet vida var işaretleyiniz")
            self.TCON_screw_label.grid(row=1,column=2)

            self.options_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            self.value_inside = tk.IntVar(self.WizardTk)
            self.value_inside.set(self.options_list[1])
            self.question_menu = tk.OptionMenu(self.WizardTk, self.value_inside, *self.options_list)
            self.question_menu.grid(row=1,column=3)
            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.get_TCON_screw_option())
            self.submit_button.grid(row=2,column=2)

        if self.wizardflags == 6:
            self.screw_coordinates=[]
            self.screw_circles=[]
            self.screw_label_guide=tk.Label(self.WizardTk, text="Yerleştirmek için sol tık ile vidanın orta noktasına tıklayınız, sağ tık son yerleştirilen vidayı siler")
            self.screw_label_guide.grid(row=2,column=2)
            self.screw_done_label=tk.Label(self.WizardTk, text=str(self.screw_processed)+" adet vida yerleştirildi")
            self.screw_done_label.grid(row=3,column=2)
            self.mbCn.bind('<Button-1>', self.screw_leftclick)
            self.mbCn.bind('<Button-3>', self.screw_rightclick)

            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.TCON_screw_end(),state ="disabled")
            self.submit_button.grid(row=4,column=2)
            #self.save_button=tk.Button(self.WizardTk, text='Kaydet', command = lambda:self.kaydet(),state="disabled")
            #self.save_button.grid(row=4,column=2)

            print("geldik")

        if self.wizardflags == 7:
            self.TCON_Q_Label=tk.Label(self.WizardTk, text="TCON DC konnektör var mı?")
            self.TCON_Q_Label.grid(row=1,column=2)
            self.TCON_Q_Label2=tk.Label(self.WizardTk, text="DC konnektörün orta noktasına tıklayın, yanlış tıklamada tekrar tıklayabilirsin")
            self.TCON_yes_button = tk.Button(self.WizardTk, text='Var', command = lambda:self.TCON_DC_place())
            self.TCON_yes_button.grid(row=1,column=3)
            self.TCON_no_button = tk.Button(self.WizardTk, text='Yok', command = lambda:self.TCON_DC_end())
            self.TCON_no_button.grid(row=1,column=4)

        if self.wizardflags == 8:
            if self.TCON_DC_include :
                self.mbCn.unbind('<Button-1>')
                self.TCON_Q_Label2.destroy()
            self.submit_button.destroy()
            self.SB_LVDS_label=tk.Label(self.WizardTk, text="Kaç adet Sourceboard LVDS konektörü var işaretleyiniz( MainBoard ve TCON konektörünü işaretlemeyiniz)")
            self.SB_LVDS_label.grid(row=1,column=2)

            self.options_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
            self.value_inside = tk.IntVar(self.WizardTk)
            self.value_inside.set(self.options_list[1])
            self.question_menu = tk.OptionMenu(self.WizardTk, self.value_inside, *self.options_list)
            self.question_menu.grid(row=1,column=3)
            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.get_SB_connector_option())
            self.submit_button.grid(row=2,column=2)

        if self.wizardflags == 9:
            self.sb_connector_coordinates=[]
            self.sb_con_circles=[]

            self.connector_label_guide=tk.Label(self.WizardTk, text="Yerleştirmek için sol tık ile konektörün orta noktasına tıklayınız, sağ tık son yerleştirilen konektörü siler")
            self.connector_label_guide.grid(row=3,column=2)
            self.connector_label_guide2=tk.Label(self.WizardTk, text="Mainboard konnektörünü İŞARETLEMEYİNİZ")
            self.connector_label_guide2.grid(row=4,column=2)
            self.connector_done_label=tk.Label(self.WizardTk, text=str(self.con_processed)+" adet konektör yerleştirildi")
            self.connector_done_label.grid(row=2,column=2)
            self.mbCn.bind('<Button-1>', self.sb_con_leftclick)
            self.mbCn.bind('<Button-3>', self.sb_con_rightclick)

            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.SB_LVDS_end(), state="disabled")
            self.submit_button.grid(row=5,column=2)

        if self.wizardflags == 10:
            self.mb_coordinate=[]
            self.psu_coordinate=[]
            self.ursa_coordinate=[]
            self.psuCheck = tk.IntVar()
            self.ursaCheck = tk.IntVar()
            self.psuCheckButton=tk.Checkbutton(self.WizardTk, text="PSU var mı(3in1 şasi ise yok'u işaretleyin)?",variable=self.psuCheck)
            self.psuCheckButton.grid(row=2,column=2)
            self.ursaCheckButton=tk.Checkbutton(self.WizardTk, text="URSA var mı?",variable=self.ursaCheck)
            self.ursaCheckButton.grid(row=3,column=2)

            self.submit_button = tk.Button(self.WizardTk, text='Onayla', command = lambda:self.get_board_check())
            self.submit_button.grid(row=5,column=2)

        if self.wizardflags == 11:
            self.boardLabel.destroy()
            self.mbCn.unbind('<Button-1>')
            self.submit_button.destroy()
            self.save_button=tk.Button(self.WizardTk, text='Kaydet', command = lambda:self.kaydet())
            self.save_button.grid(row=4,column=2)





        #tk.Button(mbTk, text="Next", command = lambda: self.nextframe()).grid()
if __name__ == "__main__":
    app = SampleApp()

    app.mainloop()
