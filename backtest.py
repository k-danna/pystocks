
import random
import time
from dateutil import rrule
from datetime import datetime, timedelta

import config as cfg
import analyze
from misc import msg

def backtest(weights):
    #iterate daily through weekdays
    for day in rrule.rrule(rrule.DAILY, dtstart=cfg.test_begin, 
            until=cfg.test_end):

        #skip weekends, holidays (only for holidays 1995 onward)
        date = str(day.date())
        if day.weekday() > 4 or date in cfg.holidays:
            continue

        day_start = time.time()

        #DEBUG
        #if date != '2017-09-29':
        #    continue

        #analyze all symbols 
        evals = {}
        for symbol in cfg.tickers:
            evals[symbol] = analyze.Analyze(symbol, date, weights)
            #print '    eval: ', symbol, evals[symbol].evaluation

        #choose best evaluations
        choices = analyze.best_eval(evals)
        for choice in choices:
            #create trade to buy/sell/pass number of shares at price
            symbol, price, shares = analyze.pick_trade(choice)
            if shares > 0:
                cfg.api.buy(symbol, shares, price, date)
            elif shares < 0:
                cfg.api.flatten(symbol, price, date)

        elapsed = round(time.time() - day_start, 3)
        msg('%s analyzed in %s (%s - %s)' % (date, elapsed,
                cfg.api.account_balance(), cfg.api.account_networth()))
        
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

    #choose random day and time interval (min 1 year)
        #backtest choosing subset of indicators, weights
            #for each sell adjust weights accordingly
                #bad trade - subtract weight
                #good trade - add weight
        #return the weights
        #weights passed to test phase

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
    return {}
