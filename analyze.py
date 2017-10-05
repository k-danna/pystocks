
import sys
import random
import numpy as np
import talib as ta
    #list of functions
    #print ta.get_functions()
    #print ta.get_function_groups()
#https://github.com/mrjbq7/ta-lib
#http://www.eickonomics.com/posts/2014-03-25-python-vs-R-adding-TA-
        #indicators/
import config as cfg
from misc import *

class Analyze(object):
    def __init__(self, symbol, date):
        self.symbol = symbol
        self.date = date
        self.indicators = {'macd': (0.0, 1.0)} #indicator: (value, weight)
        self.evaluation = 0.0
        self.price = 0.0

        self.calc_indicators()
        self.evaluate()
    
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

        #functions by group
        #groups = ta.get_function_groups()
        #for group in groups:
        #    print group
        #    print '    ' + str(groups[group])
        #    print

        #debug
        #sys.exit()

        #FIXME: normalize for splits, dividends
            #close adjusted for splits
            #adjclose adjusted for splits, dividends

        #query prev info / indicators
            #dont recalculate
        #if indicators missing
            #calc and insert
        pass

    def evaluate(self):
        evaluation = 0.0
        for key in self.indicators:
            value, weight = self.indicators[key]
            evaluation += value * weight
        self.evaluation = evaluation
        
        if cfg.random_trades:
            scalar = 1 if random.random() < 0.5 else -1
            self.evaluation = scalar * random.random()

#chooses symbol based on evaluation
def best_eval(evals):
    best = ()
    for symbol in evals:
        if evals[symbol].price == 0.0: #no NFLX data until 2002
            continue
        if not best or abs(evals[symbol].evaluation) > abs(best[1]):
            best = (symbol, evals[symbol].evaluation)
    return evals[best[0]]

def pick_trade(choice):
    min_buypower = cfg.minshares * choice.price + 2 * cfg.commission
    min_sellpower = cfg.commission
    shares = int(cfg.account.buypower / choice.price)
    #buy
    if (choice.evaluation > cfg.eval_threshold 
            and cfg.account.buypower > min_buypower):
        return (choice.symbol, choice.price, shares)
    #sell
    elif (choice.evaluation < cfg.eval_threshold 
            and cfg.account.buypower > min_sellpower):
        return (choice.symbol, choice.price, -shares)
    #do nothing
    return (choice.symbol, choice.price, 0.0)










