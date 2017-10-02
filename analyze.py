
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
        #diff of moving avgs
        value = 0.0
        self.indicators['macd_twolines'] = (value, 1.0)
        self.indicators['macd_indicator'] = (value, 1.0)
        self.indicators['macd_reverse'] = (value, 1.0)

    def calc_bollinger_bands(self):
        #bollinger band volatility
        value = 0.0
        self.indicators['bollinger_bands'] = (value, 1.0)

    def calc_breakthrough(self):
        #support/resistance 
        #approaches supp/resist 1 goes to 0, if breakthrough goes to 1
        value = 0.0
        self.indicators['breakthrough'] = (value, 1.0)

