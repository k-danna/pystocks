
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
        self.evaluation = 0.0
        self.indicator_listing = ['macd', 'bollinger', 'rsi', 'obv']

        self.indicators = self.init_indicators()
        self.weights = self.init_indicators(val=1.0)
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
                    <= datetime.strptime(self.date, '%Y-%m-%d')):
                if item[1] != 'null':
                    data.append(item)
            else:
                break

        #unpack data
        self.data = np.asarray(data)
        self.price = float(data[-1][1]) if len(data) > 0 else 0.0
        self.indicators['date'] = np.asarray([datetime.strptime(x, 
                '%Y-%m-%d') for x in self.data[:, 0]])
        self.indicators['price'] = np.asarray([float(x) 
                for x in self.data[:, 1]])
        self.indicators['volume'] = np.asarray([float(x) 
                for x in self.data[:, 2]])

    def init_indicators(self, val=0.0):
        indicators = {}
        for indicator in self.indicator_listing:
            indicators[indicator] = val
        return indicators

    def calc_indicators(self):
        #horizontal line data useful for plotting
        self.indicators['zero'] = np.asarray([0.0 for _ in 
                self.indicators['price']])
        self.indicators['fifty'] = np.asarray([50.0 for _ in 
                self.indicators['price']])

        #macd
            #macddiff = 12ema - 26ema
            #macdsignal = 9ema of macd
            #macdhist = macd - signal
        macd_ind, macd_signal, macd_hist = ta.MACD(self.indicators['price'],
                fastperiod=12, slowperiod=26, signalperiod=9)
        self.indicators['macd_ind'] = macd_ind
        self.indicators['macd_signal'] = macd_signal
        self.indicators['macd_hist'] = macd_hist
        #macd signal crossover
        today = macd_ind[-1] - macd_signal[-1]
        yesterday = macd_ind[-2] - macd_signal[-2]
        #macd crosses above signal --> buy
        if today > 0 and yesterday < 0:
            self.indicators['macd'] = 1.0
        #macd crosses below signal --> sell
        elif today < 0 and yesterday > 0:
            self.indicators['macd'] = -1.0

        #debug
        if yesterday * today < 0 and self.indicators['macd'] == 0.0:
            print '        CROSSOVER ERROR: ', yesterday, today
            print self.indicators['macd']
            sys.exit()

        #other indicators
            #price diverges from macd --> end of current trend
            #macd rises dramatically --> overbought and will return normal
            #macd above zero --> upward momentum
        #macd below zero --> downward momentum
        
        #calc bollinger bands
            #middle = 21sma
        upper, middle, lower = ta.BBANDS(self.indicators['price'],
            timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        self.indicators['bollinger_upper'] = upper
        self.indicators['bollinger_middle'] = middle
        self.indicators['bollinger_lower'] = lower
        #FIXME: set number [-1,1] for buy, sell
        self.indicators['bollinger'] = 0.0

        #calc rsi
        rsi = ta.RSI(self.indicators['price'], timeperiod=14)
        self.indicators['rsi_ind'] = rsi
        #FIXME: convert to [-1,1] for sell, buy
        self.indicators['rsi'] = 0.0

        #calc on-balance volume
            #obv = prev volume + change in volume
            #FIXME: plot messed up but numbers are fine
        obv = ta.OBV(self.indicators['price'], self.indicators['volume'])
        self.indicators['obv_ind'] = obv
        #FIXME: convert to [-1,1] for sell, buy
        self.indicators['obv'] = 0.0

        #calc ema
        ema12 = ta.EMA(self.indicators['price'], timeperiod=12)
        ema26 = ta.EMA(self.indicators['price'], timeperiod=26)
        self.indicators['ema12'] = ema12
        self.indicators['ema26'] = ema26

        #debug plot
        #window = 0
        #self.plot(['volume', 'obv'], days=window)
        #self.plot(['fifty', 'rsi'], days=window)
        #self.plot(['zero', 'macd_ind', 'macd_signal'], days=100)
        #self.plot(['price', 'ema12', 'ema26'], days=window)
        #self.plot(['price', 'upperbb', 'middlebb','lowerbb'], days=window)
        #sys.exit()

    def evaluate(self):
        evaluation = 0.0
        for key in self.indicator_listing:
            evaluation += self.indicators[key] * self.weights[key]
        self.evaluation = evaluation
        
        #random evaluation
        if cfg.random_trades:
            scalar = 1 if random.random() < 0.5 else -1
            self.evaluation = scalar * random.random()

    def plot(self, keys, days=0):
        #FIXME: https://stackoverflow.com/questions/9673988/intraday-candlestick-charts-using-matplotlib
        #BETTER FIXME: https://www.quantopian.com/posts/plot-candlestick-charts-in-research
        for key in keys:
            y = self.indicators[key][-days:-1]
            x = self.indicators['date'][-days:-1]
            if key == 'price' or key == 'zero' or key == 'volume':
                plt.plot(x, y,'b-', color='black', label=key)
            else:
                plt.plot(x, y,'-', label=key)
        plt.title('daily chart %s' % self.symbol)
        plt.xlabel('date')
        plt.ylabel('price')
        plt.legend(loc='best')
        plt.show()

#chooses symbol based on evaluation
def best_eval(evals):
    choices = []
    for symbol in evals:
        if not evals[symbol].data.size > 0: #no nflx data until 2002
            continue
        if abs(evals[symbol].evaluation) > cfg.eval_threshold:
            choices.append(evals[symbol])
    #FIXME: sort by bigger absolute val of eval then by cheaper price
    return choices

def pick_trade(choice):
    min_buypower = cfg.minshares * choice.price + 2 * cfg.commission
    min_sellpower = cfg.commission
    buypower = cfg.api.account_buypower()
    shares = int(buypower / choice.price)
    position = cfg.api.account_positions()[choice.symbol][0]

    #debug print reason for no trade
    if choice.evaluation > 0:
        print '    BUYING: %s' % choice.symbol
        if choice.evaluation <= cfg.eval_threshold:
            print '        NO BUY: eval below threshold %s' % (
                    cfg.eval_threshold,)
        if buypower <= min_buypower:
            print '        NO BUY: not enough buypower %s < %s' % (buypower,
                    min_buypower)
        if position > 0:
            print '        NO BUY: already holding a position'

    if choice.evaluation < 0:
        print '    SELLING: %s' % choice.symbol
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

