
import random
from dateutil import rrule
from datetime import datetime, timedelta

import analyze as lyz
import config as cfg
from misc import *

random.seed(cfg.seed)

def backtest():
    
    #TODO: backtest starting each day
        #save and avg stats per each
        #batch test with random intervals, starting points
            #this solves trading in depression vs bubble and overfitting
                #test with randomly located, length intervals of time

    final_day = datetime(2017, 9, 29)
    #iterate daily through weekdays since cfg.test_begin
    for day in rrule.rrule(rrule.DAILY, dtstart=cfg.test_begin, 
            until=final_day):

        #skip weekends, holidays (holidays only 1995 onward)
        date = str(day.date()) #formate date for db
        if day.weekday() > 4 or date in cfg.holidays:
            continue

        #DEBUG
        #if date != '2017-09-29':
        #    continue

        #analyze and choose best evaluation
        evals = {}
        best = ()
        for symbol in cfg.tickers:
            evals[symbol] = lyz.Analyze(symbol, date)
            #no nflx data until 2002
            if evals[symbol].price == 0.0: 
                continue
            if not best or abs(evals[symbol].evaluation) > abs(best[1]):
                best = (symbol, evals[symbol].evaluation)

        #choose best evaluation
        choice = evals[best[0]]

        #trade if we have the money to do so
            #no short selling for now
        min_buy = (cfg.minshares * choice.price) + (2 * cfg.commission)
        min_sell = cfg.commission
        if choice.evaluation > 0.0 and cfg.account.buypower > min_buy:
            #buy
            cfg.api.buy(choice.symbol, cfg.minshares, choice.price, 
                    date)
        elif choice.evaluation < 0.0 and cfg.account.buypower > min_sell:
            #sell if we own the symbol
            cfg.api.flatten(choice.symbol, choice.price, date)



        #buy or sell
        #if cfg.account.positions[choice.symbol] == 0:
        #    #make sure we have money
        #    if cfg.account.buypower > (cfg.minshares * choice.price):
        #        cfg.api.buy(choice.symbol, cfg.minshares, choice.price, 
        #                date)
        #else:
        #    #sell if already bought
        #    cfg.api.flatten(choice.symbol, choice.price, date)
        
        #update account
        cfg.account.update(date)

    #flatten any open positions at end
    date = str(final_day.date())
    for symbol in cfg.tickers:
        price = lyz.Analyze(symbol, date).price
        cfg.api.flatten(symbol, price, date)

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

def best_eval(evals):
    #break tie with shareprice, lower = better
    #use absolute value, more negative = better sell
    return [('NFLX', 0.0)]

