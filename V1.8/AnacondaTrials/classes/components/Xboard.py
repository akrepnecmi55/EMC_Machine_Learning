##code: BOE90
##version: 2
##size: [50,5]
##screwCoordinates:
##emiTapeCoordinates:
##conMatingCoordinates:
##piecesNum: 4

class Xboard():
    def __init__(self, code, version, size, screwCoordinates,
                 emiTapeCoordinates,conMatingCoordinates, piecesNum):
        self.code = code
        self.version = version
        self.size = size
        self.screwCoordinates = screwCoordinates
        self.emiTapeCoordinates = emiTapeCoordinates
        self.conMatingCoordinates = conMatingCoordinates
        self.piecesNum = piecesNum
        

