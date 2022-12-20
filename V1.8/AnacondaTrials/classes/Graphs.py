import os
import sys
sys.path.insert(0, "..")
try:
    import numpy as np
    import cv2
    import matplotlib.pylab as plt
    import matplotlib.pyplot as plot 
    'exec(%matplotlib inline)'
except ImportError:
    print('No Import')


##from io import BytesIO
##from PIL import image
lower_range_axis = np.array([-10,-10,-40])
upper_range_axis = np.array([10,10,40])
lower_range_Limit = np.array([-10,173,215])
upper_range_Limit = np.array([10,193,295])
lower_range_Red_Vrt = np.array([160,143,215])
upper_range_Red_Vrt = np.array([180,163,295])
lower_range_Blue_Hrz = np.array([95,92,215])
upper_range_Blue_Hrz = np.array([115,112,295])
lower_range_Peak_Points = np.array([93, 174, 182])
upper_range_Peak_Point = np.array([113, 194, 262])
##global xAxisLength
##global yAxisLength
##global yOrigin
##global xOrigin
##[0 0 0] [-10 -10 -40] [10 10 40]
class Graph:

    def __init__(self, revision, im):
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        y = im.shape[0]
        x = im.shape[1]
        self.hsv = hsv
        self.y = y
        self.x = x
    def getHSV():
        return self.hsv
    def getY():
        return self.y
    def getX():
        return self.x


class FirstGraph(Graph):
    def __init__(self, revision, im):
        Graph.__init__(self, revision, im)
        hsv = self.hsv
        maskedLimit = cv2.inRange(hsv, lower_range_Limit, upper_range_Limit)
        y = self.y
        x = self.x
        threshold = 0
        i=1;
        ch = False
        while(i < 8):
            j=0
            while(j < y):
                if(maskedLimit[j,(int)(i*x/8)] == 255):
                    k = 0
                    while(k < x):
                        if(maskedLimit[j,k] == 255):
                            threshold = threshold + 1
                        k = k + 1
                    if(threshold >= (int)(x/3)):
##                        print("first class daki y47 ",threshold)
                        ch = True
                        f_limit47Length = threshold
                        f_y47 = j
                        break
                    else:
                        threshold = 0
                if(ch):
                    break
                j = j + 1
            if(ch):
                break
            i = i + 1
        #47 dB limitinin x ekseni uzunluğu
        self.f_limit47Length = f_limit47Length
##        print("FirstGraph: lim47: ", f_limit47Length)
        #47 dB limitinin y eksenindeki hizası
        self.f_y47 = f_y47
        
        threshold = 0
        i=1;
        ch = False
        while(i < 24):
            j=0
            while(j < y):
                if(maskedLimit[j,(int)(i*x/24)] == 255):
                    k = 0
                    while(k < x):
                        if(maskedLimit[j,k] == 255):
                            threshold = threshold + 1
                        k = k + 1
                    if(threshold >= (int)(f_limit47Length/5) and threshold < (int)(f_limit47Length/2)):
##                        print("first class daki y40 ",threshold)
                        f_limit40Length = threshold
                        ch = True
                        f_y40 = j
                        break
                    else:
                        threshold = 0
                if(ch):
                    break
                j = j + 1
            if(ch):
                break
            i = i + 1
        #40 dB limitinin x ekseni uzunluğu
        self.f_limit40Length = f_limit40Length
##        print("FirstGraph: lim40: ", f_limit40Length)
        #40 dB limitinin y eksenindeki hizası
        self.f_y40 = f_y40

        axis_y_low = (int)(f_y40-((f_y40-f_y47)/7*(40+5)))
        axis_y_up = (int)(f_y40+((f_y40-f_y47)/7*(40+5)))
        axis_x_up = 3800
        axis_x_low = 400
        im = im[axis_y_low:axis_y_up,axis_x_low:axis_x_up,:]
        empY = axis_y_up-axis_y_low
        empX = axis_x_up-axis_x_low
        self.im = im
        
class BasicGraph(FirstGraph):
    
    def __init__(self, revision, im):
        FirstGraph.__init__(self, revision, im)
        im = self.im
        print("im shape: ",im.shape)
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        y = im.shape[0]
        x = im.shape[1]
        self.hsv = hsv
        self.y = y
        self.x = x
        maskedAxis = cv2.inRange(hsv, lower_range_axis, upper_range_axis)
        maskedLimit = cv2.inRange(hsv, lower_range_Limit, upper_range_Limit)
        maskedVrtData = cv2.inRange(hsv, lower_range_Red_Vrt, upper_range_Red_Vrt)
        maskedHrzData = cv2.inRange(hsv, lower_range_Blue_Hrz, upper_range_Blue_Hrz)
        maskedPkPnts = cv2.inRange(hsv, lower_range_Peak_Points, upper_range_Peak_Point)
##        plot.imshow(maskedAxis)
##        plot.show()
        threshold = 0;
        i=1;
        ch = False
        while(i < 5):
            j=0
            while(j < y):
                if(maskedAxis[j,(int)(i*x/5)] == 255):
                    k = 0
                    while(k < x):
                        if(maskedAxis[j,k] == 255):
                            threshold = threshold + 1
                        k = k + 1
                    if(threshold >= (int)(x/4)):
                        print(threshold)
                        ch = True
                        xAxisLength = threshold
                        yOrigin = j
                        break
                    else:
                        threshold = 0
                if(ch):
                    break
                j = j + 1
            if(ch):
                break
            i += 1

        threshold = 0;
        i=1;
        ch = False
        while(i < (int)(y/(xAxisLength/6))):
            j=0
            while(j < x):
                if(maskedAxis[(int)(i*(xAxisLength/5)),j] == 255):
                    k = 0
                    while(k < y):
                        if(maskedAxis[k,j] == 255):
                            threshold = threshold + 1
                            #print("th: ", threshold)
                        k = k + 1
                    if(threshold >= (int)(xAxisLength/4)):
                        #print(threshold)
                        ch = True
                        yAxisLength = threshold
                        xOrigin = j
                        break
                    else:
                        threshold = 0
                if(ch):
                    break
                j = j + 1
            if(ch):
                break
            i = i + 1
        #revision 1 ilk deneme demek hiçbir modifin yapılmadığı
        self.revision = revision
        #orijin noktasının y bileşeni
        self.yOrigin = yOrigin
        #orijin noktasının x bileşeni
        self.xOrigin = xOrigin
        #x Axis'in uzunluğu (araya gürültü girdiyse yanlış bilgi verebilir)
        self.xAxisLength = xAxisLength
        #y Axis'in uzunluğu (araya gürültü girdiyse yanlış bilgi verebilir)
        self.yAxisLength = yAxisLength

        threshold = 0
        i=1;
        ch = False
        while(i < 5):
            j=0
            while(j < y):
                if(maskedLimit[j,(int)(i*x/5)] == 255):
                    k = 0
                    while(k < x):
                        if(maskedLimit[j,k] == 255):
                            threshold = threshold + 1
                        k = k + 1
                    if(threshold >= (int)(xAxisLength*2/3)):
                        #print(threshold)
                        ch = True
                        limit47Length = threshold
                        y47 = j
                        break
                    else:
                        threshold = 0
                if(ch):
                    break
                j = j + 1
            if(ch):
                break
            i = i + 1
        #47 dB limitinin x ekseni uzunluğu
        self.limit47Length = limit47Length
        #47 dB limitinin y eksenindeki hizası
        self.y47 = y47
        
        threshold = 0
        i=1;
        ch = False
        while(i < 8):
            j=0
            while(j < y):
                if(maskedLimit[j,(int)(i*x/8)] == 255):
                    k = 0
                    while(k < x):
                        if(maskedLimit[j,k] == 255):
                            threshold = threshold + 1
                        k = k + 1
                    if(threshold >= (int)(xAxisLength/6) and threshold < (int)(xAxisLength/4.5)):
                        #print(threshold)
                        limit40Length = threshold
                        ch = True
                        y40 = j
                        break
                    else:
                        threshold = 0
                if(ch):
                    break
                j = j + 1
            if(ch):
                break
            i = i + 1
        #40 dB limitinin x ekseni uzunluğu
        self.limit40Length = limit40Length
        #40 dB limitinin y eksenindeki hizası
        self.y40 = y40

        i=x-1
        th=0
        ch = False
        while(i>1):
            if 255 in maskedVrtData[:,i]:
                j=1
                while(j<10):
                    if 255 not in maskedVrtData[:,i-j]:
                        i = i-j+1
                        th=0
                        break
                    else:
                        th += 1
                    j+=1
                if th >= 9:
                    lastDataX = i
                    ch = True
                    break
            if(ch):
                break
            i = i - 1

        self.lastDataX = lastDataX
        unitY = (int)((yOrigin - y47)/47)
        #1 birim y kaç pixel
        self.unitY = unitY
        y80 = (int)(y40-(yOrigin - y40))
        #80 dBm in y kordinatı
        self.y80 = y80
        #80dBm den 0'a kadar pixel boyutu y ekseninde
        yLength = yOrigin - y80
        self.yLength = yLength
##Axisin başlangıcı ve btişleri bulunacak!!!
        i = xOrigin + 2*unitY
        print("unit Y is ", unitY)
        print("xOrigin is: ", xOrigin)
        ch = False
        fault = False
        counted = 0
        misCounted = 0
        cFnd = False
        while(i < x):
            j = 0
            cFnd = False
            while(j < (int)(unitY*30)):
                ctr = 0
                tm = (int)(yOrigin - unitY*1.5)
                while(tm < (int)(yOrigin + unitY*1.5)):
                    if(maskedAxis[tm, i+j]==255):
                        ctr += 1
                    tm += 1
                #print("unitY is: ", unitY, " while ctr is: ", ctr)
                if(ctr >= int(1.3*unitY)):
                    counted += 1
                    tempLastX = i+j
                    i = i+j+unitY
                    print("x: ",tempLastX,"'de bir tik bulundu")
                    cFnd = True
                    break
                j += 1
            if(not cFnd):
                misCounted += 1
                print("miscounted", misCounted)
            if(misCounted < 2):
                if(misCounted + counted == 10):
                    lastXAxis = tempLastX
                    break
            else:
                print("hiç sayamadı ki bu :/ çıkıyoruz. Mişın komprımayzd")
                break
            i += 1
        self.lastXAxis = lastXAxis


        i = 0
        while(True):
            try:
                i += 1
                csvLists = [np.any(map(str,line.split())) for line in open('images/ex2.csv')]
                print("csv file opened")
                break
            except:
                if(i >= 5000):
                    print("time is up! couldn't open csv File!")
                    break

        i=4;
        peakNum=0
        polCol = -3
        ch = False
        peakPnts = []
        peakPnts_V = []
        peakPnts_H = []
        for x in csvLists[0]:
            tmpList = x.split(',')
            s = -1
            t = 0
            for x in tmpList:
                if('Frequency' in tmpList[t]):
                    freqCol = t
                if('Quasi' in tmpList[t]):
                    quasCol = t
                if(tmpList[s] == 'Pol'):
                    polCol = s
                    break
##                print("s: ", s)
                s -= 1
                t += 1

##        print("polcol is: ", polCol)
        i=0
        for a in csvLists:
            for b in csvLists[i]:
                tmpList = b.split(',')
                if(len(tmpList) > 3):
                    if(tmpList[polCol] == 'V' or tmpList[polCol] == 'H'):
                        try:
                            peakPnts.append([float(tmpList[freqCol]),float(tmpList[quasCol])])
                            if(tmpList[polCol] == 'V'):
                                peakPnts_V.append([float(tmpList[freqCol]),float(tmpList[quasCol])])
                            else:
                                peakPnts_H.append([float(tmpList[freqCol]),float(tmpList[quasCol])])
##                            print("eklendi")
                        except:
                            ch = True
##                            print("hata burda oluştu")
                            break
                else:
                    peakNum = i-4
##                    print("kolon 3 ten az")
                    #ch = True
                    #break
            if(ch):
                break
            i += 1
##        print("list length: ", peakNum)
        #peakPnts = np.array(peakPnts)
        try:
            print(peakPnts[0][0])
        except:
            print("marja yakın yok!")
## Önce PDF'ten tabula yardımıyla çıkarılan peak pointleri MaskedVrtData ve
## MaskedHrzData ya yerleştir
## Sonra gürültüleri ayıklayarak smootla
## Sonra arada eksik olan dataları interpolasyonla bul ve yaz
## Sonra birden fazla datanın yüklenebilmesi için dosya yükleme uygulaması
## Daha sonra yüklenen her yeni datanın kategorileriyle birlikte cvs e yazılması
## Sonra deep learning

        #vrtData = [[0 for x in range(971)]]
        vrtData = []
        hrzData = []
        for i in range(971):
            vrtData.append(0)
            hrzData.append(0)
        i = 0
        for a in peakPnts_V:
            tmpI = vrtData[int((peakPnts_V[i][0] - 30))]
            if(tmpI < peakPnts_V[i][1] + unitY):
                vrtData[int((peakPnts_V[i][0] - 30))] = peakPnts_V[i][1] + 0.5
##                print(int((peakPnts_V[i][0])),"'a ",peakPnts_V[i][1], " yazıldı")
            i += 1
##        i = 0
##        for a in peakPnts_H:
##            tmpI = hrzData[int((peakPnts_H[i][0] - 30))]
##            if(tmpI < peakPnts_H[i][1] + unitY):
##                hrzData[int((peakPnts_H[i][0] - 30))] = peakPnts_H[i][1] + unitY
####                print(int((peakPnts_H[i][0])),"'a ",peakPnts_H[i][1], " yazıldı")
##            i += 1
        xLn = lastXAxis - xOrigin
        i = 0
        while(i < xLn):
            j=0
            while(j < yLength):
                if(maskedVrtData[y80+j,i+xOrigin] == 255):
                    if(vrtData[int(i*971/xLn)] < float((y40-(y80+j))/unitY+40)):
                        t_x = int(-unitY/2)
                        t_y = int(-unitY/2)
                        th=0
                        for a in range(unitY):
                            for b in range(unitY):
                                if(maskedVrtData[y80+j+t_y,i+xOrigin+t_x] == 255):
                                    th += 1
                                if(maskedHrzData[y80+j+t_y,i+xOrigin+t_x] == 255):
                                    th += 1
                                t_y += 1
                            t_x += 1
                        if(th >= int(unitY*unitY/9)):
                            vrtData[int(i*971/xLn)] = float((y40-(y80+j))/unitY+40)
##                            print("x: ", int(i*971/xLn), " y: ", float((y40-(y80+j))/unitY+40))
                    else:
                        break
                j += 1
            i += 1
        i=0
        while(i < 971):
            if(vrtData[i]==0):
                j = i+1
                div = 1
                while(j < 971):
                    if(vrtData[j]!=0):
                        lastD = j
                        break
                    div += 1
                    j += 1
                if( i == 0):
                    g = i
                    for a in range(div):
                        vrtData[g] = vrtData[j]
                        g += 1
                        i = i + div
                elif( i == 970):
                    g = 970
                    for a in range(970 - lstDH):
                        vrtData[g] = vrtData[lstDH]
                        g -= 1
                else:
                    g = i
                    inc = float((vrtData[j]-vrtData[i-1])/(div+1))
                    ml = 1
                    for a in range(div):
                        vrtData[g] = vrtData[i-1] + inc*ml
                        g += 1
                        ml += 1
                    i = i + div
            else:
                lstDH = i    
            i += 1

##        i = 0
##        print("smoothed vrtData as follows: ")
##        while(i < 971):
##            print("x: ", i+30, " y: ", vrtData[i])
##            i += 1
        self.vrtData = vrtData

        i = 0
        while(i < xLn):
            j=0
            while(j < yLength):
                rCh = False
                if(maskedHrzData[y80+j,i+xOrigin] == 255):
                    if(maskedVrtData[y80+j-2,i+xOrigin] == 255):
                        rCh = True
                    th=0
                    ctr = 0
                    for a in range(int(2*unitY)):
                        if(maskedHrzData[y80+j+ctr,i+xOrigin] == 255):
                            th += 1
                    if(th < int(1.5*unitY) and rCh):
                        break
                    if(hrzData[int(i*971/xLn)] < float((y40-(y80+j))/unitY+40)):
                        t_x = int(-unitY/2)
                        t_y = int(-unitY/2)
                        th=0
                        for a in range(unitY):
                            for b in range(unitY):
                                if(maskedVrtData[y80+j+t_y,i+xOrigin+t_x] == 255):
                                    th += 1
                                if(maskedHrzData[y80+j+t_y,i+xOrigin+t_x] == 255):
                                    th += 1
                                t_y += 1
                            t_x += 1
                        if(th >= int(unitY*unitY/9)):
                            hrzData[int(i*971/xLn)] = float((y40-(y80+j))/unitY+40)
                            print("horizantal x: ", int(i*971/xLn) + 30, " y: ", float((y40-(y80+j))/unitY+40))
                    else:
                        break
                j += 1
            i += 1
            
        i = 0
        for a in peakPnts_H:
            tmpI = hrzData[int((peakPnts_H[i][0] - 30))]
            if(tmpI < peakPnts_H[i][1] + unitY):
                hrzData[int((peakPnts_H[i][0] - 30))] = peakPnts_H[i][1] + 0.5
##                print(int((peakPnts_H[i][0])),"'a ",peakPnts_H[i][1], " yazıldı")
            i += 1

        i=0
        while(i < 971):
            if(hrzData[i]==0):
                hrzData[i] = vrtData[i]
            i += 1

        i = 0
        print("smoothed hrzData as follows: ")
        while(i < 971):
            print("x: ", i+30, " y: ", hrzData[i])
            i += 1
        self.hrzData = hrzData
