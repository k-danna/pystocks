
import random
import time
from dateutil import rrule
from datetime import datetime, timedelta

import config as cfg
import analyze
from misc import msg

def test():
    #iterate daily through weekdays
    for day in rrule.rrule(rrule.DAILY, dtstart=cfg.test_begin, 
            until=cfg.test_end):

        #skip weekends, holidays (only for holidays 1995 onward)
        date = str(day.date())
        if day.weekday() > 4 or date in cfg.holidays:
            continue

        day_start = time.time()

        #DEBUG
        if date != '2017-09-29':
            continue

        #analyze all symbols 
        evals = {}
        for symbol in cfg.tickers:
            evals[symbol] = analyze.Analyze(symbol, date)
            print '    eval: ', symbol, evals[symbol].evaluation

        #choose best evaluation
        choice = analyze.best_eval(evals)
        print '        chose: %s' % choice.symbol

        #create trade to buy/sell/pass number of shares at price
        symbol, price, shares = analyze.pick_trade(choice)
        if shares > 0:
            cfg.api.buy(symbol, shares, price, date)
        elif shares < 0:
            cfg.api.flatten(symbol, price, date)

        msg('%s analyzed in %s' % (date, time.time() - day_start))
        
        #update account at end of day
        cfg.api.update_account(date)

    #flatten any open positions at end
    cfg.api.close_all(str(cfg.test_end.date()))

    #update account
    cfg.api.update_account(date)

    #output/store batch stats
        #data time interval (bars)
    #min/max/avg
        #trade time length
        #num trades per symbol
        #good bad trade ratio
        #gain/loss, profit
        #exposure/risk (max in market at one time)
        #return per year
        #risk adjusted return
    
    #output/store min/max/avg net stats for all batches

def train():
    #TODO: backtest starting each day
        #save and avg stats per each
        #batch test with random intervals, starting points
            #this solves trading in depression vs bubble and overfitting
                #test with randomly located, length intervals of time

    #output/store batch stats
        #data time interval (bars)
    #min/max/avg
        #trade time length
        #num trades per symbol
        #good bad trade ratio
        #gain/loss, profit
        #exposure/risk (max in market at one time)
        #return per year
        #risk adjusted return
    
    #output/store min/max/avg net stats for all batches
    pass
