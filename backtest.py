
from dateutil import rrule
from datetime import datetime, timedelta

import analyze as lyz
import config as cfg
from misc import *

def backtest():
    
    #TODO: backtest starting each day
        #save and avg stats per each
        #this solves trading in depression vs bubble / overfitting to past
            #test with random located, length intervals of time
            #start randomly, trade until random date, take stats

    #iterate through weekdays since cfg.test_begin
    for day in rrule.rrule(rrule.DAILY, dtstart=cfg.test_begin, 
            until=cfg.today):

        #skip weekends
        if day.weekday() > 4:
            continue

        #DEBUG
        date = str(day.date())
        if date != '2017-09-29':
            continue
        msg('analyzing: %s' % date)

        evals = {}
        for symbol in cfg.tickers:
            #analyze
            obj = lyz.Analyze(symbol, date)
            evals[symbol] = obj.evaluation

        #choose best evaluation and trade if able to
        msg(evals)

    #output stats
        #data time interval (bars)
    #min/max/avg/net
        #trade time length
        #num trades per symbol
        #good bad trade ratio
        #gain/loss, profit
        #volatility measure
        #exposure/risk (max in market at one time)
        #return per year
        #risk adjusted return
    

    #debug spacing
    print

def best_eval(evals):
    #break tie with shareprice, lower = better
    #use absolute value, more negative = better sell
    return [('NFLX', 0.0)]

