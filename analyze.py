
import random

import config as cfg
from misc import *

class Analyze(object):
    def __init__(self, symbol, date):
        self.symbol = symbol
        self.indicators = {'macd': (0.0, 1.0)} #value, weight
        self.evaluation = 0.0
        self.date = date
        self.price = 0.0

        self.calc_indicators()
        self.evaluate()
    
    def info(self):
        msg('analyzing %s %s' % (self.symbol, self.date))

    def calc_indicators(self):
        #FIXME: query needed info
            #only one query, used by all methods
        #query date in table for quotes, splits, dividends
        data = cfg.db.cur.execute(
            'select * from %s where Date=?' % self.symbol, (self.date,)
        )
        data = cfg.db.cur.fetchall()

        if len(data) == 0:
            #msg('no data: %s' % self.symbol)
            return

        #unpack data
        ID, Date, Open, High, Low, Close, AdjClose, Volume = data[0]
        #msg(Date)
        #msg(Open)
        #msg(High)
        #msg(Low)
        #msg(Close)
        #msg(AdjClose)
        #msg(Volume)

        #debug
        self.price = AdjClose

        #FIXME: normalize for splits, dividends
            #close adjusted for splits
            #adjclose adjusted for splits, dividends

        #query prev info / indicators
            #dont recalculate
        #if indicators missing
            #calc and insert
        self.calc_macd()

    def evaluate(self):
        evaluation = 0.0
        for key in self.indicators:
            value, weight = self.indicators[key]
            evaluation += value * weight
        self.evaluation = evaluation
        
        if cfg.random_trades:
            scalar = 1 if random.random() < 0.5 else -1
            self.evaluation = scalar * random.random() * 10

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

