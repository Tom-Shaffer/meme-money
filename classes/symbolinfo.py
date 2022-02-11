class symbolInfo:
        def __init__(self, symbol, additionalData: dict()):
            self.symbol = symbol
            self.hitsOnSubreddit = 0
            if additionalData:
                self.additionalData = additionalData