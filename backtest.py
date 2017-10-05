
import random
from dateutil import rrule
from datetime import datetime, timedelta

import analyze as lyz
import config as cfg
from misc import *

def backtest():
    
    #TODO: backtest starting each day
        #save and avg stats per each
        #batch test with random intervals, starting points
            #this solves trading in depression vs bubble and overfitting
                #test with randomly located, length intervals of time

    first_day = cfg.test_begin
    last_day = cfg.test_end
    #iterate daily through weekdays
    for day in rrule.rrule(rrule.DAILY, dtstart=first_day, 
            until=last_day):

        #skip weekends, holidays (only for holidays 1995 onward)
        date = str(day.date()) #formate date for db
        if day.weekday() > 4 or date in cfg.holidays:
            continue

        #DEBUG
        #if date != '2017-09-29':
        #    continue

        #analyze all symbols 
        evals = {}
        for symbol in cfg.tickers:
            evals[symbol] = lyz.Analyze(symbol, date)

        #choose best evaluation
        choice = lyz.best_eval(evals)

        #create trade to buy/sell/pass number of shares at price
        symbol, price, shares = lyz.pick_trade(choice)
        if shares > 0:
            cfg.api.buy(symbol, shares, price, date)
        elif shares < 0:
            cfg.api.flatten(symbol, price, date)
        
        #update account at end of day
        cfg.account.update(date)

    #flatten any open positions at end
    cfg.api.close_all(str(last_day.date))

    #update account
    cfg.account.update(date)

    #output/store batch stats
        #data time interval (bars)
    #min/max/avg
        #trade time length
        #num trades per symbol
        #good bad trade ratio
        #gain/loss, profit
        #volatility measure
        #exposure/risk (max in market at one time)
        #return per year
        #risk adjusted return
    
    #output/store min/max/avg net stats for all batches

    #debug spacing
    print

