
from dateutil import rrule
from datetime import datetime, timedelta

import analyze as lyz
import config as cfg
from misc import *

def backtest():
    #iterate through weekdays since cfg.test_begin
    evals = {}
    for date in rrule.rrule(rrule.DAILY, dtstart=cfg.test_begin, 
            until=cfg.today):

        #skip weekends
        if date.weekday() > 4:
            continue

        #debug
        #msg(date)

        #query current, prevs days info
            #if dne calc and insert
            #FIXME: store in structure with max evals at top
                #aka evals[0] = max
                #check evals[1] for tie and choose cheaper stock
        for symbol in cfg.tickers:
            obj = lyz.Analyze(symbol)
            evals[symbol] = obj.evaluation

        #choose best evaluation and trade if able to

def get_data(symbol):
    return 0



#INFO: iterate through year
#https://stackoverflow.com/questions/153584/how-to-iterate-over-a-timespan-after-days-hours-weeks-and-months-in-python#155172

#INFO: best way to format queries
#https://stackoverflow.com/questions/5243596/python-sql-query-string-formatting

