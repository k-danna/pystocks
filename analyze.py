
import sys
import random
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import talib as ta
    #list of functions
    #print ta.get_functions()
    #print ta.get_function_groups()
#https://github.com/mrjbq7/ta-lib
#http://www.eickonomics.com/posts/2014-03-25-python-vs-R-adding-TA-
        #indicators/

import config as cfg
from misc import msg

class Analyze(object):
    def __init__(self, symbol, date):
        self.symbol = symbol
        self.date = date
        self.price = 0.0
        self.indicators = self.init_indicators() #indicator: (value, weight)
        self.weights = self.init_indicators(val=1.0)
        self.evaluation = 0.0
        
        self.get_data()
        if self.data.size > 0:
            self.calc_indicators()
            self.evaluate()
    
    def get_data(self):
        #query all dates before self.date
        query = cfg.db.cur.execute(
            'select Date,AdjClose,Volume from %s' % self.symbol)
        query = cfg.db.cur.fetchall()
        data = []
        for item in query:
            if (datetime.strptime(item[0], '%Y-%m-%d') 
                    <= datetime.strptime(self.date, '%Y-%m-%d')
                    and item[1] != 'null'):
                data.append(item)
            else:
                break
        #for backtest
        self.price = float(data[-1][1]) if len(data) > 0 else 0.0
        #unpack data
        self.data = np.asarray(data)
        self.indicators['date'] = np.asarray([datetime.strptime(x, 
                '%Y-%m-%d') for x in self.data[:, 0]])
        self.indicators['price'] = np.asarray([float(x) 
                for x in self.data[:, 1]])
        self.indicators['volume'] = np.asarray([float(x) 
                for x in self.data[:, 2]])

    def init_indicators(self, val=0.0):
        indicators = {}
        self.indicator_listing = ['macd','macdsignal','macdhist']
        for indicator in self.indicator_listing:
            indicators[indicator] = val
        return indicators

    def calc_indicators(self):
        #calc macd
        macd, macdsignal, macdhist = ta.MACD(self.indicators['price'], 
                fastperiod=12, slowperiod=26, signalperiod=9)
        self.indicators['macd'] = macd
        self.indicators['macdsignal'] = macdsignal
        self.indicators['macdhist'] = macdhist

        #calc ema
        self.indicators['ema12'] = ta.EMA(self.indicators['price'],
            timeperiod=12)
        self.indicators['ema26'] = ta.EMA(self.indicators['price'],
            timeperiod=26)

        #calc bollinger bands
        upper, middle, lower = ta.BBANDS(self.indicators['price'],
            timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        self.indicators['upperbollinger'] = upper
        self.indicators['middlebollinger'] = middle
        self.indicators['lowerbollinger'] = lower

        self.plot(['price', 'ema12', 'ema26'], days=100)
        self.plot(['price', 'upperbollinger', 'middlebollinger',
                'lowerbollinger'], days=100)
        #FIXME:
        #self.indicators.plot(y=['prices'])

        sys.exit()

    def plot(self, keys, days=0):
        for key in keys:
            y = self.indicators[key][-days:-1]
            x = self.indicators['date'][-days:-1]
            if key == 'price':
                plt.plot(x, y,'b-', color='black', label=key)
            else:
                plt.plot(x, y,'-', label=key)
        #plt.title('FIXME')
        plt.xlabel('date')
        plt.ylabel('price')
        plt.legend(loc='best')
        plt.show()

    def evaluate(self):
        evaluation = 0.0
        for key in self.indicators:
            evaluation += self.indicators[key] * self.weights[key]
        self.evaluation = evaluation
        
        #random evaluation
        if cfg.random_trades:
            scalar = 1 if random.random() < 0.5 else -1
            self.evaluation = scalar * random.random()

#chooses symbol based on evaluation
def best_eval(evals):
    best = ()
    for symbol in evals:
        if not evals[symbol].data.size > 0: #no nflx data until 2002
            continue
        if not best or abs(evals[symbol].evaluation) > abs(best[1]):
            best = (symbol, evals[symbol].evaluation)
    return evals[best[0]]

def pick_trade(choice):
    min_buypower = cfg.minshares * choice.price + 2 * cfg.commission
    min_sellpower = cfg.commission
    buypower = cfg.api.account_buypower()
    shares = int(buypower / choice.price)
    position = cfg.api.account_positions()[choice.symbol][0]

    #debug print reason for no trade
    if choice.evaluation > 0:
        print '    BUYING'
        if choice.evaluation <= cfg.eval_threshold:
            print '        NO BUY: eval below threshold %s' % (
                    cfg.eval_threshold,)
        if buypower <= min_buypower:
            print '        NO BUY: not enough buypower %s < %s' % (buypower,
                    min_buypower)
        if position > 0:
            print '        NO BUY: already holding a position'

    if choice.evaluation < 0:
        print '    SELLING'
        if choice.evaluation >= cfg.eval_threshold:
            print '        NO SELL: eval below threshold %s' % (
                    cfg.eval_threshold,)
        if buypower <= min_sellpower:
            print '        NO SELL: not enough sellpower %s < %s' % (
                    buypower, min_sellpower)
        if position <= 0:
            print '        NO SELL: no shares to sell'

    #buy
    if (choice.evaluation > cfg.eval_threshold 
            and buypower > min_buypower and position <= 0):
        return (choice.symbol, choice.price, shares)
    #sell
    elif (choice.evaluation < cfg.eval_threshold 
            and buypower > min_sellpower and position > 0):
        return (choice.symbol, choice.price, -shares)
    #do nothing
    return (choice.symbol, choice.price, 0.0)

