##code: xxx
##version: 2
##sapList: "asdasdr"
##size: [x,y] -> [24,19]
##screwCoordinates:[[1,1],[23,1],[23,18],[1,18]]
##conMatingCoordinates: [LVDS, [0,10]],[DC,[2,19]],[Wifi,[17,6]] vb.

class Tcon():
    def __init__(self, code, version, size, screwCoordinates,
                 conMatingCoordinates):
        self.code = code
        self.version = version
        self.size = size
        self.screwCoordinates = screwCoordinates
        self.conMatingCoordinates = conMatingCoordinates
        

