##shieldType:
##    DS doubleshielded
##    SS singleShielded
##    NS noshield
##    FS fullShield
##vendor:
##    vendorname
##length:
##    length of the cable
##pinNumber:
##    pin count of the cable
##con1&con2:
##    connector terminal types: snap, loch, GNDlock
##mate1&mate2:
##    connected units: mainboard-ursa / ursa-tcon / tcon-xboard?
##wireType:
##    LVDS twistedpair or FPC?


class Cable():
    def __init__(self, shape, shield, _type, color, width):
        self.shape = shape
        print("Cable class: shape: ", shape)
        self.shield = shield
        print("Cable class: shield: ", shield)
        self._type = _type
        print("Cable class: _type: ", _type)
        self.color = color
        print("Cable class: color: ", color)
        self.width = width
        print("Cable class: width: ", width)
        self.coords = []

    def getCoords(self):
        return self.coords
        
    def setCoords(self, x):
        self.coords = x
        
    def addCoords(self, x):
        for i in x:
            self.coords.append(i)
            
    def shldTypeShiftUp(self):
        it = list(self.shieldTypes).index(self.shield)
        lgt = len(self.shieldTypes)
        tmpIt = (it + 1) % lgt
        print("it was: ", self.shield)
        self.shield = list(self.shieldTypes)[tmpIt]
        print("now it is: ", self.shield, " and it means: ", self.shieldTypes[self.shield])
        
    def shldTypeShiftDwn(self):
        it = list(self.shieldTypes).index(self.shield)
        lgt = len(self.shieldTypes)
        tmpIt = (it - 1) % lgt
        print("it was: ", self.shield)
        self.shield = list(self.shieldTypes)[tmpIt]
        print("now it is: ", self.shield, " and it means: ", self.shieldTypes[self.shield])

class LVDS(Cable):
    def __init__(self):
        super().__init__('flat', 'NS', 'LVDS','#0101FF', 2)
        self.shieldTypes = {
            'NS': 'No Shield',
            'SS': 'SingleShield',
            'DS': 'Double Shield'
        }
        print("sub class LVDS oluşturuldu")


class DC(Cable):
    def __init__(self):
        super().__init__('Cylindir', 'NS', 'DC','#444401', 1)
        self.shieldTypes = {
            'NS': 'No Shield',
            'CS': 'Circular Shield'
        }
        print("sub class DC oluşturuldu")
        
class VBY1(Cable):
    def __init__(self):
        super().__init__('flat', 'NS', 'VBY1','#0111FF', 2)
        self.shieldTypes = {
            'NS': 'No Shield',
            'SS': 'SingleShield',
            'DS': 'Double Shield'
        }
        print("sub class VBY1 oluşturuldu")
        
class MLVDS(Cable):
    def __init__(self):
        super().__init__('flat', 'NS', 'MLVDS','#011111', 2.5)
        self.shieldTypes = {
            'NS': 'No Shield',
            'SS': 'SingleShield',
            'DS': 'Double Shield'
        }
        print("sub class MLVDS oluşturuldu")
        
class WIFI(Cable):
    def __init__(self):
        super().__init__('Cylindir', 'CS', 'WIFI','#31F111', 0.7)
        self.shieldTypes = {
            'NS': 'No Shield',
            'CS': 'Circular Shield'
        }
        print("sub class WIFI oluşturuldu")

class AC(Cable):
    def __init__(self):
        super().__init__('Cylindir', 'NS', 'AC','#111111', 0.4)
        self.shieldTypes = {
            'NS': 'No Shield',
            'CS': 'Circular Shield'
        }
        print("sub class AC oluşturuldu")
        
class FPC(Cable):
    def __init__(self):
        super().__init__('flat', 'NS', 'FPC','#223311', 0.8)
        self.shieldTypes = {
            'NS': 'No Shield',
            'SS': 'SingleShield',
            'DS': 'Double Shield'
        }
        print("sub class FPC oluşturuldu")

class BT_ANT(Cable):
    def __init__(self):
        super().__init__('Cylindir', 'NS', 'BT_ANT','#441188', 0.2)
        self.shieldTypes = {
            'NS': 'No Shield',
            'CS': 'Circular Shield'
        }
        print("sub class BT_ANT oluşturuldu")

class WF_ANT(Cable):
    def __init__(self):
        super().__init__('Cylindir', 'NS', 'WF_ANT','#4411AA', 0.2)
        self.shieldTypes = {
            'NS': 'No Shield',
            'CS': 'Circular Shield'
        }
        print("sub class WF_ANT oluşturuldu")
        
class SPK(Cable):
    def __init__(self):
        super().__init__('Cylindir', 'NS', 'SPK','#AAFF22', 0.5)
        self.shieldTypes = {
            'NS': 'No Shield',
            'CS': 'Circular Shield'
        }
        print("sub class SPK oluşturuldu")

def cblSel(x):
    print("cblSel e girdi")
    if x == 'LVDS':
        print("LVDS secildi")
        return LVDS()
    elif x == 'DC':
        return DC()
    elif x == 'VBY1':
        return VBY1()
    elif x == 'MLVDS':
        return MLVDS()
    elif x == 'WIFI':
        return WIFI()
    elif x == 'AC':
        return AC()
    elif x == 'FPC':
        return FPC()
    elif x == 'BT_ANT':
        return BT_ANT()
    elif x == 'WF_ANT':
        return WF_ANT()
    elif x == 'SPK':
        return SPK()
    
    


# class Vby1(Cable):
    # def __init__(self, shielType, vendor, length, pinNumber,
                 # con1, con2, mate1, mate2):
        # Cable.__init__(self, shielType, vendor, length, pinNumber)
        # self.con1 = con1
        # self.con2 = con2
        # self.mate1 = mate1
        # self.mate2 = mate2


# class DC(Cable):
    # def __init__(self, shielType, vendor, length, pinNumber, mate1, mate2):
        # Cable.__init__(self, shielType, vendor, length, pinNumber)
        # self.mate1 = mate1
        # self.mate2 = mate2


# class FPC(Cable):
    # def __init__(self, shielType, vendor, length, pinNumber, mate1, mate2):
        # Cable.__init__(self, shielType, vendor, length, pinNumber)
        # self.mate1 = mate1
        # self.mate2 = mate2

# class AC(Cable):
    # def __init__(self, shielType, vendor, length, pinNumber, mate1, earthCon):
        # Cable.__init__(self, shielType, vendor, length, pinNumber)
        # self.mate1 = mate1
        # self.earthCon = earthCon
