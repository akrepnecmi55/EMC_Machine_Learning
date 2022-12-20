##code: AF
##version: 21
##sapList: "WHK110"
##size: [x,y] -> [24,19]
##screwCoordinates:[[1,1],[23,1],[23,18],[1,18]]
##swVersion: ps1782.27.003.52
##emcParameters: "span, step, amplitude vs"
##panelParameters: "dotfreq, verticalsynq, vs."
##conMatingCoordinates: [LVDS, [0,10]],[DC,[2,19]],[Wifi,[17,6]] vb.
##includes: [PSU,LD,ursa] -> 3in1 [Ursa]-> UrsaOnBoard
##[Ursa,Tcon]->UrsaOnBoard,Tconless

class Mainboard():
    def __init__(self, code, version, sapList, size, screwCoordinates,
                 swVersion, emcParameters, panelParameters,
                 conMatingCoordinates, includes):
        self.code = code
        self.version = version
        self.sapList = sapList
        self.size = size
        self.screwCoordinates = screwCoordinates
        self.swVersion = swVersion
        self.emcParameters = emcParameters
        self.panelParameters = panelParameters
        self.conMatingCoordinates = conMatingCoordinates
        self.includes = includes
        
    
        
