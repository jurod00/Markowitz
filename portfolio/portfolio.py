class Portfolio:

    def __init__(self):

        self.times: list=[]
        self.stocks: list=[]
        self.symbols: list=[]

        self.riskFreeRate: float=float(0.00)

        self.premiumCall: list=[]
        self.strikesCall: list=[]
        self.implVolCall: list=[]
        self.indicesCall: list=[]
        self.symbolsCall: list=[]

        self.premiumPut: list=[]
        self.strikesPut: list=[]
        self.implVolPut: list=[]
        self.indicesPut: list=[]
        self.symbolsPut: list=[]

    def setTimes(self, times: list) -> None:
        self.times = times

    def setStocks(self, stocks: list) -> None:
        self.stocks = stocks

    def setSymbols(self, symbols: list) -> None:
        self.symbols = symbols
        
        
    def setRiskFreeRate(self, riskFreeRate: float) -> None:
        self.riskFreeRate = riskFreeRate

    
    def setPremiumCall(self, premiumCall: list) -> None:
        self.premiumCall = premiumCall

    def setStrikesCall(self, strikesCall: list) -> None:
        self.strikesCall = strikesCall

    def setImplVolCall(self, implVolCall: list) -> None:
        self.implVolCall = implVolCall

    def setIndicesCall(self, indicesCall: list) -> None:
        self.indicesCall = indicesCall

    def setSymbolsCall(self, symbolsCall: list) -> None:
        self.symbolsCall = symbolsCall

    
    def setPremiumPut(self, premiumPut: list) -> None:
        self.premiumPut = premiumPut

    def setStrikesPut(self, strikesPut: list) -> None:
        self.strikesPut = strikesPut

    def setImplVolPut(self, implVolPut: list) -> None:
        self.implVolPut = implVolPut

    def setIndicesPut(self, indicesPut: list) -> None:
        self.indicesPut = indicesPut

    def setSymbolsPut(self, symbolsPut: list) -> None:
        self.symbolsPut = symbolsPut