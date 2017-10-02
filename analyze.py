
#calcs and uses indicators to determine buy or sell

class Analyze(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.indicators = {'macd': (0.0, 1.0)} #value, weight
        self.evaluation = 0.0
        self.calc_indicators()
        self.evaluate()
    
    def info(self):
        print '[*] analyzing %s' % self.symbol

    def calc_indicators(self):
        self.calc_macd()

    def evaluate(self):
        evaluation = 0.0
        for key in self.indicators:
            value, weight = self.indicators[key]
            evaluation += value * weight
        self.evaluation = evaluation

    def calc_macd(self):
        #macd, reverse macd
        return 0.0

    def calc_volatility(self):
        #bollinger bands
        return 0.0

    def calc_breakthrough(self):
        #support/resistance 
        #approaches supp/resist 1 goes to 0, if breakthrough goes to 1
        return 0.0

