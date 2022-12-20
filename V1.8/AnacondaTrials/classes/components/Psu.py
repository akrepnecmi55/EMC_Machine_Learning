##code: WHE191R
##version: 2
##sapList: WHE140
##size: [20,30]
##screwCoordinates:[][][][] 
##technology: Flyack, LLC
##conMatingCoordinates: [][]
##earthCon: True
##lips: True
##swFreq:2Meg
##ldFreq:1Meg

class Psu():
    def __init__(self, code, version, sapList, size, screwCoordinates,
                 technology, conMatingCoordinates, earthCon, lips,
                 swFreq, ldFreq):
        self.code = code
        self.version = version
        self.sapList = sapList
        self.screwCoordinates = screwCoordinates
        self.technology = technology
        self.conMatingCoordinates = conMatingCoordinates
        self.earthCon = earthCon
        self.lips = lips
        self.swFreq = swFreq
        self.ldFreq = ldFreq

