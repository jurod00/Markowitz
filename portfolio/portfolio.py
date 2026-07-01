class Portfolio:

    def __init__(self):

        self.times: list=None
        self.stocks: list=None
        self.symbols: list=None

        self.riskFreeRate: float=None

        self.premiumCall: list=None
        self.strikesCall: list=None
        self.implVolCall: list=None
        self.indicesCall: list=None
        self.symbolsCall: list=None

        self.premiumPut: list=None
        self.strikesPut: list=None
        self.implVolPut: list=None
        self.indicesPut: list=None
        self.symbolsPut: list=None

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