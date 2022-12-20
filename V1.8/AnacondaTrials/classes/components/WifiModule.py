##code: ZZX190R
##vendor:CVTE
##size: [30,70] (mm)
##bt: True
##band: dual
##swVersion: 1112.2k11lnldkf1.1212
##conMatingCoordinates: [USB,[15,0]],[BT,[20,60]]
##protocols: [a,g,b,n,ac]

class WifiModule():
    def __init__(self, code, vendor, size, bt, band,
                 swVersion, conMatingCoordinates, protocols):
        self.code = code
        self.vendor = vendor
        self.size = size
        self.bt = bt
        self.band = band
        self.swVersion = swVersion
        self.conMatingCoordinates = conMatingCoordinates
        self.protocols = protocols
        

