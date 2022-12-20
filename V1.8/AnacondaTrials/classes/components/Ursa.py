##code: ZGX150
##version: 21
##sapList: "ZGX152"
##size: [x,y] -> [24,19]
##screwCoordinates:[[1,1],[23,1],[23,18],[1,18]]
##swVersion: ps1782.27.003.52
##conMatingCoordinates: [LVDS, [0,10]],[DC,[2,19]],[Wifi,[17,6]] vb.

class Ursa():
    def __init__(self, code, version, sapList, size, screwCoordinates,
                 swVersion, conMatingCoordinates):
        self.code = code
        self.version = version
        self.sapList = sapList
        self.size = size
        self.screwCoordinates = screwCoordinates
        self.swVersion = swVersion
        self.conMatingCoordinates = conMatingCoordinates
        

