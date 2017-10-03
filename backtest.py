
from dateutil import rrule
from datetime import datetime, timedelta

import analyze as lyz
import config as cfg
from misc import *

def backtest():
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
            #query date for split, dividends
                #db close price adjusted for splits
                #db adjclose price adjusted for splits and dividends

            #analyze

            #FIXME: store in structure with max evals at top
                #aka evals[0] = max
                #check evals[1] for tie and choose cheaper stock
            obj = lyz.Analyze(symbol, date)
            evals[symbol] = obj.evaluation

        #choose best evaluation and trade if able to
        msg(evals)
    
    print #debug spacing

def best_eval(evals):
    #break tie with shareprice, lower = better
    #use absolute value, more negative = better sell
    return [('NFLX', 0.0)]

