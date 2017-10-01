
#calcs and uses indicators to determine buy or sell

class Analyze(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.indicators = {'macd': (1.0, 0.0)}
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
        return 0.0

